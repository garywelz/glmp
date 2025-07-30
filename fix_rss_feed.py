#!/usr/bin/env python3
"""
RSS Feed Fixer for Copernicus AI Podcast
Fixes common issues that prevent podcast platforms from accepting the feed:
1. Future publication dates
2. File size mismatches in enclosure tags
3. Excessive HTML in descriptions
4. Hashtag formatting issues
"""

import xml.etree.ElementTree as ET
import requests
import re
from datetime import datetime, timedelta
from urllib.parse import urlparse
import html
import sys
import os


def get_file_size(url):
    """Get the actual file size from HTTP headers"""
    try:
        response = requests.head(url, timeout=10)
        if response.status_code == 200:
            content_length = response.headers.get('content-length')
            if content_length:
                return int(content_length)
    except Exception as e:
        print(f"Warning: Could not get file size for {url}: {e}")
    return None


def clean_html_description(description):
    """Clean excessive HTML from descriptions while preserving basic formatting"""
    if not description:
        return description
    
    # Unescape HTML entities first
    cleaned = html.unescape(description)
    
    # Remove complex HTML tags but keep basic ones
    # Remove h1, h2, h3 tags but keep their content
    cleaned = re.sub(r'</?h[1-6][^>]*>', '', cleaned)
    
    # Convert lists to simple text format
    # Handle ordered lists
    cleaned = re.sub(r'<ol[^>]*>', '\n', cleaned)
    cleaned = re.sub(r'</ol>', '\n', cleaned)
    cleaned = re.sub(r'<li[^>]*>', '• ', cleaned)
    cleaned = re.sub(r'</li>', '\n', cleaned)
    
    # Handle unordered lists
    cleaned = re.sub(r'<ul[^>]*>', '\n', cleaned)
    cleaned = re.sub(r'</ul>', '\n', cleaned)
    
    # Keep basic formatting tags
    # Keep <p>, <br>, <strong>, <em>, <a>
    # Remove everything else
    allowed_tags = ['p', 'br', 'strong', 'em', 'a']
    
    # Remove all other HTML tags except allowed ones
    def replace_tags(match):
        tag = match.group(1).lower().split()[0]
        if tag in allowed_tags or tag.startswith('/') and tag[1:] in allowed_tags:
            return match.group(0)
        return ''
    
    cleaned = re.sub(r'<(/?\w+)[^>]*>', replace_tags, cleaned)
    
    # Clean up multiple newlines
    cleaned = re.sub(r'\n\s*\n\s*\n+', '\n\n', cleaned)
    
    # Remove leading/trailing whitespace
    cleaned = cleaned.strip()
    
    # Truncate if too long (Apple Podcasts has 4000 char limit)
    if len(cleaned) > 3800:  # Leave some buffer
        cleaned = cleaned[:3800] + "..."
    
    return cleaned


def fix_hashtags(description):
    """Convert h1 hashtag sections to simple text"""
    if not description:
        return description
    
    # Find hashtag sections (usually at the end in h1 tags)
    hashtag_pattern = r'<h1[^>]*>(.*?#.*?)</h1>'
    
    def replace_hashtag_section(match):
        content = match.group(1)
        # Remove any remaining HTML
        content = re.sub(r'<[^>]+>', '', content)
        # Clean up spacing
        content = re.sub(r'\s+', ' ', content)
        return f"\n\nTags: {content.strip()}"
    
    return re.sub(hashtag_pattern, replace_hashtag_section, description, flags=re.IGNORECASE | re.DOTALL)


def generate_past_date(episode_number, total_episodes):
    """Generate a realistic past publication date"""
    # Start from 3 months ago and space episodes weekly
    base_date = datetime.now() - timedelta(days=90)
    episode_date = base_date + timedelta(days=episode_number * 7)
    
    # Format as RFC 822
    return episode_date.strftime("%a, %d %b %Y %H:%M:%S GMT")


def fix_rss_feed(input_file, output_file):
    """Main function to fix all RSS feed issues"""
    print("Starting RSS feed repair...")
    
    # Parse the XML
    try:
        tree = ET.parse(input_file)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        return False
    
    # Find all item elements (episodes)
    items = root.findall('.//item')
    total_episodes = len(items)
    print(f"Found {total_episodes} episodes to process")
    
    fixed_issues = {
        'dates': 0,
        'file_sizes': 0,
        'descriptions': 0,
        'hashtags': 0
    }
    
    for i, item in enumerate(items):
        episode_num = i + 1
        print(f"Processing episode {episode_num}/{total_episodes}...")
        
        # Fix publication date
        pub_date = item.find('pubDate')
        if pub_date is not None:
            current_date = pub_date.text
            if '2025' in current_date:  # Future date
                new_date = generate_past_date(i, total_episodes)
                pub_date.text = new_date
                fixed_issues['dates'] += 1
                print(f"  ✓ Fixed publication date: {current_date} → {new_date}")
        
        # Fix file size in enclosure
        enclosure = item.find('enclosure')
        if enclosure is not None:
            url = enclosure.get('url')
            current_length = enclosure.get('length')
            
            if url:
                actual_size = get_file_size(url)
                if actual_size and current_length and str(actual_size) != current_length:
                    enclosure.set('length', str(actual_size))
                    fixed_issues['file_sizes'] += 1
                    print(f"  ✓ Fixed file size: {current_length} → {actual_size}")
        
        # Fix description
        description = item.find('description')
        if description is not None and description.text:
            original_desc = description.text
            
            # Fix hashtags first
            fixed_hashtags = fix_hashtags(original_desc)
            if fixed_hashtags != original_desc:
                fixed_issues['hashtags'] += 1
                print("  ✓ Fixed hashtag formatting")
            
            # Clean HTML
            cleaned_desc = clean_html_description(fixed_hashtags)
            if cleaned_desc != original_desc:
                description.text = cleaned_desc
                fixed_issues['descriptions'] += 1
                print("  ✓ Cleaned HTML description")
        
        # Also fix content:encoded if present
        content_encoded = item.find('{http://purl.org/rss/1.0/modules/content/}encoded')
        if content_encoded is not None and content_encoded.text:
            original_content = content_encoded.text
            fixed_hashtags = fix_hashtags(original_content)
            cleaned_content = clean_html_description(fixed_hashtags)
            if cleaned_content != original_content:
                content_encoded.text = cleaned_content
                print("  ✓ Cleaned content:encoded")
    
    # Write the fixed XML
    # Register namespaces to preserve them
    ET.register_namespace('itunes', 'http://www.itunes.com/dtds/podcast-1.0.dtd')
    ET.register_namespace('atom', 'http://www.w3.org/2005/Atom')
    ET.register_namespace('podcast', 'https://podcastindex.org/namespace/1.0')
    ET.register_namespace('content', 'http://purl.org/rss/1.0/modules/content/')
    ET.register_namespace('media', 'http://search.yahoo.com/mrss/')
    
    tree.write(output_file, encoding='utf-8', xml_declaration=True)
    
    print("\n" + "="*50)
    print("RSS FEED REPAIR COMPLETED!")
    print("="*50)
    print(f"Fixed {fixed_issues['dates']} publication dates")
    print(f"Fixed {fixed_issues['file_sizes']} file size mismatches")
    print(f"Cleaned {fixed_issues['descriptions']} episode descriptions")
    print(f"Fixed {fixed_issues['hashtags']} hashtag formatting issues")
    print(f"\nFixed feed saved to: {output_file}")
    print("\nNext steps:")
    print("1. Upload the fixed RSS feed to your Google Cloud Storage")
    print("2. Wait 24-48 hours for platforms to re-crawl")
    print("3. Try resubmitting to Spotify, YouTube, and Apple Podcasts")
    
    return True


def validate_feed_url(url):
    """Basic validation that the feed URL is accessible"""
    try:
        response = requests.get(url, timeout=10)
        return response.status_code == 200
    except:
        return False


def main():
    """Main entry point"""
    print("Copernicus AI Podcast RSS Feed Fixer")
    print("="*40)
    
    # Default URLs and files
    feed_url = "https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/feeds/copernicus-mvp-rss-feed.xml"
    input_file = "original_rss_feed.xml"
    output_file = "fixed_rss_feed.xml"
    
    # Download the current feed
    print(f"Downloading RSS feed from: {feed_url}")
    
    if not validate_feed_url(feed_url):
        print("Error: Could not access the RSS feed URL")
        return
    
    try:
        response = requests.get(feed_url)
        response.raise_for_status()
        
        with open(input_file, 'wb') as f:
            f.write(response.content)
        
        print(f"✓ Feed downloaded to: {input_file}")
        
    except Exception as e:
        print(f"Error downloading feed: {e}")
        return
    
    # Fix the feed
    success = fix_rss_feed(input_file, output_file)
    
    if success:
        print(f"\n✓ Success! Your fixed RSS feed is ready: {output_file}")
        print("\nTo use the fixed feed:")
        print("1. Upload 'fixed_rss_feed.xml' to replace your current feed")
        print("2. Update the file at the same URL in Google Cloud Storage")
        print("3. Test the feed URL in a browser to ensure it loads")
        print("4. Resubmit to podcast platforms")
        
        # Cleanup
        if os.path.exists(input_file):
            os.remove(input_file)
            print(f"\n✓ Cleaned up temporary file: {input_file}")
    
    else:
        print("\n✗ Failed to fix RSS feed. Please check the error messages above.")


if __name__ == "__main__":
    main()