"""Web scraping for FedRAMP public pages"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import re


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
