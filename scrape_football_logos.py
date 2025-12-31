import requests
from bs4 import BeautifulSoup
import json
import re
from urllib.parse import urljoin
import time

def get_country_flag_emoji(country_slug):
    """Map country slugs to flag emojis"""
    flag_map = {
        'england': '🏴󠁧󠁢󠁥󠁮󠁧󠁿',
        'spain': '🇪🇸',
        'italy': '🇮🇹',
        'germany': '🇩🇪',
        'france': '🇫🇷',
        'portugal': '🇵🇹',
        'netherlands': '🇳🇱',
        'brazil': '🇧🇷',
        'turkey': '🇹🇷',
        'scotland': '🏴󠁧󠁢󠁳󠁣󠁴󠁿',
        'belgium': '🇧🇪',
        'argentina': '🇦🇷',
        'albania': '🇦🇱',
        'algeria': '🇩🇿',
        'australia': '🇦🇺',
        'austria': '🇦🇹',
        'belarus': '🇧🇾',
        'bulgaria': '🇧🇬',
        'cameroon': '🇨🇲',
        'canada': '🇨🇦',
        'chile': '🇨🇱',
        'china': '🇨🇳',
        'colombia': '🇨🇴',
        'croatia': '🇭🇷',
        'cyprus': '🇨🇾',
        'czech-republic': '🇨🇿',
        'denmark': '🇩🇰',
        'ecuador': '🇪🇨',
        'egypt': '🇪🇬',
        'finland': '🇫🇮',
        'greece': '🇬🇷',
        'hungary': '🇭🇺',
        'iceland': '🇮🇸',
        'india': '🇮🇳',
        'indonesia': '🇮🇩',
        'iran': '🇮🇷',
        'iraq': '🇮🇶',
        'israel': '🇮🇱',
        'japan': '🇯🇵',
        'mexico': '🇲🇽',
        'morocco': '🇲🇦',
        'nigeria': '🇳🇬',
        'norway': '🇳🇴',
        'poland': '🇵🇱',
        'qatar': '🇶🇦',
        'romania': '🇷🇴',
        'russia': '🏳',
        'saudi-arabia': '🇸🇦',
        'senegal': '🇸🇳',
        'serbia': '🇷🇸',
        'south-africa': '🇿🇦',
        'south-korea': '🇰🇷',
        'sweden': '🇸🇪',
        'switzerland': '🇨🇭',
        'tunisia': '🇹🇳',
        'ukraine': '🇺🇦',
        'uruguay': '🇺🇾',
        'usa': '🇺🇸',
        'wales': '🏴󠁧󠁢󠁷󠁬󠁳󠁿',
    }
    return flag_map.get(country_slug.lower(), '🏳️')

def extract_country_from_url(url):
    """Extract country slug from logo URL path"""
    if not url:
        return None
    match = re.search(r'/logos/([^/]+)/', url)
    if match:
        return match.group(1)
    return None

def scrape_team_from_element(element, base_url):
    """Extract team data from an HTML element"""
    img = element.find('img', src=True)
    if not img:
        return None
    
    img_src = img.get('src') or img.get('data-src') or img.get('data-lazy-src')
    if not img_src:
        return None
    
    logo_url = urljoin(base_url, img_src)
    
    # Extract country from URL
    country_slug = extract_country_from_url(logo_url)
    
    # Find team name
    team_name = None
    
    # Try alt text first
    alt_text = img.get('alt', '')
    if alt_text and 'logo' not in alt_text.lower() and len(alt_text) > 2:
        team_name = alt_text.strip()
    
    # Try heading tags
    if not team_name:
        for tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            name_elem = element.find(tag)
            if name_elem:
                text = name_elem.get_text(strip=True)
                text = re.sub(r'[🇦-🇿🏴]+', '', text).strip()
                text = re.sub(r'\([^)]+\)', '', text).strip()
                if text and 3 <= len(text) <= 60:
                    team_name = text
                    break
    
    # Try link text
    if not team_name:
        link = element.find('a')
        if link:
            text = link.get_text(strip=True)
            text = re.sub(r'[🇦-🇿🏴]+', '', text).strip()
            text = re.sub(r'\([^)]+\)', '', text).strip()
            if text and 3 <= len(text) <= 60:
                team_name = text
    
    # Extract from URL as last resort
    if not team_name and logo_url:
        match = re.search(r'/([^/]+)\.\w+\.png$', logo_url)
        if match:
            slug = match.group(1)
            team_name = slug.replace('-', ' ').title()
    
    if not team_name or len(team_name) < 2:
        return None
    
    # Clean team name
    team_name = re.sub(r'\s+logo\s*$', '', team_name, flags=re.I).strip()
    
    # Get country name
    country = country_slug.replace('-', ' ').title() if country_slug else 'Unknown'
    flag_emoji = get_country_flag_emoji(country_slug) if country_slug else '🏳️'
    
    return {
        'name': team_name,
        'country': country,
        'flagEmoji': flag_emoji,
        'logoUrl': logo_url
    }

def scrape_page(url, processed_teams):
    """Scrape teams from a single page"""
    teams_data = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all images with logos
        all_images = soup.find_all('img', src=True)
        
        for img in all_images:
            img_src = img.get('src') or img.get('data-src') or img.get('data-lazy-src')
            if not img_src or 'assets.football-logos.cc' not in img_src:
                continue
            
            parent = img.find_parent(['div', 'article', 'li', 'a', 'section'])
            if not parent:
                continue
            
            team_data = scrape_team_from_element(parent, url)
            if team_data and team_data['name'] not in processed_teams:
                teams_data.append(team_data)
                processed_teams.add(team_data['name'])
        
        return teams_data
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return []

def get_all_country_urls(base_url):
    """Get all country page URLs from the main page"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(base_url, headers=headers, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        country_urls = set()
        
        # Find all links that look like country pages
        all_links = soup.find_all('a', href=True)
        for link in all_links:
            href = link.get('href', '')
            # Country pages are typically like /england/, /spain/, etc.
            # Exclude team-specific pages and other non-country pages
            if (href.startswith('/') and 
                not href.startswith('//') and
                not href.startswith('/logo') and
                not href.startswith('/?') and
                not href.startswith('/#') and
                not 'http' in href and
                len(href.split('/')) == 3 and  # /country/ format
                href.count('/') == 2):
                country_url = urljoin(base_url, href)
                if country_url != base_url:
                    country_urls.add(country_url)
        
        # Also try to find country links in navigation/filters
        country_links = soup.find_all('a', href=re.compile(r'/[a-z-]+/$', re.I))
        for link in country_links:
            href = link.get('href', '')
            if href and not href.startswith('http'):
                country_url = urljoin(base_url, href)
                if country_url != base_url and country_url.endswith('/'):
                    country_urls.add(country_url)
        
        return sorted(list(country_urls))
    except Exception as e:
        print(f"Error getting country URLs: {e}")
        return []

def scrape_team_logos():
    """Scrape team names and logos from football-logos.cc"""
    base_url = "https://football-logos.cc/"
    teams_data = []
    processed_teams = set()
    
    print("Scraping main page...")
    main_teams = scrape_page(base_url, processed_teams)
    teams_data.extend(main_teams)
    print(f"Found {len(main_teams)} teams on main page")
    
    print("\nGetting all country URLs...")
    country_urls = get_all_country_urls(base_url)
    print(f"Found {len(country_urls)} country pages to scrape")
    
    print("\nScraping country pages...")
    for i, country_url in enumerate(country_urls, 1):
        print(f"[{i}/{len(country_urls)}] Scraping {country_url}...")
        country_teams = scrape_page(country_url, processed_teams)
        teams_data.extend(country_teams)
        print(f"  Found {len(country_teams)} teams (Total: {len(teams_data)})")
        time.sleep(0.5)  # Be polite
        
        # Check for pagination on country pages
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(country_url, headers=headers, timeout=30)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for pagination links
            pagination_links = soup.find_all('a', href=re.compile(r'page|p=\d+', re.I))
            for page_link in pagination_links[:3]:  # Limit to 3 pages per country
                page_url = urljoin(base_url, page_link.get('href'))
                if page_url != country_url:
                    print(f"    Scraping pagination: {page_url}")
                    page_teams = scrape_page(page_url, processed_teams)
                    teams_data.extend(page_teams)
                    print(f"      Found {len(page_teams)} teams")
                    time.sleep(0.3)
        except:
            pass
    
    print(f"\nTotal teams scraped: {len(teams_data)}")
    return teams_data

def save_to_json(teams_data, filename='assets/football_teams.json'):
    """Save scraped data to JSON file"""
    import os
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(teams_data, f, indent=2, ensure_ascii=False)
    print(f"\nData saved to {filename}")

def main():
    print("Starting comprehensive football logos scraper...")
    teams = scrape_team_logos()
    
    if teams:
        save_to_json(teams)
        print(f"\nSuccessfully scraped {len(teams)} teams!")
        print(f"\nTeams by country:")
        from collections import Counter
        countries = Counter([t['country'] for t in teams])
        for country, count in countries.most_common(10):
            print(f"  {country}: {count} teams")
    else:
        print("\nNo teams found.")

if __name__ == "__main__":
    main()

