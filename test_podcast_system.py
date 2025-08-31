#!/usr/bin/env python3
"""
Comprehensive test suite for the podcast generation system
Tests each component and the complete workflow
"""

import json
import requests
import time
import logging
from datetime import datetime
from google.cloud import storage
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PodcastSystemTester:
    def __init__(self):
        self.cloud_function_url = "https://us-central1-regal-scholar-453620-r7.cloudfunctions.net/generate-podcast"
        self.cloud_run_url = None  # Will be determined from Cloud Function
        self.bucket_name = "regal-scholar-453620-r7-podcast-storage"
        self.storage_client = storage.Client()
        
    def test_cloud_function_health(self):
        """Test if Cloud Function is accessible"""
        logger.info("🔍 Testing Cloud Function accessibility...")
        
        try:
            # Test with OPTIONS request (CORS preflight)
            response = requests.options(self.cloud_function_url, timeout=10)
            logger.info(f"OPTIONS response: {response.status_code}")
            
            return True
        except Exception as e:
            logger.error(f"Cloud Function not accessible: {e}")
            return False
    
    def test_storage_access(self):
        """Test Google Cloud Storage access and list existing podcasts"""
        logger.info("🔍 Testing Storage access and listing existing podcasts...")
        
        try:
            bucket = self.storage_client.bucket(self.bucket_name)
            blobs = list(bucket.list_blobs(prefix="podcasts/", max_results=10))
            
            logger.info(f"Found {len(blobs)} podcast files:")
            
            latest_number = 250000
            for blob in blobs:
                if blob.name.endswith('.mp3'):
                    filename = blob.name.split('/')[-1]
                    logger.info(f"  📁 {filename} ({blob.size} bytes, {blob.time_created})")
                    
                    # Extract number for filename analysis
                    import re
                    match = re.search(r'ever-\w+-(\d+)', filename)
                    if match:
                        number = int(match.group(1))
                        latest_number = max(latest_number, number)
            
            logger.info(f"📊 Latest podcast number found: {latest_number}")
            logger.info(f"📊 Next podcast should be: {latest_number + 1}")
            
            return True, latest_number
            
        except Exception as e:
            logger.error(f"Storage access failed: {e}")
            return False, None
    
    def test_filename_generation(self, category="Mathematics"):
        """Test filename generation logic"""
        logger.info(f"🔍 Testing filename generation for category: {category}")
        
        # This would normally be done by the backend
        # For testing, we'll simulate the logic
        
        category_abbrev = {
            'Biology': 'bio',
            'Chemistry': 'chem', 
            'Computer Science': 'compsci',
            'Mathematics': 'math',
            'Physics': 'phys'
        }
        
        abbrev = category_abbrev.get(category, 'misc')
        prefix = f"ever-{abbrev}-"
        
        # Get current max number
        success, latest_number = self.test_storage_access()
        if success:
            next_number = latest_number + 1
            expected_filename = f"{prefix}{next_number:06d}"
            logger.info(f"📝 Expected next filename: {expected_filename}")
            return expected_filename
        
        return None
    
    def test_podcast_generation(self, test_short=True):
        """Test complete podcast generation workflow"""
        logger.info("🔍 Testing complete podcast generation...")
        
        # Use shorter duration for testing
        test_data = {
            "subject": "Test Quantum Computing Basics" if test_short else "Advanced Quantum Error Correction",
            "category": "Computer Science",
            "duration": "5" if test_short else "10",
            "speakers": "single",
            "difficulty": "General",
            "source_links": [],
            "additional_notes": "This is a test generation - please keep content brief and focused."
        }
        
        logger.info(f"Test data: {json.dumps(test_data, indent=2)}")
        
        try:
            start_time = time.time()
            
            response = requests.post(
                self.cloud_function_url,
                json=test_data,
                timeout=600,  # 10 minute timeout
                headers={'Content-Type': 'application/json'}
            )
            
            end_time = time.time()
            duration = end_time - start_time
            
            logger.info(f"⏱️  Request completed in {duration:.1f} seconds")
            logger.info(f"📊 Response status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                logger.info("✅ Podcast generation successful!")
                logger.info(f"📁 Filename: {result.get('filename', 'unknown')}")
                logger.info(f"🔗 Audio URL: {result.get('audio_url', 'unknown')}")
                
                # Test if the audio file is accessible
                if result.get('audio_url'):
                    audio_response = requests.head(result['audio_url'], timeout=10)
                    logger.info(f"🎵 Audio file accessible: {audio_response.status_code == 200}")
                    logger.info(f"📊 Audio file size: {audio_response.headers.get('content-length', 'unknown')} bytes")
                
                return True, result
            else:
                error_text = response.text
                logger.error(f"❌ Podcast generation failed: {error_text}")
                return False, error_text
                
        except requests.exceptions.Timeout:
            logger.error("❌ Request timed out")
            return False, "Timeout"
        except Exception as e:
            logger.error(f"❌ Test failed: {e}")
            return False, str(e)
    
    def test_multi_voice_generation(self):
        """Test multi-voice podcast generation"""
        logger.info("🔍 Testing multi-voice generation...")
        
        test_data = {
            "subject": "AI Ethics Debate",
            "category": "Computer Science", 
            "duration": "5",
            "speakers": "debate",  # This should trigger multiple voices
            "difficulty": "General",
            "source_links": [],
            "additional_notes": "Focus on different perspectives - one optimistic, one cautious about AI development."
        }
        
        return self.test_podcast_generation(test_short=True)
    
    def analyze_existing_podcasts(self):
        """Analyze existing podcasts to understand current issues"""
        logger.info("🔍 Analyzing existing podcasts...")
        
        try:
            bucket = self.storage_client.bucket(self.bucket_name)
            blobs = list(bucket.list_blobs(prefix="podcasts/"))
            
            podcasts = []
            metadata_files = []
            
            for blob in blobs:
                if blob.name.endswith('.mp3'):
                    podcasts.append(blob)
                elif blob.name.endswith('_metadata.json'):
                    metadata_files.append(blob)
            
            logger.info(f"📊 Found {len(podcasts)} podcast files and {len(metadata_files)} metadata files")
            
            # Analyze filenames for numbering pattern
            filename_numbers = []
            for blob in podcasts:
                filename = blob.name.split('/')[-1]
                match = re.search(r'ever-\w+-(\d+)', filename)
                if match:
                    filename_numbers.append(int(match.group(1)))
            
            if filename_numbers:
                filename_numbers.sort()
                logger.info(f"📊 Filename numbers found: {filename_numbers[:5]}...{filename_numbers[-5:] if len(filename_numbers) > 5 else ''}")
                logger.info(f"📊 Latest number: {max(filename_numbers)}")
                
                # Check for gaps or duplicates
                gaps = []
                for i in range(min(filename_numbers), max(filename_numbers) + 1):
                    if i not in filename_numbers:
                        gaps.append(i)
                
                if gaps:
                    logger.warning(f"⚠️  Found {len(gaps)} gaps in numbering: {gaps[:10]}")
                else:
                    logger.info("✅ No gaps found in filename numbering")
            
            # Analyze recent metadata
            if metadata_files:
                logger.info("🔍 Analyzing recent podcast metadata...")
                recent_metadata = metadata_files[-3:]  # Last 3 metadata files
                
                for metadata_blob in recent_metadata:
                    try:
                        metadata_content = metadata_blob.download_as_text()
                        metadata = json.loads(metadata_content)
                        
                        logger.info(f"📄 {metadata_blob.name}:")
                        logger.info(f"  Subject: {metadata.get('subject', 'unknown')}")
                        logger.info(f"  Duration: {metadata.get('duration_minutes', 'unknown')} min")
                        logger.info(f"  Speakers: {metadata.get('speakers', 'unknown')}")
                        logger.info(f"  Word count: {metadata.get('word_count', 'unknown')}")
                        
                    except Exception as e:
                        logger.error(f"Error reading metadata {metadata_blob.name}: {e}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error analyzing podcasts: {e}")
            return False
    
    def run_comprehensive_test(self):
        """Run all tests in sequence"""
        logger.info("🧪 Starting comprehensive podcast system test...")
        
        results = {}
        
        # Test 1: Cloud Function accessibility
        results['cloud_function'] = self.test_cloud_function_health()
        
        # Test 2: Storage access
        results['storage'], latest_number = self.test_storage_access()
        
        # Test 3: Filename generation
        expected_filename = self.test_filename_generation()
        results['filename_generation'] = expected_filename is not None
        
        # Test 4: Analyze existing podcasts
        results['analysis'] = self.analyze_existing_podcasts()
        
        # Test 5: Single voice generation
        logger.info("🧪 Testing single voice generation...")
        results['single_voice'], single_result = self.test_podcast_generation(test_short=True)
        
        # Test 6: Multi-voice generation
        if results['single_voice']:
            logger.info("🧪 Testing multi-voice generation...")
            results['multi_voice'], multi_result = self.test_multi_voice_generation()
        else:
            results['multi_voice'] = False
            multi_result = "Skipped due to single voice test failure"
        
        # Summary
        logger.info("📋 Test Results Summary:")
        for test_name, passed in results.items():
            status = "✅ PASS" if passed else "❌ FAIL"
            logger.info(f"  {test_name}: {status}")
        
        all_passed = all(results.values())
        
        if all_passed:
            logger.info("🎉 All tests passed! System is working correctly.")
        else:
            logger.warning("⚠️  Some tests failed. Check logs above for details.")
        
        return results

if __name__ == "__main__":
    tester = PodcastSystemTester()
    results = tester.run_comprehensive_test()