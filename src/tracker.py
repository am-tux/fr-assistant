"""
Tracking management for FedRAMP discussions and keywords.

This module handles loading, saving, and managing tracked items
(discussions and keywords) for personalized monitoring.
"""

import yaml
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any


class TrackingManager:
    """Manages tracked discussions and keywords."""

    def __init__(self, config_path: str = "tracking.yaml"):
        """
        Initialize the tracking manager.

        Args:
            config_path: Path to tracking configuration file
        """
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """
        Load tracking configuration from YAML file.

        Returns:
            Dictionary with tracking configuration
        """
        if not os.path.exists(self.config_path):
            # Return empty structure if file doesn't exist
            return {
                'tracked_discussions': [],
                'tracked_keywords': [],
                'settings': {
                    'check_days_back': 7,
                    'case_insensitive_keywords': True,
                    'search_commits': True,
                    'search_discussions': True
                }
            }

        try:
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)

                # Ensure required keys exist
                if 'tracked_discussions' not in config:
                    config['tracked_discussions'] = []
                if 'tracked_keywords' not in config:
                    config['tracked_keywords'] = []
                if 'settings' not in config:
                    config['settings'] = {
                        'check_days_back': 7,
                        'case_insensitive_keywords': True,
                        'search_commits': True,
                        'search_discussions': True
                    }

                return config
        except Exception as e:
            print(f"Error loading tracking config: {e}")
            return {
                'tracked_discussions': [],
                'tracked_keywords': [],
                'settings': {
                    'check_days_back': 7,
                    'case_insensitive_keywords': True,
                    'search_commits': True,
                    'search_discussions': True
                }
            }

    def _save_config(self) -> bool:
        """
        Save tracking configuration to YAML file.

        Returns:
            True if saved successfully, False otherwise
        """
        try:
            with open(self.config_path, 'w') as f:
                yaml.dump(self.config, f, default_flow_style=False, sort_keys=False)
            return True
        except Exception as e:
            print(f"Error saving tracking config: {e}")
            return False

    def add_discussion(self, url: str, title: str = "", reason: str = "",
                      priority: str = "medium") -> bool:
        """
        Add a discussion to tracking.

        Args:
            url: GitHub discussion URL
            title: Discussion title (optional)
            reason: Why tracking this discussion (optional)
            priority: Priority level (critical, high, medium, low)

        Returns:
            True if added successfully, False if already tracked
        """
        # Check if already tracked
        for discussion in self.config['tracked_discussions']:
            if discussion['url'] == url:
                print(f"Discussion already tracked: {url}")
                return False

        # Add new discussion
        new_discussion = {
            'url': url,
            'title': title,
            'reason': reason,
            'priority': priority,
            'added': datetime.now().strftime('%Y-%m-%d')
        }

        self.config['tracked_discussions'].append(new_discussion)
        return self._save_config()

    def remove_discussion(self, url: str) -> bool:
        """
        Remove a discussion from tracking.

        Args:
            url: GitHub discussion URL to remove

        Returns:
            True if removed successfully, False if not found
        """
        original_count = len(self.config['tracked_discussions'])
        self.config['tracked_discussions'] = [
            d for d in self.config['tracked_discussions']
            if d['url'] != url
        ]

        if len(self.config['tracked_discussions']) == original_count:
            print(f"Discussion not found in tracking: {url}")
            return False

        return self._save_config()

    def add_keyword(self, term: str, context: str = "", priority: str = "medium") -> bool:
        """
        Add a keyword to tracking.

        Args:
            term: Keyword to track
            context: Context/reason for tracking (optional)
            priority: Priority level (critical, high, medium, low)

        Returns:
            True if added successfully, False if already tracked
        """
        # Check if already tracked
        for keyword in self.config['tracked_keywords']:
            if keyword['term'].lower() == term.lower():
                print(f"Keyword already tracked: {term}")
                return False

        # Add new keyword
        new_keyword = {
            'term': term,
            'context': context,
            'priority': priority,
            'added': datetime.now().strftime('%Y-%m-%d')
        }

        self.config['tracked_keywords'].append(new_keyword)
        return self._save_config()

    def remove_keyword(self, term: str) -> bool:
        """
        Remove a keyword from tracking.

        Args:
            term: Keyword to remove

        Returns:
            True if removed successfully, False if not found
        """
        original_count = len(self.config['tracked_keywords'])
        self.config['tracked_keywords'] = [
            k for k in self.config['tracked_keywords']
            if k['term'].lower() != term.lower()
        ]

        if len(self.config['tracked_keywords']) == original_count:
            print(f"Keyword not found in tracking: {term}")
            return False

        return self._save_config()

    def get_tracked_discussions(self) -> List[Dict[str, str]]:
        """
        Get list of tracked discussions.

        Returns:
            List of tracked discussion dictionaries
        """
        return self.config['tracked_discussions']

    def get_tracked_keywords(self) -> List[Dict[str, str]]:
        """
        Get list of tracked keywords.

        Returns:
            List of tracked keyword dictionaries
        """
        return self.config['tracked_keywords']

    def get_settings(self) -> Dict[str, Any]:
        """
        Get tracking settings.

        Returns:
            Dictionary of settings
        """
        return self.config['settings']

    def has_tracked_items(self) -> bool:
        """
        Check if any items are being tracked.

        Returns:
            True if tracking discussions or keywords, False otherwise
        """
        return (len(self.config['tracked_discussions']) > 0 or
                len(self.config['tracked_keywords']) > 0)

    def list_all(self) -> str:
        """
        Generate a formatted list of all tracked items.

        Returns:
            Formatted string showing all tracked items
        """
        output = []

        if not self.has_tracked_items():
            return "No tracked discussions or keywords.\n\nTo start tracking:\n  python3 main.py track add-discussion --url <URL>\n  python3 main.py track add-keyword --term <TERM>"

        # Tracked discussions
        if self.config['tracked_discussions']:
            output.append("📋 Tracked Discussions:")
            output.append("")
            for i, disc in enumerate(self.config['tracked_discussions'], 1):
                priority_emoji = {
                    'critical': '🚨',
                    'high': '📌',
                    'medium': '⚙️',
                    'low': 'ℹ️'
                }.get(disc.get('priority', 'medium'), '⚙️')

                output.append(f"{i}. {priority_emoji} {disc.get('title', 'Untitled')}")
                output.append(f"   URL: {disc['url']}")
                if disc.get('reason'):
                    output.append(f"   Reason: {disc['reason']}")
                output.append(f"   Priority: {disc.get('priority', 'medium')} | Added: {disc.get('added', 'unknown')}")
                output.append("")

        # Tracked keywords
        if self.config['tracked_keywords']:
            output.append("🔍 Tracked Keywords:")
            output.append("")
            for i, kw in enumerate(self.config['tracked_keywords'], 1):
                priority_emoji = {
                    'critical': '🚨',
                    'high': '📌',
                    'medium': '⚙️',
                    'low': 'ℹ️'
                }.get(kw.get('priority', 'medium'), '⚙️')

                output.append(f"{i}. {priority_emoji} \"{kw['term']}\"")
                if kw.get('context'):
                    output.append(f"   Context: {kw['context']}")
                output.append(f"   Priority: {kw.get('priority', 'medium')} | Added: {kw.get('added', 'unknown')}")
                output.append("")

        # Settings
        settings = self.config.get('settings', {})
        output.append("⚙️ Settings:")
        output.append(f"   Check last {settings.get('check_days_back', 7)} days for activity")
        output.append(f"   Case insensitive: {settings.get('case_insensitive_keywords', True)}")
        output.append(f"   Search commits: {settings.get('search_commits', True)}")
        output.append(f"   Search discussions: {settings.get('search_discussions', True)}")

        return "\n".join(output)


def create_default_config(config_path: str = "tracking.yaml") -> bool:
    """
    Create a default tracking.yaml from the sample file.

    Args:
        config_path: Path where to create the config file

    Returns:
        True if created successfully, False otherwise
    """
    sample_path = "tracking.yaml.sample"

    if os.path.exists(config_path):
        print(f"Config file already exists: {config_path}")
        return False

    if not os.path.exists(sample_path):
        print(f"Sample file not found: {sample_path}")
        return False

    try:
        import shutil
        shutil.copy(sample_path, config_path)
        print(f"Created tracking config: {config_path}")
        print("Edit this file to add your tracked items.")
        return True
    except Exception as e:
        print(f"Error creating config: {e}")
        return False


def search_keywords_in_text(text: str, keywords: List[str], case_insensitive: bool = True) -> Dict[str, List[int]]:
    """
    Search for keywords in text and return matches with positions.

    Args:
        text: Text to search in
        keywords: List of keywords to search for
        case_insensitive: Whether to perform case-insensitive search

    Returns:
        Dictionary mapping keyword -> list of positions found
    """
    matches = {}

    for keyword in keywords:
        search_text = text.lower() if case_insensitive else text
        search_keyword = keyword.lower() if case_insensitive else keyword

        positions = []
        start = 0
        while True:
            pos = search_text.find(search_keyword, start)
            if pos == -1:
                break
            positions.append(pos)
            start = pos + 1

        if positions:
            matches[keyword] = positions

    return matches


def search_keywords_in_commits(commits: List[Dict], tracked_keywords: List[Dict]) -> List[Dict]:
    """
    Search for tracked keywords in commit messages.

    Args:
        commits: List of commit dictionaries (from GitTracker)
        tracked_keywords: List of tracked keyword dictionaries

    Returns:
        List of matches with commit info and matched keywords
    """
    if not tracked_keywords:
        return []

    keywords = [kw['term'] for kw in tracked_keywords]
    keyword_dict = {kw['term']: kw for kw in tracked_keywords}
    case_insensitive = True  # Default, could come from settings

    matches = []

    for commit in commits:
        message = commit.get('message', '')
        found = search_keywords_in_text(message, keywords, case_insensitive)

        if found:
            for keyword in found.keys():
                matches.append({
                    'keyword': keyword,
                    'keyword_info': keyword_dict[keyword],
                    'commit': commit,
                    'match_type': 'commit_message',
                    'repository': commit.get('repository', 'unknown')
                })

    return matches


def search_keywords_in_discussions(rfcs: List[Dict], tracked_keywords: List[Dict]) -> List[Dict]:
    """
    Search for tracked keywords in discussion titles.

    Args:
        rfcs: List of RFC/discussion dictionaries (from WebScraper)
        tracked_keywords: List of tracked keyword dictionaries

    Returns:
        List of matches with discussion info and matched keywords
    """
    if not tracked_keywords:
        return []

    keywords = [kw['term'] for kw in tracked_keywords]
    keyword_dict = {kw['term']: kw for kw in tracked_keywords}
    case_insensitive = True  # Default, could come from settings

    matches = []

    for rfc in rfcs:
        title = rfc.get('title', '')
        found = search_keywords_in_text(title, keywords, case_insensitive)

        if found:
            for keyword in found.keys():
                matches.append({
                    'keyword': keyword,
                    'keyword_info': keyword_dict[keyword],
                    'discussion': rfc,
                    'match_type': 'discussion_title'
                })

    return matches
