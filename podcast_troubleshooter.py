#!/usr/bin/env python3
"""
Comprehensive Podcast RSS Feed Troubleshooter
Diagnoses why your podcast isn't being accepted by major platforms
Provides specific actionable fixes and platform requirements
"""

import xml.etree.ElementTree as ET
import requests
import re
from datetime import datetime, timedelta
from urllib.parse import urlparse
import html
import sys
import os
import json


class PodcastTroubleshooter:
    def __init__(self, feed_url):
        self.feed_url = feed_url
        self.issues = []
        self.warnings = []
        self.feed_content = None
        self.root = None
        
    def download_feed(self):
        """Download and parse the RSS feed"""
        try:
            print(f"🔍 Downloading feed from: {self.feed_url}")
            response = requests.get(self.feed_url, timeout=30)
            response.raise_for_status()
            
            self.feed_content = response.text
            self.root = ET.fromstring(response.content)
            print("✅ Feed downloaded and parsed successfully")
            return True
            
        except requests.RequestException as e:
            self.issues.append(f"❌ CRITICAL: Cannot download feed - {e}")
            return False
        except ET.ParseError as e:
            self.issues.append(f"❌ CRITICAL: Invalid XML format - {e}")
            return False

    def check_basic_accessibility(self):
        """Check if feed is publicly accessible"""
        print("\n🔍 Testing Feed Accessibility...")
        
        # Test HTTP headers
        try:
            response = requests.head(self.feed_url, timeout=10)
            content_type = response.headers.get('content-type', '')
            
            if 'xml' not in content_type.lower() and 'rss' not in content_type.lower():
                self.warnings.append(f"⚠️  Content-Type is '{content_type}' - should be 'application/rss+xml' or 'application/xml'")
            
            if response.status_code != 200:
                self.issues.append(f"❌ CRITICAL: Feed returns HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.issues.append(f"❌ CRITICAL: Feed not accessible - {e}")
            return False
            
        return True

    def check_future_dates(self):
        """Check for future publication dates"""
        print("🔍 Checking publication dates...")
        
        current_date = datetime.now()
        future_dates = 0
        
        for item in self.root.findall('.//item'):
            pub_date = item.find('pubDate')
            if pub_date is not None:
                date_str = pub_date.text
                if '2025' in date_str:
                    # Try to parse the date
                    try:
                        episode_date = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %Z")
                        if episode_date > current_date:
                            future_dates += 1
                    except:
                        # If we can't parse, assume it's future if it contains 2025
                        future_dates += 1
        
        if future_dates > 0:
            self.issues.append(f"❌ CRITICAL: {future_dates} episodes have future publication dates (2025)")
            self.issues.append("   📋 FIX: Change all episode dates to past dates")
        else:
            print("✅ All episodes have valid past publication dates")

    def check_file_accessibility(self):
        """Check if audio files are accessible"""
        print("🔍 Testing audio file accessibility...")
        
        inaccessible_files = 0
        size_mismatches = 0
        
        for i, item in enumerate(self.root.findall('.//item')[:3]):  # Check first 3 episodes
            enclosure = item.find('enclosure')
            if enclosure is not None:
                url = enclosure.get('url')
                claimed_length = enclosure.get('length')
                
                if url:
                    try:
                        response = requests.head(url, timeout=15)
                        if response.status_code != 200:
                            inaccessible_files += 1
                            self.issues.append(f"❌ Audio file not accessible: {url} (HTTP {response.status_code})")
                        else:
                            # Check file size
                            actual_length = response.headers.get('content-length')
                            if actual_length and claimed_length:
                                if abs(int(actual_length) - int(claimed_length)) > 1000:  # Allow 1KB difference
                                    size_mismatches += 1
                                    self.issues.append(f"❌ File size mismatch: Claimed {claimed_length}, Actual {actual_length}")
                    except Exception as e:
                        inaccessible_files += 1
                        self.issues.append(f"❌ Cannot access audio file: {url} - {e}")
        
        if inaccessible_files == 0 and size_mismatches == 0:
            print("✅ Audio files are accessible with correct sizes")

    def check_required_elements(self):
        """Check for required RSS elements"""
        print("🔍 Checking required RSS elements...")
        
        # Channel level requirements
        channel = self.root.find('.//channel')
        required_channel_elements = {
            'title': 'Podcast title',
            'description': 'Podcast description',
            'link': 'Podcast homepage URL'
        }
        
        for element, description in required_channel_elements.items():
            if channel.find(element) is None:
                self.issues.append(f"❌ CRITICAL: Missing required element: <{element}> ({description})")
        
        # iTunes specific requirements
        itunes_required = {
            '{http://www.itunes.com/dtds/podcast-1.0.dtd}owner': 'iTunes owner information',
            '{http://www.itunes.com/dtds/podcast-1.0.dtd}image': 'iTunes podcast image',
            '{http://www.itunes.com/dtds/podcast-1.0.dtd}author': 'iTunes author'
        }
        
        for element, description in itunes_required.items():
            if channel.find(element) is None:
                self.issues.append(f"❌ CRITICAL: Missing iTunes element: {element.split('}')[1]} ({description})")
        
        # Check episodes have required elements
        items = self.root.findall('.//item')
        if len(items) == 0:
            self.issues.append("❌ CRITICAL: No episodes found in feed")
        else:
            print(f"✅ Found {len(items)} episodes")
            
            # Check first episode for required elements
            first_item = items[0]
            required_item_elements = ['title', 'enclosure', 'guid']
            
            for element in required_item_elements:
                if first_item.find(element) is None:
                    self.issues.append(f"❌ CRITICAL: Episode missing required element: <{element}>")

    def check_image_requirements(self):
        """Check podcast artwork requirements"""
        print("🔍 Checking podcast artwork...")
        
        channel = self.root.find('.//channel')
        itunes_image = channel.find('{http://www.itunes.com/dtds/podcast-1.0.dtd}image')
        
        if itunes_image is not None:
            image_url = itunes_image.get('href')
            if image_url:
                try:
                    response = requests.head(image_url, timeout=10)
                    if response.status_code != 200:
                        self.issues.append(f"❌ Podcast artwork not accessible: {image_url}")
                    else:
                        print("✅ Podcast artwork is accessible")
                except Exception as e:
                    self.issues.append(f"❌ Cannot access podcast artwork: {e}")

    def check_description_issues(self):
        """Check for description formatting issues"""
        print("🔍 Checking episode descriptions...")
        
        html_issues = 0
        excessive_length = 0
        
        for item in self.root.findall('.//item'):
            description = item.find('description')
            if description is not None and description.text:
                desc_text = description.text
                
                # Check for excessive HTML
                if desc_text.count('<') > 10:  # Arbitrary threshold
                    html_issues += 1
                
                # Check length (Apple has 4000 char limit)
                if len(desc_text) > 4000:
                    excessive_length += 1
        
        if html_issues > 0:
            self.warnings.append(f"⚠️  {html_issues} episodes have complex HTML in descriptions")
        
        if excessive_length > 0:
            self.warnings.append(f"⚠️  {excessive_length} episodes have descriptions longer than 4000 characters")

    def check_platform_specific_issues(self):
        """Check for platform-specific issues"""
        print("🔍 Checking platform-specific requirements...")
        
        # Spotify specific checks
        owner_email = self.root.find('.//{http://www.itunes.com/dtds/podcast-1.0.dtd}owner/{http://www.itunes.com/dtds/podcast-1.0.dtd}email')
        if owner_email is None:
            self.issues.append("❌ SPOTIFY: Missing owner email for verification")
        
        # YouTube specific checks
        items = self.root.findall('.//item')
        if len(items) > 500:
            self.warnings.append("⚠️  YOUTUBE: More than 500 episodes may cause issues with RSS upload")
        
        # Apple Podcasts specific checks
        explicit = self.root.find('.//{http://www.itunes.com/dtds/podcast-1.0.dtd}explicit')
        if explicit is None:
            self.warnings.append("⚠️  APPLE: Missing explicit content tag")

    def generate_platform_instructions(self):
        """Generate platform-specific submission instructions"""
        print("\n" + "="*60)
        print("📋 PLATFORM SUBMISSION INSTRUCTIONS")
        print("="*60)
        
        print("\n🎵 SPOTIFY FOR CREATORS:")
        print("1. Go to: https://creators.spotify.com/")
        print("2. Sign in with your Spotify account")
        print("3. Click 'Add your podcast'")
        print("4. Enter your RSS feed URL:")
        print(f"   {self.feed_url}")
        print("5. Spotify will send verification email to: garywelz@gmail.com")
        print("6. Check email and verify ownership")
        print("7. Wait 24-48 hours for review")
        
        print("\n📺 YOUTUBE:")
        print("1. Go to: https://studio.youtube.com/")
        print("2. Sign in to YouTube Studio")
        print("3. Click 'Content' → 'Podcasts'")
        print("4. Click 'New' → 'Upload podcast via RSS'")
        print("5. Enter your RSS feed URL:")
        print(f"   {self.feed_url}")
        print("6. Verify email ownership (garywelz@gmail.com)")
        print("7. Select episodes to upload")
        print("8. Set visibility to 'Public' when ready")
        
        print("\n🍎 APPLE PODCASTS:")
        print("1. Go to: https://podcastsconnect.apple.com/")
        print("2. Sign in with your Apple ID")
        print("3. Click '+' to add a new show")
        print("4. Enter your RSS feed URL:")
        print(f"   {self.feed_url}")
        print("5. Fill out show information")
        print("6. Submit for review")
        print("7. Wait 24-72 hours for approval")

    def generate_fix_script(self):
        """Generate a script to fix the identified issues"""
        print("\n" + "="*60)
        print("🔧 AUTOMATED FIX SCRIPT")
        print("="*60)
        
        if any("future publication dates" in issue for issue in self.issues):
            print("\n⚠️  CRITICAL ISSUE DETECTED: Future publication dates")
            print("Run the RSS fixer script to resolve this automatically:")
            print("\nCopy and paste this into a new file called 'fix_dates.py':")
            print("-" * 50)
            
            fix_script = '''import xml.etree.ElementTree as ET
import requests
from datetime import datetime, timedelta

def fix_feed_dates():
    # Download current feed
    url = "''' + self.feed_url + '''"
    response = requests.get(url)
    
    # Parse XML
    root = ET.fromstring(response.content)
    
    # Fix dates
    items = root.findall('.//item')
    base_date = datetime.now() - timedelta(days=len(items) * 7)  # Start weeks ago
    
    for i, item in enumerate(items):
        pub_date = item.find('pubDate')
        if pub_date is not None and '2025' in pub_date.text:
            new_date = base_date + timedelta(days=i * 7)
            pub_date.text = new_date.strftime("%a, %d %b %Y %H:%M:%S GMT")
            print(f"Fixed episode {i+1} date")
    
    # Save fixed feed
    tree = ET.ElementTree(root)
    tree.write('fixed_feed.xml', encoding='utf-8', xml_declaration=True)
    print("Fixed feed saved as 'fixed_feed.xml'")
    print("Upload this file to replace your current RSS feed")

if __name__ == "__main__":
    fix_feed_dates()'''
            
            print(fix_script)
            print("-" * 50)
            print("\nThen run: python fix_dates.py")

    def run_full_diagnosis(self):
        """Run complete diagnostic check"""
        print("🚀 Starting comprehensive podcast feed diagnosis...")
        print("="*60)
        
        # Step 1: Download feed
        if not self.download_feed():
            return False
        
        # Step 2: Check accessibility
        if not self.check_basic_accessibility():
            return False
        
        # Step 3: Run all checks
        self.check_future_dates()
        self.check_file_accessibility()
        self.check_required_elements()
        self.check_image_requirements()
        self.check_description_issues()
        self.check_platform_specific_issues()
        
        # Step 4: Report results
        self.print_results()
        
        # Step 5: Provide instructions
        self.generate_platform_instructions()
        
        # Step 6: Generate fix script if needed
        if self.issues:
            self.generate_fix_script()
        
        return True

    def print_results(self):
        """Print diagnostic results"""
        print("\n" + "="*60)
        print("📊 DIAGNOSTIC RESULTS")
        print("="*60)
        
        if not self.issues and not self.warnings:
            print("🎉 EXCELLENT! Your RSS feed appears to be properly formatted!")
            print("If platforms are still rejecting it, try:")
            print("1. Wait 24-48 hours and resubmit")
            print("2. Contact platform support directly")
            print("3. Check if your account has any restrictions")
            return
        
        if self.issues:
            print(f"\n❌ CRITICAL ISSUES FOUND ({len(self.issues)}):")
            print("These MUST be fixed before platforms will accept your feed:")
            for issue in self.issues:
                print(f"   {issue}")
        
        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            print("These should be addressed for best compatibility:")
            for warning in self.warnings:
                print(f"   {warning}")
        
        print(f"\n🔧 PRIORITY ACTION ITEMS:")
        print("1. Fix all CRITICAL issues above")
        print("2. Test feed URL in browser to ensure it loads")
        print("3. Wait 24-48 hours after fixes before resubmitting")
        print("4. Use platform-specific submission instructions below")


def main():
    """Main entry point"""
    feed_url = "https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/feeds/copernicus-mvp-rss-feed.xml"
    
    troubleshooter = PodcastTroubleshooter(feed_url)
    troubleshooter.run_full_diagnosis()


if __name__ == "__main__":
    main()