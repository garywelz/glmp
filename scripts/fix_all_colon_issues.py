#!/usr/bin/env python3
"""
Fix all process files by quote-wrapping labels with colons or (...)+ patterns.
Uses the same logic as fix_anaerobic_colons.py but processes all JSON files.
"""

import json
import re
import sys
from pathlib import Path

def quote_problematic_labels(text):
    """Find node labels containing colons or (...)+ patterns and wrap them in quotes."""
    pattern = r'(\w+)\[([^\]]*(?::|\([^)]+\)\d+\+)[^\]]*)\]'
    
    def replacer(match):
        node_id = match.group(1)
        label = match.group(2)
        label_escaped = label.replace('"', '\\"')
        return f'{node_id}["{label_escaped}"]'
    
    return re.sub(pattern, replacer, text)

def fix_file(file_path, dry_run=False):
    """Fix a single JSON file."""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except Exception as e:
        return {'error': str(e)}
    
    mermaid = data.get('mermaid', '')
    if not mermaid:
        return {'skipped': 'No mermaid field'}
    
    # Count issues before fix
    issues_before = len(re.findall(r'\[[^\]]*(?::|\([^)]+\)\d+\+)[^\]]*\]', mermaid))
    
    if issues_before == 0:
        return {'skipped': 'No issues found'}
    
    fixed_mermaid = quote_problematic_labels(mermaid)
    
    # Count after (should be 0 unquoted, or same number quoted)
    issues_after = len(re.findall(r'\[[^\]]*(?::|\([^)]+\)\d+\+)[^\]]*\]', fixed_mermaid))
    
    if not dry_run:
        data['mermaid'] = fixed_mermaid
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    return {
        'name': data.get('name', 'Unknown'),
        'issues_before': issues_before,
        'issues_after': issues_after,
        'fixed': issues_after == 0
    }

def main():
    dry_run = '--dry-run' in sys.argv or '-n' in sys.argv
    processes_dir = Path("processes_with_not_gates")
    
    if not processes_dir.exists():
        print(f"❌ Error: Directory not found: {processes_dir}")
        sys.exit(1)
    
    mode = "DRY RUN" if dry_run else "FIX"
    print(f"🔧 {mode} mode: Scanning all process files...\n")
    
    results = []
    
    for json_file in sorted(processes_dir.rglob("*.json")):
        result = fix_file(json_file, dry_run=dry_run)
        if 'error' in result:
            print(f"❌ {json_file}: {result['error']}")
        elif 'skipped' in result:
            if result['skipped'] == 'No issues found':
                # Skip files with no issues (quiet mode)
                pass
            else:
                print(f"⏭️  {json_file}: {result['skipped']}")
        else:
            results.append((json_file, result))
            status = "Would fix" if dry_run else "Fixed"
            print(f"✅ {status}: {result['name']}")
            print(f"   {result['issues_before']} → {result['issues_after']} issues ({json_file})")
    
    if not results:
        print("\n✅ No files needed fixing!")
        return
    
    print(f"\n📊 Summary:")
    print(f"   • Files {'would be' if dry_run else 'were'} fixed: {len(results)}")
    total_fixed = sum(r['issues_before'] for _, r in results)
    print(f"   • Total labels {'would be' if dry_run else 'were'} fixed: {total_fixed}")
    
    if dry_run:
        print("\n💡 To apply fixes, run without --dry-run:")
        print("   python3 scripts/fix_all_colon_issues.py")
    else:
        print("\n✅ All fixes applied!")
        print("💡 Next steps:")
        print("   1. Review the changes")
        print("   2. Test affected processes in viewer")
        print("   3. Deploy to GCS")

if __name__ == "__main__":
    main()

