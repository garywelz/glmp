#!/usr/bin/env python3
"""
GLMP Graph Validator
Detects logic and syntax errors in all 108 process flowcharts

Error Patterns Detected:
1. AND gates with < 2 inputs
2. OR gates with < 2 outputs
3. Trapezoids that aren't terminal (have children)
4. Multiple inputs without AND gate marking
5. Multiple outputs without OR gate marking
6. Mermaid syntax errors
"""

import json
import re
import os
from collections import defaultdict
from pathlib import Path

class GraphValidator:
    def __init__(self, process_dir):
        self.process_dir = Path(process_dir)
        self.errors = defaultdict(list)
        self.warnings = defaultdict(list)
        
    def validate_all(self):
        """Validate all process JSON files"""
        process_files = []
        for organism_dir in ['ecoli', 'yeast', 'bacillus']:
            org_path = self.process_dir / organism_dir
            if org_path.exists():
                process_files.extend(org_path.glob('*.json'))
        
        print(f"🔍 Validating {len(process_files)} processes...")
        print()
        
        for process_file in sorted(process_files):
            self.validate_process(process_file)
        
        return self.generate_report()
    
    def validate_process(self, filepath):
        """Validate a single process file"""
        try:
            with open(filepath) as f:
                process = json.load(f)
            
            process_id = process['id']
            mermaid = process.get('mermaid', '')
            
            if not mermaid:
                self.errors[process_id].append("No Mermaid diagram found")
                return
            
            # Parse the Mermaid diagram
            graph = self.parse_mermaid(mermaid)
            
            # Run all validation checks
            self.check_and_gates(process_id, graph)
            self.check_or_gates(process_id, graph)
            self.check_trapezoid_sequences(process_id, graph)
            self.check_missing_logic_gates(process_id, graph)
            self.check_mermaid_syntax(process_id, mermaid)
            
        except Exception as e:
            self.errors[process_id].append(f"Failed to process: {str(e)}")
    
    def parse_mermaid(self, mermaid):
        """Parse Mermaid diagram into graph structure"""
        graph = {
            'nodes': {},  # node_id -> {label, shape, style}
            'edges': [],  # (from, to, label)
            'inputs': defaultdict(list),  # node_id -> [parent_ids]
            'outputs': defaultdict(list),  # node_id -> [child_ids]
        }
        
        lines = mermaid.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('%%') or line.startswith('style '):
                continue
            
            # Parse node connections: A --> B
            edge_match = re.match(r'(\w+)\s*-->\s*(\w+|\{.*?\}|\{\{.*?\}\})', line)
            if edge_match:
                from_node = edge_match.group(1)
                to_node = edge_match.group(2).strip('{}')
                graph['edges'].append((from_node, to_node, None))
                graph['inputs'][to_node].append(from_node)
                graph['outputs'][from_node].append(to_node)
                continue
            
            # Parse node connections with labels: A -->|label| B
            edge_label_match = re.match(r'(\w+)\s*-->\s*\|([^|]+)\|\s*(\w+)', line)
            if edge_label_match:
                from_node = edge_label_match.group(1)
                label = edge_label_match.group(2)
                to_node = edge_label_match.group(3)
                graph['edges'].append((from_node, to_node, label))
                graph['inputs'][to_node].append(from_node)
                graph['outputs'][from_node].append(to_node)
                continue
            
            # Parse node definitions
            # AND gate: {{NodeID: Label}}
            and_match = re.match(r'(\w+)\{\{([^}]+)\}\}', line)
            if and_match:
                node_id = and_match.group(1)
                label = and_match.group(2)
                graph['nodes'][node_id] = {'label': label, 'shape': 'and', 'type': 'logic'}
                continue
            
            # OR gate: {NodeID: Label}
            or_match = re.match(r'(\w+)\{([^}]+)\}', line)
            if or_match:
                node_id = or_match.group(1)
                label = or_match.group(2)
                graph['nodes'][node_id] = {'label': label, 'shape': 'or', 'type': 'logic'}
                continue
            
            # Trapezoid: [/Label/]
            trap_match = re.match(r'(\w+)\[/([^/]+)/\]', line)
            if trap_match:
                node_id = trap_match.group(1)
                label = trap_match.group(2)
                graph['nodes'][node_id] = {'label': label, 'shape': 'trapezoid', 'type': 'terminal'}
                continue
            
            # Regular rectangle: [Label]
            rect_match = re.match(r'(\w+)\[([^\]]+)\]', line)
            if rect_match:
                node_id = rect_match.group(1)
                label = rect_match.group(2)
                graph['nodes'][node_id] = {'label': label, 'shape': 'rectangle', 'type': 'normal'}
                continue
        
        return graph
    
    def check_and_gates(self, process_id, graph):
        """Check AND gates have 2+ inputs"""
        for node_id, node_data in graph['nodes'].items():
            if node_data.get('shape') == 'and':
                inputs = graph['inputs'][node_id]
                if len(inputs) < 2:
                    self.errors[process_id].append(
                        f"❌ AND gate '{node_id}' has only {len(inputs)} input(s) - needs 2+"
                    )
    
    def check_or_gates(self, process_id, graph):
        """Check OR gates have 2+ outputs"""
        for node_id, node_data in graph['nodes'].items():
            if node_data.get('shape') == 'or':
                outputs = graph['outputs'][node_id]
                if len(outputs) < 2:
                    self.errors[process_id].append(
                        f"❌ OR gate '{node_id}' has only {len(outputs)} output(s) - needs 2+"
                    )
    
    def check_trapezoid_sequences(self, process_id, graph):
        """Check trapezoids are terminal (no non-trapezoid children)"""
        for node_id, node_data in graph['nodes'].items():
            if node_data.get('shape') == 'trapezoid':
                children = graph['outputs'][node_id]
                
                # Check if any children exist
                if children:
                    non_trap_children = []
                    for child_id in children:
                        child_node = graph['nodes'].get(child_id, {})
                        if child_node.get('shape') != 'trapezoid':
                            non_trap_children.append(child_id)
                    
                    if non_trap_children:
                        self.errors[process_id].append(
                            f"❌ Trapezoid '{node_id}' is NOT terminal - has children: {non_trap_children}"
                        )
    
    def check_missing_logic_gates(self, process_id, graph):
        """Check for nodes with multiple inputs/outputs that should be logic gates"""
        for node_id, node_data in graph['nodes'].items():
            node_type = node_data.get('type', 'normal')
            
            # Skip if already a logic gate
            if node_type == 'logic':
                continue
            
            # Check for multiple inputs (potential AND gate)
            inputs = graph['inputs'][node_id]
            if len(inputs) >= 2:
                self.warnings[process_id].append(
                    f"⚠️  Node '{node_id}' has {len(inputs)} inputs but is not marked as AND gate"
                )
            
            # Check for multiple outputs (potential OR gate)
            outputs = graph['outputs'][node_id]
            if len(outputs) >= 2:
                self.warnings[process_id].append(
                    f"⚠️  Node '{node_id}' has {len(outputs)} outputs but is not marked as OR gate"
                )
    
    def check_mermaid_syntax(self, process_id, mermaid):
        """Check for common Mermaid syntax errors"""
        lines = mermaid.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Check for brackets inside trapezoid labels
            if re.search(r'\[/[^\]]*\[.*?\][^\]]*/', line):
                self.errors[process_id].append(
                    f"❌ Line {i}: Brackets inside trapezoid label - Mermaid syntax error"
                )
            
            # Check for wrong trapezoid syntax [\\...../]
            if re.search(r'\[\\\\.*?/\]', line):
                self.errors[process_id].append(
                    f"❌ Line {i}: Wrong trapezoid syntax [\\\\...../] - should be [/..../]"
                )
            
            # Check for missing closing brackets
            open_brackets = line.count('[')
            close_brackets = line.count(']')
            if open_brackets != close_brackets and '-->' in line:
                self.warnings[process_id].append(
                    f"⚠️  Line {i}: Unbalanced brackets (may cause syntax error)"
                )
    
    def generate_report(self):
        """Generate comprehensive validation report"""
        report = []
        report.append("╔══════════════════════════════════════════════════════════════════════════════╗")
        report.append("║                                                                              ║")
        report.append("║                    📊 GRAPH VALIDATION REPORT                                ║")
        report.append("║                                                                              ║")
        report.append("╚══════════════════════════════════════════════════════════════════════════════╝")
        report.append("")
        
        total_errors = sum(len(errs) for errs in self.errors.values())
        total_warnings = sum(len(warns) for warns in self.warnings.values())
        processes_with_errors = len(self.errors)
        processes_with_warnings = len(self.warnings)
        
        report.append(f"📊 SUMMARY:")
        report.append(f"  Total Errors:   {total_errors}")
        report.append(f"  Total Warnings: {total_warnings}")
        report.append(f"  Processes with Errors:   {processes_with_errors}")
        report.append(f"  Processes with Warnings: {processes_with_warnings}")
        report.append("")
        
        # Group by error type
        syntax_errors = []
        logic_errors = []
        trapezoid_errors = []
        
        for process_id, error_list in sorted(self.errors.items()):
            for error in error_list:
                if 'syntax' in error.lower() or 'bracket' in error.lower():
                    syntax_errors.append((process_id, error))
                elif 'trapezoid' in error.lower():
                    trapezoid_errors.append((process_id, error))
                else:
                    logic_errors.append((process_id, error))
        
        report.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        report.append("🔴 CRITICAL: Mermaid Syntax Errors (Breaks Rendering)")
        report.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        report.append("")
        
        if syntax_errors:
            for process_id, error in syntax_errors:
                report.append(f"  {process_id}:")
                report.append(f"    {error}")
                report.append("")
        else:
            report.append("  ✅ No syntax errors found!")
            report.append("")
        
        report.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        report.append("🟡 HIGH: Trapezoid Sequence Errors (Confusing Logic)")
        report.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        report.append("")
        
        if trapezoid_errors:
            for process_id, error in trapezoid_errors:
                report.append(f"  {process_id}:")
                report.append(f"    {error}")
                report.append("")
        else:
            report.append("  ✅ No trapezoid sequence errors found!")
            report.append("")
        
        report.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        report.append("🟡 HIGH: Logic Gate Errors (Invalid AND/OR)")
        report.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        report.append("")
        
        if logic_errors:
            for process_id, error in logic_errors:
                report.append(f"  {process_id}:")
                report.append(f"    {error}")
                report.append("")
        else:
            report.append("  ✅ No logic gate errors found!")
            report.append("")
        
        report.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        report.append("🟢 MEDIUM: Warnings (Missing Logic Gate Markings)")
        report.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        report.append("")
        
        # Show only first 20 warnings
        warning_count = 0
        for process_id, warning_list in sorted(self.warnings.items()):
            if warning_count >= 20:
                report.append(f"  ... and {total_warnings - 20} more warnings")
                break
            for warning in warning_list:
                report.append(f"  {process_id}:")
                report.append(f"    {warning}")
                report.append("")
                warning_count += 1
        
        if total_warnings == 0:
            report.append("  ✅ No warnings!")
            report.append("")
        
        report.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        report.append("✅ VALIDATION COMPLETE")
        report.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        report.append("")
        
        return '\n'.join(report)

if __name__ == '__main__':
    import sys
    
    process_dir = sys.argv[1] if len(sys.argv) > 1 else '/workspace/processes_with_not_gates'
    
    validator = GraphValidator(process_dir)
    report = validator.validate_all()
    
    print(report)
    
    # Save report to file
    with open('/workspace/GRAPH_VALIDATION_REPORT.txt', 'w') as f:
        f.write(report)
    
    print("\n📁 Report saved to: GRAPH_VALIDATION_REPORT.txt")
