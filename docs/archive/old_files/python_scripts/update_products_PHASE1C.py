#!/usr/bin/env python3
"""
PHASE 1C: Update Product Outputs to Black
==========================================
Convert final outcome/product nodes to true black (#000000).

Strategy:
- Target terminal outcome nodes (survival, growth, homeostasis)
- Leave intermediate products alone
- Use keyword matching + validation
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Tuple

# Keywords that indicate FINAL products/outcomes (not intermediates)
FINAL_PRODUCT_KEYWORDS = [
    'Survival', 'Growth', 'Homeostasis', 'Equilibrium', 
    'Complete Response', 'System Balance', 'Adaptation',
    'Mature Cell', 'Cell Division', 'Recovery',
    'Restored Function', 'Optimal', 'Successful',
    # Recombination products
    'Crossover product', 'Non-crossover product', 'recombinant', 'parental',
    # Transition states
    'transition', 'Phase Change'
]

def is_final_product(node_text: str) -> bool:
    """Check if node text indicates a final product/outcome"""
    text_lower = node_text.lower()
    
    # Check for final product keywords
    for keyword in FINAL_PRODUCT_KEYWORDS:
        if keyword.lower() in text_lower:
            return True
    
    return False

def get_node_text(node_id: str, mermaid: str) -> str:
    """Extract node text for a given node ID"""
    patterns = [
        rf'{node_id}\[([^\]]+)\]',
        rf'{node_id}\{{([^}}]+)\}}',
        rf'{node_id}\(([^)]+)\)',
        rf'{node_id}\[\\.([^/]+)/\]',  # Trapezoid
        rf'{node_id}\{{\{{([^}}]+)\}}\}}',  # Hexagon
    ]
    
    for pattern in patterns:
        match = re.search(pattern, mermaid)
        if match:
            return match.group(1)
    
    return ""

def update_products_to_black(json_path: Path) -> Dict:
    """Update final product nodes to black"""
    
    process_id = json_path.stem
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if 'mermaid' not in data:
            return {'success': False, 'error': 'No mermaid field'}
        
        mermaid = data['mermaid']
        original_mermaid = mermaid
        changes = []
        
        # Find all styled nodes
        style_pattern = r'style (\w+) fill:#([0-9a-fA-F]+)'
        styled_nodes = re.findall(style_pattern, mermaid)
        
        for node_id, current_color in styled_nodes:
            # Skip if already black
            if current_color == '000000':
                continue
            
            # Skip logic gates (we already updated these)
            if current_color in ['ff9f43', 'e74c3c', '7950f2']:  # OR, NOT, AND
                continue
            
            # Get node text
            node_text = get_node_text(node_id, mermaid)
            
            if not node_text:
                continue
            
            # Check if this is a final product
            if is_final_product(node_text):
                # Update style to black
                old_style = f'style {node_id} fill:#{current_color}'
                new_style = f'style {node_id} fill:#000000'
                
                mermaid = mermaid.replace(old_style, new_style)
                changes.append(f'{node_id}: {node_text[:40]} → black')
        
        # Save if changed
        if changes:
            data['mermaid'] = mermaid
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        
        return {
            'success': True,
            'changes': changes,
            'process_id': process_id,
            'count': len(changes)
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'process_id': process_id
        }

def main():
    """Main execution"""
    
    print("=" * 70)
    print("⚫ PHASE 1C: PRODUCT OUTPUTS → BLACK")
    print("=" * 70)
    print()
    print("Updating final outcome/product nodes to true black #000000")
    print()
    print("Target keywords:")
    for keyword in FINAL_PRODUCT_KEYWORDS[:10]:
        print(f"  • {keyword}")
    print(f"  ... and {len(FINAL_PRODUCT_KEYWORDS) - 10} more")
    print()
    print("=" * 70)
    print()
    
    # Find all process files
    gcs_dir = Path('/workspace/gcs-processes')
    json_files = list(gcs_dir.rglob('*.json'))
    
    results = []
    for json_file in sorted(json_files):
        result = update_products_to_black(json_file)
        results.append(result)
        
        rel_path = json_file.relative_to(gcs_dir)
        if result['success']:
            if result['changes']:
                count = result.get('count', 0)
                print(f"✓ {rel_path} ({count} products)")
                for change in result['changes'][:5]:  # Show first 5
                    print(f"  → {change}")
                if len(result['changes']) > 5:
                    print(f"  ... and {len(result['changes']) - 5} more")
        else:
            print(f"✗ {rel_path}: {result['error']}")
    
    # Summary
    print()
    print("=" * 70)
    print("📊 SUMMARY")
    print("=" * 70)
    
    updated = [r for r in results if r['success'] and r['changes']]
    unchanged = [r for r in results if r['success'] and not r['changes']]
    failed = [r for r in results if not r['success']]
    
    print(f"  Total files:            {len(results)}")
    print(f"  ✓ Products updated:     {len(updated)}")
    print(f"  ⊘ No changes:           {len(unchanged)}")
    print(f"  ✗ Failed:               {len(failed)}")
    print()
    
    if updated:
        total_products = sum(r.get('count', 0) for r in updated)
        print(f"  Total products → black: {total_products}")
        print()
        print("🎉 Phase 1C complete!")
        print()
        print("✅ PHASE 1 (A+B+C) FULLY COMPLETE:")
        print("  🟠 OR gates:  Orange diamond ◆    (#ff9f43)")
        print("  🟣 AND gates: Purple hexagon ⬡    (#7950f2)")
        print("  🔴 NOT gates: Red trapezoid ⏷     (#e74c3c)")
        print("  ⚫ Products:   True black         (#000000)")
        print()
        print("Ready for deployment! 🚀")
    
    return 0 if not failed else 1

if __name__ == '__main__':
    import sys
    sys.exit(main())
