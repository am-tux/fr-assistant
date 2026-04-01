"""Web scraping for FedRAMP public pages"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import re
import feedparser


class WebScraper:
    """Scrapes public FedRAMP web pages for updates"""

    def __init__(self):
        self.headers = {
            'User-Agent': 'FedRAMP-Git-Tracker/1.0'
        }

    def get_github_rfcs(self, since: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """Scrape GitHub Discussions RFCs from FedRAMP/community

        Args:
            since: Get RFCs after this datetime

        Returns:
            List of RFC dictionaries with title, author, date, url, comments
        """
        url = "https://github.com/FedRAMP/community/discussions/categories/rfcs"

        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            rfcs = []

            # Find all discussion links
            all_links = soup.find_all('a', href=True)

            for link in all_links:
                try:
                    url_path = link.get('href', '')
                    if not url_path:
                        continue

                    # Only keep links to specific discussions (have a number)
                    # Pattern: /FedRAMP/community/discussions/101
                    if not re.search(r'/discussions/\d+$', url_path):
                        continue

                    title = link.get_text(strip=True)
                    if not title or len(title) < 5:  # Skip empty or very short titles
                        continue

                    # Make URL absolute
                    if url_path.startswith('/'):
                        full_url = f"https://github.com{url_path}"
                    else:
                        full_url = url_path

                    # Skip if we've already added this URL
                    if any(rfc['url'] == full_url for rfc in rfcs):
                        continue

                    # Extract date if available from parent elements
                    parent = link.find_parent()
                    date_str = ""
                    author = "Unknown"
                    comments = 0

                    if parent:
                        # Try to find relative-time element
                        time_elem = parent.find('relative-time')
                        if time_elem:
                            date_str = time_elem.get('datetime', '')

                        # Try to find author
                        author_elem = parent.find('a', class_='author')
                        if author_elem:
                            author = author_elem.get_text(strip=True)

                    # Parse datetime if available
                    rfc_date = None
                    if date_str:
                        try:
                            rfc_date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                        except:
                            pass

                    # Filter by date if specified and date is available
                    if since and rfc_date and rfc_date < since:
                        continue

                    rfcs.append({
                        'title': title,
                        'author': author,
                        'date': date_str if date_str else "Unknown",
                        'url': full_url,
                        'comments': comments
                    })

                except Exception as e:
                    # Skip individual parsing errors
                    continue

            return rfcs

        except requests.RequestException as e:
            print(f"Error fetching GitHub RFCs: {e}")
            return []

    def get_fedramp_blog_posts(self, since: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """Scrape FedRAMP.gov blog for recent posts

        Note: FedRAMP.gov is a JavaScript-based single-page application.
        Blog content cannot be scraped without a headless browser.
        This function returns an empty list with a note.

        Args:
            since: Get posts after this datetime

        Returns:
            Empty list (blog requires JavaScript rendering)
        """
        # FedRAMP.gov uses SvelteKit - content loads via JavaScript
        # Traditional scraping doesn't work without a headless browser
        # For now, return empty list
        return []

    def get_fedramp_events(self, days_ahead: int = 7) -> List[Dict[str, Any]]:
        """Scrape FedRAMP.gov events page for upcoming meetings

        Note: FedRAMP.gov is a JavaScript-based single-page application.
        Event content cannot be scraped without a headless browser.
        This function returns an empty list with a note.

        Args:
            days_ahead: Number of days ahead to look for events

        Returns:
            Empty list (events page requires JavaScript rendering)
        """
        # FedRAMP.gov uses SvelteKit - content loads via JavaScript
        # Traditional scraping doesn't work without a headless browser
        # For now, return empty list
        return []

    def get_discussion_activity(self, discussion_url: str) -> Optional[Dict[str, Any]]:
        """Get detailed activity information for a specific discussion

        Args:
            discussion_url: Full URL to GitHub discussion

        Returns:
            Dictionary with comment_count, last_activity, participants, or None if error
        """
        try:
            response = requests.get(discussion_url, headers=self.headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # Find comment count
            comment_count = 0

            # Try to find comment count in various places
            # Look for elements like "5 comments" or discussion metadata
            timeline = soup.find('div', class_='js-discussion')
            if timeline:
                # Count all comment divs
                comments = timeline.find_all('div', class_='timeline-comment')
                comment_count = len(comments)

            # Alternative: look for comment counter in sidebar
            comment_label = soup.find('span', string=re.compile(r'\d+\s+comments?', re.IGNORECASE))
            if comment_label:
                match = re.search(r'(\d+)', comment_label.get_text())
                if match:
                    comment_count = int(match.group(1))

            # Find last activity timestamp
            last_activity = None
            last_activity_str = "Unknown"

            # Look for relative-time elements
            time_elements = soup.find_all('relative-time')
            if time_elements:
                # Get the most recent timestamp
                timestamps = []
                for elem in time_elements:
                    datetime_str = elem.get('datetime', '')
                    if datetime_str:
                        try:
                            dt = datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
                            timestamps.append(dt)
                        except:
                            pass

                if timestamps:
                    last_activity = max(timestamps)
                    last_activity_str = last_activity.strftime('%Y-%m-%d %H:%M:%S UTC')

            # Find participants
            participants = []
            author_links = soup.find_all('a', class_='author')
            seen = set()
            for link in author_links:
                username = link.get_text(strip=True)
                if username and username not in seen:
                    participants.append(username)
                    seen.add(username)

            # Get discussion title
            title = "Unknown"
            title_elem = soup.find('h1', class_='gh-header-title')
            if title_elem:
                title = title_elem.get_text(strip=True)

            return {
                'url': discussion_url,
                'title': title,
                'comment_count': comment_count,
                'last_activity': last_activity_str,
                'last_activity_datetime': last_activity,
                'participants': participants,
                'participant_count': len(participants)
            }

        except requests.RequestException as e:
            print(f"Error fetching discussion activity: {e}")
            return None
        except Exception as e:
            print(f"Error parsing discussion: {e}")
            return None

    def get_fedramp_notices(self, since: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """Get FedRAMP notices from RSS feed

        Args:
            since: Get notices after this datetime

        Returns:
            List of notice dictionaries with title, link, date, description, content
        """
        rss_url = "https://www.fedramp.gov/notices/rss.xml"

        try:
            # Fetch RSS content using requests (handles SSL better)
            response = requests.get(rss_url, headers=self.headers, timeout=10)
            response.raise_for_status()

            # Parse RSS feed from content
            feed = feedparser.parse(response.content)

            if feed.bozo:
                # Feed parsing error
                print(f"Error parsing RSS feed: {feed.bozo_exception}")
                return []

            notices = []

            for entry in feed.entries:
                try:
                    # Extract fields
                    title = entry.get('title', 'Untitled')
                    link = entry.get('link', '')
                    description = entry.get('description', '')

                    # Get full content if available
                    content = ''
                    if 'content' in entry and entry.content:
                        content = entry.content[0].get('value', '')
                    elif 'summary' in entry:
                        content = entry.summary

                    # Parse date
                    published_date = None
                    date_str = "Unknown"

                    if 'published_parsed' in entry and entry.published_parsed:
                        from time import mktime
                        published_date = datetime.fromtimestamp(mktime(entry.published_parsed))
                        date_str = published_date.strftime('%Y-%m-%d')
                    elif 'published' in entry:
                        date_str = entry.published

                    # Filter by date if specified
                    if since and published_date and published_date < since:
                        continue

                    notices.append({
                        'title': title,
                        'link': link,
                        'date': date_str,
                        'date_obj': published_date,
                        'description': description,
                        'content': content
                    })

                except Exception as e:
                    # Skip individual entry parsing errors
                    print(f"Error parsing notice entry: {e}")
                    continue

            return notices

        except Exception as e:
            print(f"Error fetching FedRAMP notices RSS: {e}")
            return []
