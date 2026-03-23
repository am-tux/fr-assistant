"""GitHub Discussions tracking via GitHub API"""

import os
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import re


class DiscussionsTracker:
    """Tracks GitHub Discussions for a repository"""

    def __init__(self, repo_config: Dict[str, Any], github_api_config: Dict[str, Any]):
        """Initialize discussions tracker

        Args:
            repo_config: Repository configuration from config.yaml
            github_api_config: GitHub API configuration
        """
        self.name = repo_config['name']
        self.discussions_enabled = repo_config.get('track_discussions', False)

        if not self.discussions_enabled:
            return

        # Parse GitHub URL to get owner/repo
        url = repo_config['url']
        match = re.match(r'https://github\.com/([^/]+)/([^/]+)', url)
        if match:
            self.owner = match.group(1)
            self.repo = match.group(2)
        else:
            raise ValueError(f"Invalid GitHub URL: {url}")

        # API configuration
        self.token = github_api_config.get('token', '')
        self.respect_rate_limits = github_api_config.get('respect_rate_limits', True)
        self.rate_limit_buffer = github_api_config.get('rate_limit_buffer', 100)

        # Discussion channels configuration
        discussions_config = repo_config.get('discussions_config', {})
        self.channels = discussions_config.get('channels', {})

        # Headers for API requests
        self.headers = {
            'Accept': 'application/vnd.github+json',
        }
        if self.token:
            self.headers['Authorization'] = f'Bearer {self.token}'

        # GraphQL endpoint (GitHub Discussions uses GraphQL)
        self.graphql_url = 'https://api.github.com/graphql'

    def get_discussions(self, since: Optional[datetime] = None,
                        state: str = 'OPEN') -> List[Dict[str, Any]]:
        """Get discussions from the repository

        Args:
            since: Get discussions updated since this datetime
            state: Discussion state (OPEN, CLOSED, or None for all)

        Returns:
            List of discussion dictionaries
        """
        if not self.discussions_enabled:
            return []

        # GraphQL query for discussions
        query = """
        query($owner: String!, $repo: String!, $first: Int!, $after: String) {
          repository(owner: $owner, name: $repo) {
            discussions(first: $first, after: $after, orderBy: {field: UPDATED_AT, direction: DESC}) {
              pageInfo {
                hasNextPage
                endCursor
              }
              nodes {
                id
                number
                title
                body
                url
                createdAt
                updatedAt
                author {
                  login
                }
                category {
                  name
                }
                labels(first: 10) {
                  nodes {
                    name
                  }
                }
                comments {
                  totalCount
                }
                reactions {
                  totalCount
                }
                answer {
                  id
                  createdAt
                  author {
                    login
                  }
                }
                answerChosenAt
              }
            }
          }
        }
        """

        variables = {
            'owner': self.owner,
            'repo': self.repo,
            'first': 100,
            'after': None
        }

        all_discussions = []
        has_next_page = True

        while has_next_page:
            try:
                response = requests.post(
                    self.graphql_url,
                    json={'query': query, 'variables': variables},
                    headers=self.headers,
                    timeout=30
                )

                if response.status_code == 200:
                    data = response.json()

                    if 'errors' in data:
                        print(f"GraphQL errors: {data['errors']}")
                        break

                    discussions_data = data['data']['repository']['discussions']
                    nodes = discussions_data['nodes']

                    # Process discussions
                    for node in nodes:
                        # Filter by date if specified
                        if since:
                            updated_at = datetime.fromisoformat(node['updatedAt'].replace('Z', '+00:00'))
                            if updated_at < since:
                                has_next_page = False
                                break

                        discussion = self._parse_discussion(node)
                        all_discussions.append(discussion)

                    # Pagination
                    page_info = discussions_data['pageInfo']
                    has_next_page = page_info['hasNextPage'] and has_next_page
                    if has_next_page:
                        variables['after'] = page_info['endCursor']
                    else:
                        break

                else:
                    if response.status_code == 403 and 'rate limit' in response.text.lower():
                        print(f"⚠️  GitHub API rate limit reached. Discussions data will be unavailable.")
                        print(f"   (Continuing with git data only. Set GITHUB_TOKEN for higher limits.)")
                    else:
                        print(f"Error fetching discussions: {response.status_code} - {response.text}")
                    break

            except Exception as e:
                print(f"Exception fetching discussions: {e}")
                break

        return all_discussions

    def _parse_discussion(self, node: Dict[str, Any]) -> Dict[str, Any]:
        """Parse a discussion node from GraphQL response"""
        # Extract labels
        labels = [label['name'] for label in node.get('labels', {}).get('nodes', [])]

        # Determine channel based on labels and keywords
        channel = self._classify_channel(node['title'], node.get('body', ''), labels)

        # Parse dates
        created_at = datetime.fromisoformat(node['createdAt'].replace('Z', '+00:00'))
        updated_at = datetime.fromisoformat(node['updatedAt'].replace('Z', '+00:00'))

        # Check if answered
        is_answered = node.get('answer') is not None
        answer_time = None
        answerer = None

        if is_answered and node.get('answerChosenAt'):
            answer_time = datetime.fromisoformat(node['answerChosenAt'].replace('Z', '+00:00'))
            if node['answer'] and node['answer'].get('author'):
                answerer = node['answer']['author'].get('login', 'Unknown')

        discussion = {
            'id': node['id'],
            'number': node['number'],
            'title': node['title'],
            'body': node.get('body', ''),
            'url': node['url'],
            'created_at': created_at,
            'updated_at': updated_at,
            'author': node['author']['login'] if node.get('author') else 'Unknown',
            'category': node['category']['name'] if node.get('category') else 'General',
            'labels': labels,
            'channel': channel,
            'comment_count': node['comments']['totalCount'],
            'reaction_count': node['reactions']['totalCount'],
            'is_answered': is_answered,
            'answer_time': answer_time,
            'answerer': answerer
        }

        return discussion

    def _classify_channel(self, title: str, body: str, labels: List[str]) -> str:
        """Classify discussion into a channel based on keywords and labels

        Args:
            title: Discussion title
            body: Discussion body
            labels: List of label names

        Returns:
            Channel name (20x, Rev5, RFCs, or General)
        """
        text = f"{title} {body}".lower()

        # Check each channel configuration
        for channel_name, config in self.channels.items():
            if not config.get('enabled', True):
                continue

            # Check labels
            channel_labels = [label.lower() for label in config.get('labels', [])]
            if any(label.lower() in channel_labels for label in labels):
                return channel_name

            # Check keywords
            keywords = [kw.lower() for kw in config.get('keywords', [])]
            if any(keyword in text for keyword in keywords):
                return channel_name

        return 'General'

    def get_new_discussions(self, since: datetime) -> List[Dict[str, Any]]:
        """Get discussions created since a specific datetime

        Args:
            since: Get discussions created after this datetime

        Returns:
            List of discussion dictionaries
        """
        all_discussions = self.get_discussions()
        return [d for d in all_discussions if d['created_at'] >= since]

    def get_active_discussions(self, since: datetime) -> List[Dict[str, Any]]:
        """Get discussions with activity since a specific datetime

        Args:
            since: Get discussions updated after this datetime

        Returns:
            List of discussion dictionaries
        """
        all_discussions = self.get_discussions()
        return [d for d in all_discussions if d['updated_at'] >= since]

    def get_unanswered_discussions(self, older_than_hours: int = 48) -> List[Dict[str, Any]]:
        """Get unanswered discussions older than specified hours

        Args:
            older_than_hours: Get unanswered discussions older than this many hours

        Returns:
            List of discussion dictionaries
        """
        cutoff_time = datetime.now().astimezone() - timedelta(hours=older_than_hours)
        all_discussions = self.get_discussions()

        return [
            d for d in all_discussions
            if not d['is_answered'] and d['created_at'] < cutoff_time
        ]

    def get_discussions_by_channel(self, channel: str,
                                   since: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """Get discussions for a specific channel

        Args:
            channel: Channel name (20x, Rev5, RFCs, General)
            since: Optional datetime filter

        Returns:
            List of discussion dictionaries
        """
        all_discussions = self.get_discussions(since=since)
        return [d for d in all_discussions if d['channel'] == channel]

    def get_open_rfcs(self, sort_by: str = 'newest') -> List[Dict[str, Any]]:
        """Get open RFC discussions

        Args:
            sort_by: Sort order (newest, oldest, most_comments, most_reactions)

        Returns:
            List of RFC discussion dictionaries with topic classification
        """
        # Get RFCs channel discussions
        rfcs = self.get_discussions_by_channel('RFCs')

        # Filter to open RFCs only
        open_rfcs = [d for d in rfcs if not d['is_answered']]

        # Classify by topic (Rev5, 20x, General)
        for rfc in open_rfcs:
            rfc['topic'] = self._classify_rfc_topic(rfc)

        # Sort
        if sort_by == 'newest':
            open_rfcs.sort(key=lambda x: x['created_at'], reverse=True)
        elif sort_by == 'oldest':
            open_rfcs.sort(key=lambda x: x['created_at'])
        elif sort_by == 'most_comments':
            open_rfcs.sort(key=lambda x: x['comment_count'], reverse=True)
        elif sort_by == 'most_reactions':
            open_rfcs.sort(key=lambda x: x['reaction_count'], reverse=True)

        return open_rfcs

    def _classify_rfc_topic(self, rfc: Dict[str, Any]) -> str:
        """Classify RFC as Rev5, 20x, or General

        Args:
            rfc: RFC discussion dictionary

        Returns:
            Topic classification (Rev5, 20x, or General)
        """
        text = f"{rfc['title']} {rfc['body']}".lower()
        labels = [label.lower() for label in rfc.get('labels', [])]

        # Check for Rev5 indicators
        rev5_keywords = ['rev5', 'rev 5', 'revision 5', 'baseline', 'control update', 'control modification']
        rev5_labels = ['rev5', 'revision 5']

        if any(kw in text for kw in rev5_keywords) or any(label in rev5_labels for label in labels):
            return 'Rev5'

        # Check for 20x indicators
        twentyx_keywords = ['20x', 'fedramp 2.0', 'modernization', 'automation', 'continuous monitoring', 'cloud-native']
        twentyx_labels = ['20x', 'fedramp 2.0']

        if any(kw in text for kw in twentyx_keywords) or any(label in twentyx_labels for label in labels):
            return '20x'

        return 'General'

    def get_most_responded_discussions(self, timeframe: str = '7d',
                                        channel: str = 'all',
                                        limit: int = 10) -> List[Dict[str, Any]]:
        """Get discussions with most responses in a timeframe

        Args:
            timeframe: Time window (24h, 7d, 30d, all)
            channel: Channel filter (20x, Rev5, RFCs, all)
            limit: Maximum number of discussions to return

        Returns:
            List of discussion dictionaries sorted by comment count
        """
        # Parse timeframe
        since = None
        if timeframe == '24h':
            since = datetime.now().astimezone() - timedelta(hours=24)
        elif timeframe == '7d':
            since = datetime.now().astimezone() - timedelta(days=7)
        elif timeframe == '30d':
            since = datetime.now().astimezone() - timedelta(days=30)

        # Get discussions
        if channel == 'all':
            discussions = self.get_discussions(since=since)
        else:
            discussions = self.get_discussions_by_channel(channel, since=since)

        # Sort by comment count
        discussions.sort(key=lambda x: x['comment_count'], reverse=True)

        return discussions[:limit]
