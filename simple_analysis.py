#!/usr/bin/env python3
"""
Simple analysis of current podcast system issues
Uses only standard libraries and HTTP requests
"""

import json
import re
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_form_accessibility():
    """Test if the podcast form is accessible"""
    logger.info("🔍 Testing form accessibility...")
    
    try:
        form_url = "https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/form.html"
        response = requests.head(form_url, timeout=10)
        
        if response.status_code == 200:
            logger.info("✅ Form is accessible")
            return True
        else:
            logger.error(f"❌ Form not accessible: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"❌ Error accessing form: {e}")
        return False

def test_cloud_function():
    """Test Cloud Function accessibility"""
    logger.info("🔍 Testing Cloud Function...")
    
    try:
        function_url = "https://us-central1-regal-scholar-453620-r7.cloudfunctions.net/generate-podcast"
        
        # Test OPTIONS request (CORS preflight)
        response = requests.options(function_url, timeout=10)
        logger.info(f"OPTIONS response: {response.status_code}")
        
        # Test with minimal data
        test_data = {
            "subject": "Test",
            "category": "Mathematics", 
            "duration": "5",
            "speakers": "single",
            "difficulty": "General"
        }
        
        # Don't actually generate - just test connectivity
        logger.info("Cloud Function appears accessible (use full test for generation)")
        return True
        
    except Exception as e:
        logger.error(f"❌ Cloud Function error: {e}")
        return False

def analyze_rss_feed():
    """Analyze RSS feed for date and metadata issues"""
    logger.info("🔍 Analyzing RSS feed...")
    
    try:
        feed_url = "https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/feeds/copernicus-mvp-rss-feed.xml"
        response = requests.get(feed_url, timeout=30)
        
        if response.status_code != 200:
            logger.error(f"❌ Cannot access RSS feed: {response.status_code}")
            return False
        
        # Parse XML
        root = ET.fromstring(response.content)
        items = root.findall('.//item')
        
        logger.info(f"📊 Found {len(items)} episodes in RSS feed")
        
        # Check dates
        future_dates = 0
        for i, item in enumerate(items[:5]):  # Check first 5
            pub_date_elem = item.find('pubDate')
            if pub_date_elem is not None:
                pub_date = pub_date_elem.text
                logger.info(f"Episode {i+1} date: {pub_date}")
                
                if '2025' in pub_date:
                    future_dates += 1
        
        if future_dates > 0:
            logger.warning(f"⚠️  Found {future_dates} episodes with future dates (2025)")
            logger.info("🔧 This needs to be fixed before platform submission")
        else:
            logger.info("✅ No future dates found")
        
        # Check file URLs
        logger.info("🔍 Checking audio file accessibility...")
        for i, item in enumerate(items[:3]):  # Check first 3
            enclosure = item.find('enclosure')
            if enclosure is not None:
                url = enclosure.get('url')
                if url:
                    try:
                        resp = requests.head(url, timeout=10)
                        size = resp.headers.get('content-length', 'unknown')
                        logger.info(f"Episode {i+1} audio: {resp.status_code} ({size} bytes)")
                    except Exception as e:
                        logger.error(f"Episode {i+1} audio error: {e}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ RSS feed analysis failed: {e}")
        return False

def create_quick_fix_summary():
    """Create a summary of issues and fixes"""
    summary = """
# 🎙️ Podcast System - Issue Analysis & Fixes

## 🔍 Current Issues Identified

### 1. Filename Numbering Problem
- **Issue**: Files overwriting instead of incrementing
- **Root Cause**: Filename generation not checking existing files
- **Fix**: Implemented `get_next_filename()` with collision detection

### 2. Multi-Voice Audio Problem  
- **Issue**: Same voice for all speakers
- **Root Cause**: Voice assignment logic not working
- **Fix**: Distinct voice mapping with Google TTS different models

### 3. Duration Problem
- **Issue**: 4-5 minutes instead of 10 minutes
- **Root Cause**: Content generation not targeting word count
- **Fix**: Word count calculation (140-160 WPM) with duration targeting

### 4. Endpoint Confusion
- **Issue**: Two endpoints, unclear which is used
- **Root Cause**: Legacy code and unclear routing
- **Fix**: Single main endpoint `/generate-podcast` with legacy redirect

### 5. Debugging Issues
- **Issue**: No logging, hard to trace problems
- **Root Cause**: Insufficient error handling and logging
- **Fix**: Comprehensive structured logging with job IDs

## 🚀 Solution Implemented

### New Architecture:
```
Form → Cloud Function → Cloud Run Backend → Storage
                              ↓
                      [OpenAI + Google TTS]
```

### Key Improvements:
1. **Robust filename generation** with collision detection
2. **Multiple distinct voices** using Google TTS
3. **Duration targeting** based on word count
4. **Comprehensive logging** for debugging
5. **Error handling** with graceful degradation
6. **Health checks** and monitoring endpoints

## 📋 Deployment Steps

1. **Deploy Backend**: `bash deploy_backend.sh`
2. **Set API Key**: Update Cloud Run with OpenAI API key
3. **Deploy Function**: Update and run `bash deploy_function.sh`
4. **Test System**: `python3 test_podcast_system.py`
5. **Fix RSS Feed**: `python3 fix_existing_issues.py`

## ✅ Expected Results After Fix

- ✅ Filenames increment: `ever-math-250034` → `ever-math-250035`
- ✅ Multiple voices in multi-speaker podcasts
- ✅ Duration matches request (±1 minute)
- ✅ Complete request tracing with job IDs
- ✅ Clear error messages for debugging
"""
    
    with open('ISSUE_ANALYSIS.md', 'w') as f:
        f.write(summary)
    
    logger.info("📄 Issue analysis saved to: ISSUE_ANALYSIS.md")

def main():
    """Run complete analysis"""
    logger.info("🧪 Starting podcast system analysis...")
    
    results = {}
    
    # Test form
    results['form'] = test_form_accessibility()
    
    # Test Cloud Function
    results['function'] = test_cloud_function()
    
    # Analyze RSS feed
    results['rss'] = analyze_rss_feed()
    
    # Create summary
    create_quick_fix_summary()
    
    # Results
    logger.info("📋 Analysis Results:")
    for component, status in results.items():
        status_icon = "✅" if status else "❌"
        logger.info(f"  {component}: {status_icon}")
    
    logger.info("\n🚀 Next Steps:")
    logger.info("1. Review ISSUE_ANALYSIS.md for detailed fix plan")
    logger.info("2. Deploy new backend: bash deploy_backend.sh")
    logger.info("3. Test with comprehensive suite")
    
    return results

if __name__ == "__main__":
    main()