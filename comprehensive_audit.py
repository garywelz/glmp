#!/usr/bin/env python3
"""
Comprehensive GLMP Process Audit

Validates all 108 processes for:
1. Technical accuracy (shapes, colors, counts)
2. Semantic appropriateness (gate identification)
3. Color consistency (semantic coloring)

Acknowledges subjectivity and flags judgment calls for review.
"""

import json
import re
import sys
from pathlib import Path
from collections import defaultdict

class ProcessAuditor:
    def __init__(self):
        self.results = []
        self.subjective_flags = []
        
        # Expected colors (Phase 2 semantic scheme)
        self.colors = {
            'green': '#51cf66',      # Triggers
            'amber': '#ffa726',      # Enzymes
            'darkSkyBlue': '#42a5f5', # Processing
            'lightCyan': '#b3e5fc',  # Intermediates
            'yellow': '#ffd600',     # OR gates
            'purple': '#7950f2',     # AND gates
            'red': '#e74c3c',        # NOT gates
            'black': '#000000'       # Products
        }
        
        # Gate shape patterns
        self.or_pattern = re.compile(r'(\w+)\{\{')
        self.and_pattern = re.compile(r'(\w+)\[\[\[')
        self.not_pattern = re.compile(r'(\w+)\[/')
        
    def count_visual_gates(self, mermaid):
        """Count actual visual gate shapes in Mermaid code."""
        or_nodes = self.or_pattern.findall(mermaid)
        and_nodes = self.and_pattern.findall(mermaid)
        not_nodes = self.not_pattern.findall(mermaid)
        
        return {
            'or': len(or_nodes),
            'and': len(and_nodes),
            'not': len(not_nodes),
            'or_nodes': or_nodes,
            'and_nodes': and_nodes,
            'not_nodes': not_nodes
        }
    
    def check_gate_colors(self, mermaid, visual_gates):
        """Verify gate nodes have correct colors."""
        issues = []
        
        # Extract style statements
        style_lines = [line.strip() for line in mermaid.split('\n') if 'style ' in line]
        
        # Check each gate type
        for or_node in visual_gates['or_nodes']:
            # Find style for this node
            node_style = [s for s in style_lines if or_node in s]
            if node_style:
                if '#ffd600' not in node_style[0] and 'yellow' not in node_style[0]:
                    issues.append(f"OR gate '{or_node}' not styled yellow")
            else:
                issues.append(f"OR gate '{or_node}' has no style")
        
        for and_node in visual_gates['and_nodes']:
            node_style = [s for s in style_lines if and_node in s]
            if node_style:
                if '#7950f2' not in node_style[0] and 'purple' not in node_style[0]:
                    issues.append(f"AND gate '{and_node}' not styled purple")
            else:
                issues.append(f"AND gate '{and_node}' has no style")
        
        for not_node in visual_gates['not_nodes']:
            node_style = [s for s in style_lines if not_node in s]
            if node_style:
                if '#e74c3c' not in node_style[0] and 'red' not in node_style[0]:
                    issues.append(f"NOT gate '{not_node}' not styled red")
            else:
                issues.append(f"NOT gate '{not_node}' has no style")
        
        return issues
    
    def check_semantic_appropriateness(self, mermaid, visual_gates):
        """Check if identified gates are biologically appropriate.
        
        This is SUBJECTIVE and flags questionable cases.
        """
        flags = []
        
        # Extract node definitions to check labels
        node_defs = {}
        for line in mermaid.split('\n'):
            # Match patterns like: NodeID[Label Text] or NodeID{{Label}}
            match = re.search(r'(\w+)[\[{/]+([^}\]]+)[\]}/]+', line)
            if match:
                node_id, label = match.groups()
                node_defs[node_id] = label.strip()
        
        # Check OR gates - should represent genuine alternatives
        for or_node in visual_gates['or_nodes']:
            label = node_defs.get(or_node, '')
            
            # Questionable if it's just describing conditions
            if 'high' in label.lower() or 'low' in label.lower():
                flags.append({
                    'node': or_node,
                    'type': 'OR',
                    'label': label,
                    'concern': 'May be describing conditions rather than true alternative pathways',
                    'severity': 'review'
                })
        
        # Check AND gates - should represent multi-component requirements
        for and_node in visual_gates['and_nodes']:
            label = node_defs.get(and_node, '')
            
            # Should contain words indicating assembly/requirement
            assembly_words = ['requires', 'assembly', 'complex', 'both', 'all']
            if not any(word in label.lower() for word in assembly_words):
                flags.append({
                    'node': and_node,
                    'type': 'AND',
                    'label': label,
                    'concern': 'AND gate label unclear about multi-component requirement',
                    'severity': 'review'
                })
        
        # Check NOT gates - should represent active repression
        for not_node in visual_gates['not_nodes']:
            label = node_defs.get(not_node, '')
            
            # Should contain repression-related words
            repression_words = ['repressor', 'inhibit', 'block', 'prevent', 'suppress']
            if not any(word in label.lower() for word in repression_words):
                flags.append({
                    'node': not_node,
                    'type': 'NOT',
                    'label': label,
                    'concern': 'NOT gate label unclear about active repression mechanism',
                    'severity': 'review'
                })
        
        return flags
    
    def audit_process(self, process_data):
        """Comprehensive audit of single process."""
        process_id = process_data.get('id', 'unknown')
        process_name = process_data.get('name', 'Unknown')
        
        result = {
            'id': process_id,
            'name': process_name,
            'organism': process_data.get('organism', 'Unknown'),
            'valid': True,
            'issues': [],
            'warnings': [],
            'subjective_flags': []
        }
        
        # Get metadata claims
        metadata_gates = process_data.get('logicGates', {})
        claimed = {
            'or': metadata_gates.get('or', 0),
            'and': metadata_gates.get('and', 0),
            'not': metadata_gates.get('not', 0)
        }
        
        # Count visual gates
        mermaid = process_data.get('mermaid', '')
        visual = self.count_visual_gates(mermaid)
        
        # Check for discrepancies
        if claimed['or'] != visual['or']:
            result['valid'] = False
            result['issues'].append(f"OR gate count mismatch: claimed {claimed['or']}, visual {visual['or']}")
        
        if claimed['and'] != visual['and']:
            result['valid'] = False
            result['issues'].append(f"AND gate count mismatch: claimed {claimed['and']}, visual {visual['and']}")
        
        if claimed['not'] != visual['not']:
            result['valid'] = False
            result['issues'].append(f"NOT gate count mismatch: claimed {claimed['not']}, visual {visual['not']}")
        
        # Check gate colors
        color_issues = self.check_gate_colors(mermaid, visual)
        if color_issues:
            result['valid'] = False
            result['issues'].extend(color_issues)
        
        # Check semantic appropriateness (subjective)
        semantic_flags = self.check_semantic_appropriateness(mermaid, visual)
        if semantic_flags:
            result['subjective_flags'] = semantic_flags
        
        # Store counts for reporting
        result['claimed'] = claimed
        result['visual'] = {
            'or': visual['or'],
            'and': visual['and'],
            'not': visual['not']
        }
        result['gate_nodes'] = {
            'or': visual['or_nodes'],
            'and': visual['and_nodes'],
            'not': visual['not_nodes']
        }
        
        return result
    
    def generate_report(self, results):
        """Generate comprehensive audit report."""
        total = len(results)
        valid = sum(1 for r in results if r['valid'])
        invalid = total - valid
        
        report = []
        report.append("=" * 80)
        report.append("🔍 COMPREHENSIVE GLMP PROCESS AUDIT REPORT")
        report.append("=" * 80)
        report.append("")
        report.append(f"Total Processes Audited: {total}")
        report.append(f"✅ Valid (no technical issues): {valid} ({valid/total*100:.1f}%)")
        report.append(f"❌ Invalid (technical issues found): {invalid} ({invalid/total*100:.1f}%)")
        report.append("")
        
        # Count subjective flags
        total_flags = sum(len(r['subjective_flags']) for r in results)
        report.append(f"⚠️  Subjective Concerns Flagged: {total_flags}")
        report.append("")
        
        # Summary of issues
        report.append("=" * 80)
        report.append("📊 ISSUE SUMMARY")
        report.append("=" * 80)
        report.append("")
        
        issue_types = defaultdict(int)
        for r in results:
            for issue in r['issues']:
                if 'count mismatch' in issue:
                    issue_types['Count Mismatch'] += 1
                elif 'not styled' in issue:
                    issue_types['Incorrect Color'] += 1
                elif 'no style' in issue:
                    issue_types['Missing Style'] += 1
        
        for issue_type, count in sorted(issue_types.items(), key=lambda x: -x[1]):
            report.append(f"  {issue_type}: {count}")
        report.append("")
        
        # Detailed process reports
        report.append("=" * 80)
        report.append("📋 DETAILED PROCESS REPORTS")
        report.append("=" * 80)
        report.append("")
        
        for r in results:
            if not r['valid'] or r['subjective_flags']:
                report.append(f"Process: {r['name']}")
                report.append(f"ID: {r['id']}")
                report.append(f"Organism: {r['organism']}")
                report.append(f"Status: {'❌ INVALID' if not r['valid'] else '⚠️  REVIEW NEEDED'}")
                report.append("")
                
                if r['issues']:
                    report.append("  Technical Issues:")
                    for issue in r['issues']:
                        report.append(f"    • {issue}")
                    report.append("")
                
                report.append(f"  Gate Counts:")
                report.append(f"    Claimed: OR={r['claimed']['or']}, AND={r['claimed']['and']}, NOT={r['claimed']['not']}")
                report.append(f"    Visual:  OR={r['visual']['or']}, AND={r['visual']['and']}, NOT={r['visual']['not']}")
                report.append("")
                
                if r['gate_nodes']['or']:
                    report.append(f"  OR gates: {', '.join(r['gate_nodes']['or'])}")
                if r['gate_nodes']['and']:
                    report.append(f"  AND gates: {', '.join(r['gate_nodes']['and'])}")
                if r['gate_nodes']['not']:
                    report.append(f"  NOT gates: {', '.join(r['gate_nodes']['not'])}")
                report.append("")
                
                if r['subjective_flags']:
                    report.append("  ⚠️  Subjective Concerns:")
                    for flag in r['subjective_flags']:
                        report.append(f"    • {flag['type']} gate '{flag['node']}':")
                        report.append(f"      Label: \"{flag['label']}\"")
                        report.append(f"      Concern: {flag['concern']}")
                    report.append("")
                
                report.append("-" * 80)
                report.append("")
        
        return "\n".join(report)

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 comprehensive_audit.py <metadata.json>")
        print("   or: python3 comprehensive_audit.py --url <metadata_url>")
        sys.exit(1)
    
    # Load metadata
    if sys.argv[1] == '--url':
        import urllib.request
        url = sys.argv[2]
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read())
    else:
        with open(sys.argv[1]) as f:
            data = json.load(f)
    
    processes = data.get('processes', [])
    
    print(f"🔍 Starting comprehensive audit of {len(processes)} processes...")
    print()
    
    auditor = ProcessAuditor()
    results = []
    
    for i, process in enumerate(processes, 1):
        result = auditor.audit_process(process)
        results.append(result)
        
        # Progress indicator
        if i % 10 == 0:
            print(f"  Processed {i}/{len(processes)}...")
    
    print()
    print("✅ Audit complete!")
    print()
    
    # Generate and print report
    report = auditor.generate_report(results)
    print(report)
    
    # Save to file
    output_file = 'glmp_audit_report.txt'
    with open(output_file, 'w') as f:
        f.write(report)
    
    print()
    print(f"📄 Full report saved to: {output_file}")
    
    # Exit code
    invalid_count = sum(1 for r in results if not r['valid'])
    sys.exit(0 if invalid_count == 0 else 1)

if __name__ == '__main__':
    main()
