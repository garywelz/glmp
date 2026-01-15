#!/bin/bash

# Upload the corrected GLMP database table to Google Cloud Storage
# This replaces the old version with the new one that has all the correct columns and data

echo "🚀 Uploading corrected GLMP database table..."

# Upload the corrected database table
gsutil cp glmp-database-table.html gs://regal-scholar-453620-r7-podcast-storage/glmp-database-table.html

# Set cache-busting headers to ensure fresh content
gsutil setmeta -h "Cache-Control:no-cache, no-store, must-revalidate" gs://regal-scholar-453620-r7-podcast-storage/glmp-database-table.html

echo "✅ Database table uploaded successfully!"
echo "📍 Available at: https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-database-table.html"
echo ""
echo "🔄 The table will now show:"
echo "   - All correct statistics from your live database"
echo "   - Colored dots for OR/AND/NOT gates"
echo "   - Architecture ratios (100:X:Y:Z) for each process"
echo "   - Auto-updates when new processes are added"
