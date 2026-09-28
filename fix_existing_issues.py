#!/usr/bin/env python3
"""
Fix existing issues in the podcast generation system
Addresses filename numbering, metadata, and RSS feed problems
"""

import json
import logging
import re
from datetime import datetime, timedelta
from google.cloud import storage
from typing import Dict, List, Any
import xml.etree.ElementTree as ET
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PodcastFixer:
    def __init__(self):
        self.bucket_name = "regal-scholar-453620-r7-podcast-storage"
        self.storage_client = storage.Client()
        self.bucket = self.storage_client.bucket(self.bucket_name)
    
    def analyze_filename_issues(self):
        """Analyze and report filename numbering issues"""
        logger.info("🔍 Analyzing filename numbering issues...")
        
        try:
            blobs = list(self.bucket.list_blobs(prefix="podcasts/"))
            mp3_files = [blob for blob in blobs if blob.name.endswith('.mp3')]
            
            # Extract numbers from filenames
            filename_data = []
            for blob in mp3_files:
                filename = blob.name.split('/')[-1]
                match = re.search(r'ever-(\w+)-(\d+)', filename)
                if match:
                    category = match.group(1)
                    number = int(match.group(2))
                    filename_data.append({
                        'filename': filename,
                        'category': category,
                        'number': number,
                        'blob': blob
                    })
            
            # Sort by number
            filename_data.sort(key=lambda x: x['number'])
            
            logger.info(f"📊 Found {len(filename_data)} numbered podcast files")
            
            # Check for duplicates
            numbers = [item['number'] for item in filename_data]
            duplicates = []
            for i, num in enumerate(numbers):
                if numbers.count(num) > 1 and num not in duplicates:
                    duplicates.append(num)
            
            if duplicates:
                logger.warning(f"⚠️  Found duplicate numbers: {duplicates}")
                
                # Show duplicate files
                for dup_num in duplicates:
                    dup_files = [item for item in filename_data if item['number'] == dup_num]
                    logger.warning(f"  Number {dup_num}:")
                    for item in dup_files:
                        logger.warning(f"    - {item['filename']} ({item['blob'].time_created})")
            else:
                logger.info("✅ No duplicate numbers found")
            
            # Check for gaps
            if filename_data:
                min_num = min(numbers)
                max_num = max(numbers)
                expected_numbers = set(range(min_num, max_num + 1))
                actual_numbers = set(numbers)
                gaps = expected_numbers - actual_numbers
                
                if gaps:
                    logger.warning(f"⚠️  Found {len(gaps)} gaps in numbering: {sorted(list(gaps))[:10]}")
                else:
                    logger.info("✅ No gaps found in filename numbering")
            
            return filename_data
            
        except Exception as e:
            logger.error(f"Error analyzing filenames: {e}")
            return []
    
    def fix_rss_feed_dates(self):
        """Fix future dates in RSS feed"""
        logger.info("🔍 Fixing RSS feed dates...")
        
        try:
            # Download current RSS feed
            feed_url = f"https://storage.googleapis.com/{self.bucket_name}/feeds/copernicus-mvp-rss-feed.xml"
            response = requests.get(feed_url, timeout=30)
            
            if response.status_code != 200:
                logger.error(f"Cannot download RSS feed: {response.status_code}")
                return False
            
            # Parse XML
            root = ET.fromstring(response.content)
            
            # Find all items with future dates
            items = root.findall('.//item')
            logger.info(f"Found {len(items)} episodes in RSS feed")
            
            # Fix dates
            base_date = datetime.now() - timedelta(days=len(items) * 7)  # Start weeks ago
            fixed_count = 0
            
            for i, item in enumerate(items):
                pub_date_elem = item.find('pubDate')
                if pub_date_elem is not None:
                    old_date = pub_date_elem.text
                    
                    # Check if date is in the future
                    if '2025' in old_date or datetime.strptime(old_date, "%a, %d %b %Y %H:%M:%S GMT") > datetime.now():
                        new_date = base_date + timedelta(days=i * 7)
                        pub_date_elem.text = new_date.strftime("%a, %d %b %Y %H:%M:%S GMT")
                        logger.info(f"Fixed episode {i+1}: {old_date} → {pub_date_elem.text}")
                        fixed_count += 1
            
            if fixed_count > 0:
                # Save fixed feed
                ET.register_namespace('itunes', 'http://www.itunes.com/dtds/podcast-1.0.dtd')
                ET.register_namespace('atom', 'http://www.w3.org/2005/Atom')
                ET.register_namespace('podcast', 'https://podcastindex.org/namespace/1.0')
                
                tree = ET.ElementTree(root)
                tree.write('fixed_rss_feed.xml', encoding='utf-8', xml_declaration=True)
                
                logger.info(f"✅ Fixed {fixed_count} episode dates")
                logger.info("📁 Fixed feed saved as: fixed_rss_feed.xml")
                logger.info("🔧 Upload this file to replace the current RSS feed")
                return True
            else:
                logger.info("✅ No date fixes needed")
                return True
                
        except Exception as e:
            logger.error(f"Error fixing RSS feed: {e}")
            return False
    
    def create_deployment_checklist(self):
        """Create a deployment checklist to ensure all issues are addressed"""
        checklist = """
# 🚀 Podcast System Deployment Checklist

## Pre-Deployment Checks
- [ ] OpenAI API key is set in Cloud Run environment
- [ ] Google Cloud credentials are properly configured
- [ ] Storage bucket permissions are correct
- [ ] Text-to-Speech API is enabled

## Deployment Steps
1. [ ] Deploy Cloud Run backend: `bash deploy_backend.sh`
2. [ ] Update Cloud Function with Cloud Run URL
3. [ ] Deploy Cloud Function: `bash deploy_function.sh`
4. [ ] Test with: `python test_podcast_system.py`

## Issue Fixes Implemented
- [x] **Filename numbering**: Proper incremental numbering with collision detection
- [x] **Multi-voice audio**: Distinct voices for different speakers using Google TTS
- [x] **Duration targeting**: Word count calculation and content length adjustment
- [x] **Comprehensive logging**: Detailed logging at every step
- [x] **Error handling**: Robust error handling and recovery
- [x] **Endpoint consolidation**: Single clear endpoint with legacy redirect

## Post-Deployment Verification
- [ ] Generate test podcast with single voice
- [ ] Generate test podcast with multiple voices
- [ ] Verify filename increments correctly
- [ ] Check audio duration matches request
- [ ] Verify different voices are used
- [ ] Test error handling with invalid inputs

## RSS Feed Fixes
- [ ] Run `python fix_existing_issues.py` to fix date issues
- [ ] Upload fixed RSS feed to replace current version
- [ ] Verify feed validates correctly
- [ ] Resubmit to podcast platforms

## Monitoring Setup
- [ ] Configure Cloud Logging alerts
- [ ] Set up uptime monitoring
- [ ] Create dashboard for podcast generation metrics
- [ ] Set up error rate alerting

## Success Criteria
- ✅ Podcasts generate with correct incremental filenames
- ✅ Multi-voice podcasts have distinct speakers
- ✅ Duration matches user request (±1 minute tolerance)
- ✅ All components log properly for debugging
- ✅ RSS feed has valid dates and metadata
- ✅ System handles errors gracefully
"""
        
        with open('deployment_checklist.md', 'w') as f:
            f.write(checklist)
        
        logger.info("📋 Deployment checklist created: deployment_checklist.md")
    
    def run_complete_fix(self):
        """Run all fixes and analysis"""
        logger.info("🔧 Running complete podcast system analysis and fixes...")
        
        # 1. Analyze current state
        filename_data = self.analyze_filename_issues()
        
        # 2. Fix RSS feed dates
        rss_fixed = self.fix_rss_feed_dates()
        
        # 3. Create deployment checklist
        self.create_deployment_checklist()
        
        # 4. Summary
        logger.info("📋 Fix Summary:")
        logger.info(f"  📁 Analyzed {len(filename_data)} podcast files")
        logger.info(f"  📅 RSS feed dates: {'✅ Fixed' if rss_fixed else '❌ Needs attention'}")
        logger.info(f"  📋 Deployment checklist: ✅ Created")
        
        logger.info("\n🚀 Next Steps:")
        logger.info("1. Review deployment_checklist.md")
        logger.info("2. Deploy the new backend: bash deploy_backend.sh")
        logger.info("3. Test the system: python test_podcast_system.py")
        
        return True

if __name__ == "__main__":
    import re
    
    fixer = PodcastFixer()
    fixer.run_complete_fix()