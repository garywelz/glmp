#!/usr/bin/env python3
"""
Fix Mermaid syntax errors in three identified processes
"""

import json
import sys

def fix_stringent_response(mermaid_code):
    """Fix forward slashes in node labels"""
    # The issue is with AV[/ppGpp Degradation/] - forward slashes in brackets
    # Should be: AV["ppGpp Degradation"] or AV[(ppGpp Degradation)]
    fixed = mermaid_code.replace('AV[/ppGpp Degradation/]', 'AV["ppGpp Degradation"]')
    return fixed

def fix_fatty_acid_degradation(mermaid_code):
    """Fix line 47: malformed diamond node syntax"""
    # The error: AP[\\{{AND: CoA-SH<br/>Available?/]}}
    # Should be: AP{{AND: CoA-SH<br/>Available?}}
    # Find and replace the malformed pattern
    fixed = mermaid_code.replace('AP[\\{{AND: CoA-SH<br/>Available?/]}}', 'AP{{AND: CoA-SH<br/>Available?}}')
    # Also check for any other variations
    fixed = fixed.replace('AP[{{AND:', 'AP{{AND:')
    fixed = fixed.replace('AP[\\{{AND:', 'AP{{AND:')
    return fixed

def fix_homologous_recombination(mermaid_code):
    """Fix line 115: forward slashes in node label"""
    # The error: End4[/(DNA degraded)/]
    # Should be: End4["(DNA degraded)"] or End4[(DNA degraded)]
    fixed = mermaid_code.replace('End4[/(DNA degraded)/]', 'End4["(DNA degraded)"]')
    return fixed

def main():
    files_to_fix = [
        ('/tmp/stringent.json', 'ecoli_stringent_response', fix_stringent_response),
        ('/tmp/fatty_acid.json', 'ecoli_fatty_acid_degradation', fix_fatty_acid_degradation),
        ('/tmp/homologous.json', 'ecoli_homologous_recombination', fix_homologous_recombination),
    ]
    
    print("🔧 Fixing Mermaid Syntax Errors")
    print("=" * 60)
    
    for filepath, process_id, fix_func in files_to_fix:
        print(f"\n📝 Processing {process_id}...")
        
        try:
            # Read the JSON file
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Get the mermaid code
            mermaid_code = data.get('mermaid', '')
            if not mermaid_code:
                print(f"   ⚠️  No mermaid code found in {process_id}")
                continue
            
            # Show before/after for the problematic line
            lines = mermaid_code.split('\n')
            print(f"   📄 Mermaid code has {len(lines)} lines")
            
            # Apply the fix
            fixed_mermaid = fix_func(mermaid_code)
            
            # Check if anything changed
            if fixed_mermaid == mermaid_code:
                print(f"   ⚠️  No changes made - pattern not found")
                # Show a sample of the mermaid code to help debug
                print(f"   📋 First 10 lines of mermaid:")
                for i, line in enumerate(lines[:10], 1):
                    print(f"      {i}: {line}")
            else:
                # Update the data
                data['mermaid'] = fixed_mermaid
                
                # Save back to the file
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                print(f"   ✅ Fixed and saved {process_id}")
                
        except Exception as e:
            print(f"   ❌ Error processing {process_id}: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("✅ Fix complete! Files are ready to upload back to GCS.")

if __name__ == '__main__':
    main()



