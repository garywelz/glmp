#!/usr/bin/env python3
"""
Fix syntax errors in the three identified processes
"""

import json
import urllib.request
from google.cloud import storage

BUCKET_NAME = "regal-scholar-453620-r7-podcast-storage"
PROCESSES_BASE_URL = f"https://storage.googleapis.com/{BUCKET_NAME}/glmp-v2/processes/"

# Processes to fix
PROCESSES_TO_FIX = [
    ("ecoli_stringent_response", "ecoli", 20),
    ("ecoli_fatty_acid_degradation", "ecoli", 47),
    ("ecoli_homologous_recombination", "ecoli", 115),
]

def fetch_process(process_id, organism):
    """Fetch process JSON from GCS"""
    url = f"{PROCESSES_BASE_URL}{organism}/{process_id}.json"
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"Error fetching {process_id}: {e}")
        return None

def fix_stringent_response(mermaid):
    """Fix line 20: subgraph ending issue with (p)ppGpp"""
    lines = mermaid.split('\n')
    fixed_lines = []
    
    for i, line in enumerate(lines, 1):
        if i == 20:
            # The issue is likely with parentheses in subgraph name/label
            # Look for subgraph ending with (p)ppGpp
            if 'end' in line.lower() and '(p)ppGpp' in line:
                # Fix: ensure proper subgraph syntax
                # If it's trying to end a subgraph, make sure it's properly formatted
                line = line.replace('(p)ppGpp', 'ppGpp')  # Remove problematic parentheses
                # Or if it's a label, quote it properly
                if 'subgraph' in lines[i-2].lower() if i > 2 else False:
                    # Check previous lines for subgraph start
                    pass
            # Alternative: if it's a node label with parentheses, quote it
            if '[' in line and '(p)ppGpp' in line and ']' in line:
                # Quote the label properly
                line = line.replace('(p)ppGpp', '"ppGpp"')
        fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)

def fix_fatty_acid_degradation(mermaid):
    """Fix line 47: malformed diamond node syntax"""
    lines = mermaid.split('\n')
    fixed_lines = []
    
    for i, line in enumerate(lines, 1):
        if i == 47:
            # The error shows: AP[\{{AND: CoA-SH Av
            # This is malformed - should be AP{AND: CoA-SH Available?}
            # Fix the \{{ syntax
            if '\\{{' in line or '[{{' in line:
                # Replace malformed syntax
                line = line.replace('\\{{', '{')
                line = line.replace('[{{', '{')
                # Ensure proper closing
                if '}}' in line:
                    line = line.replace('}}', '}')
                # If it has [ at start, remove it for diamond node
                if line.strip().startswith('AP['):
                    line = line.replace('AP[', 'AP{', 1)
        fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)

def fix_homologous_recombination(mermaid):
    """Fix line 115: forward slashes in node label"""
    lines = mermaid.split('\n')
    fixed_lines = []
    
    for i, line in enumerate(lines, 1):
        if i == 115:
            # The error shows: End4[/(DNA degraded)/]
            # Forward slashes inside brackets cause issues
            # Should be: End4["(DNA degraded)"] or End4[(DNA degraded)]
            if 'End4' in line and '/(' in line and ')/' in line:
                # Remove forward slashes, keep parentheses
                line = line.replace('/(', '(')
                line = line.replace(')/', ')')
                # Or quote the entire label
                if '[' in line and ']' in line:
                    # Find the label content and quote it
                    start = line.find('[')
                    end = line.find(']')
                    if start != -1 and end != -1:
                        label = line[start+1:end]
                        if not label.startswith('"'):
                            label = f'"{label}"'
                            line = line[:start+1] + label + line[end:]
        fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)

def save_process(process_id, organism, process_data):
    """Save fixed process back to GCS"""
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(f"glmp-v2/processes/{organism}/{process_id}.json")
    
    blob.upload_from_string(
        json.dumps(process_data, indent=2),
        content_type="application/json"
    )
    print(f"✅ Saved {process_id}")

def main():
    print("🔧 Fixing Syntax Errors in 3 Processes")
    print("=" * 60)
    
    fixes = {
        "ecoli_stringent_response": fix_stringent_response,
        "ecoli_fatty_acid_degradation": fix_fatty_acid_degradation,
        "ecoli_homologous_recombination": fix_homologous_recombination,
    }
    
    for process_id, organism, error_line in PROCESSES_TO_FIX:
        print(f"\n📝 Processing {process_id} (error on line {error_line})...")
        
        # Fetch process
        process_data = fetch_process(process_id, organism)
        if not process_data:
            print(f"❌ Failed to fetch {process_id}")
            continue
        
        # Show problematic line
        mermaid = process_data.get('mermaid', '')
        lines = mermaid.split('\n')
        if error_line <= len(lines):
            print(f"   Line {error_line}: {lines[error_line-1]}")
        
        # Fix it
        fix_func = fixes.get(process_id)
        if fix_func:
            fixed_mermaid = fix_func(mermaid)
            process_data['mermaid'] = fixed_mermaid
            
            # Save
            save_process(process_id, organism, process_data)
            print(f"✅ Fixed {process_id}")
        else:
            print(f"❌ No fix function for {process_id}")
    
    print("\n" + "=" * 60)
    print("✅ Complete!")

if __name__ == '__main__':
    main()

