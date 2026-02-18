#!/usr/bin/env python3
"""
GLMP Collection Validator
Checks all processes for syntax errors, JSON validity, and Mermaid chart errors
"""

import json
import urllib.request
import urllib.error
import sys
from typing import Dict, List, Tuple
import re

# Configuration
METADATA_URL = 'https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/metadata.json'
PROCESSES_BASE_URL = 'https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/processes/'

# Required fields in process JSON
REQUIRED_FIELDS = ['id', 'name', 'organism', 'category', 'description', 'mermaid', 'sources']

# Mermaid syntax patterns to check
MERMAID_ERROR_PATTERNS = [
    (r'graph\s+TD', 'graph TD declaration'),
    (r'graph\s+LR', 'graph LR declaration'),
    (r'graph\s+BT', 'graph BT declaration'),
    (r'graph\s+RL', 'graph RL declaration'),
]

# Common Mermaid syntax errors
MERMAID_SYNTAX_ISSUES = [
    (r'--[^>]', 'Missing arrow direction (use --> or ---)'),
    (r'\["[^"]*"\]', 'Properly quoted node labels'),
    (r'style\s+\w+\s+fill:', 'Style declarations'),
]

class ValidationError:
    def __init__(self, process_id: str, error_type: str, message: str, details: str = ""):
        self.process_id = process_id
        self.error_type = error_type
        self.message = message
        self.details = details
    
    def __str__(self):
        return f"[{self.error_type}] {self.process_id}: {self.message}" + (f" ({self.details})" if self.details else "")


def fetch_json(url: str) -> Tuple[Dict, str]:
    """Fetch JSON from URL, return (data, error_message)"""
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            content = response.read().decode('utf-8')
            return json.loads(content), None
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}: {e.reason}"
    except urllib.error.URLError as e:
        return None, f"URL Error: {str(e)}"
    except json.JSONDecodeError as e:
        return None, f"JSON Parse Error: {str(e)}"
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"


def validate_json_structure(process_data: Dict, process_id: str) -> List[ValidationError]:
    """Validate JSON structure and required fields"""
    errors = []
    
    # Check required fields
    for field in REQUIRED_FIELDS:
        if field not in process_data:
            errors.append(ValidationError(
                process_id, 
                "MISSING_FIELD",
                f"Missing required field: {field}"
            ))
    
    # Validate field types
    if 'mermaid' in process_data:
        if not isinstance(process_data['mermaid'], str):
            errors.append(ValidationError(
                process_id,
                "INVALID_TYPE",
                "Field 'mermaid' must be a string"
            ))
        elif len(process_data['mermaid'].strip()) == 0:
            errors.append(ValidationError(
                process_id,
                "EMPTY_MERMAID",
                "Mermaid flowchart is empty"
            ))
    
    if 'sources' in process_data:
        if not isinstance(process_data['sources'], list):
            errors.append(ValidationError(
                process_id,
                "INVALID_TYPE",
                "Field 'sources' must be a list"
            ))
    
    # Validate ID matches
    if 'id' in process_data and process_id != process_data['id']:
        errors.append(ValidationError(
            process_id,
            "ID_MISMATCH",
            f"Process ID mismatch: expected '{process_id}', got '{process_data.get('id')}'"
        ))
    
    return errors


def extract_node_ids(mermaid_code: str) -> Dict[str, List[str]]:
    """Extract all node IDs from Mermaid code, return {node_id: [lines where it appears]}"""
    node_ids = {}
    lines = mermaid_code.split('\n')
    
    # Pattern to match node definitions: ID[Label] or ID{Label} or ID(Label)
    node_patterns = [
        r'(\w+)\s*\[[^\]]+\]',  # Rectangle: A[Label]
        r'(\w+)\s*\{[^\}]+\}',  # Diamond: A{Label}
        r'(\w+)\s*\([^\)]+\)',  # Round: A(Label)
    ]
    
    for i, line in enumerate(lines, 1):
        line = line.strip()
        if not line or line.startswith('//') or line.startswith('%%') or line.startswith('style'):
            continue
        
        # Check for node definitions
        for pattern in node_patterns:
            matches = re.finditer(pattern, line)
            for match in matches:
                node_id = match.group(1)
                if node_id not in node_ids:
                    node_ids[node_id] = []
                node_ids[node_id].append(i)
        
        # Also check for node IDs in edges: A --> B
        edge_pattern = r'(\w+)\s*(?:-->|--|==>|==)'
        matches = re.finditer(edge_pattern, line)
        for match in matches:
            node_id = match.group(1)
            if node_id not in node_ids:
                node_ids[node_id] = []
            node_ids[node_id].append(i)
    
    return node_ids


def extract_gate_info(mermaid_code: str) -> Dict[str, Dict]:
    """Extract gate information: node_id -> {type, inputs, outputs, color, shape}"""
    gates = {}
    lines = mermaid_code.split('\n')
    
    # Extract node definitions
    node_defs = {}  # node_id -> {shape, label, line}
    for i, line in enumerate(lines, 1):
        line = line.strip()
        if not line or line.startswith('//') or line.startswith('%%'):
            continue
        
        # Rectangle: A[Label]
        match = re.search(r'(\w+)\s*\[([^\]]+)\]', line)
        if match:
            node_id, label = match.groups()
            node_defs[node_id] = {'shape': 'rectangle', 'label': label, 'line': i}
        
        # Diamond: A{Label}
        match = re.search(r'(\w+)\s*\{([^\}]+)\}', line)
        if match:
            node_id, label = match.groups()
            node_defs[node_id] = {'shape': 'diamond', 'label': label, 'line': i}
        
        # Round: A(Label)
        match = re.search(r'(\w+)\s*\(([^\)]+)\)', line)
        if match:
            node_id, label = match.groups()
            node_defs[node_id] = {'shape': 'round', 'label': label, 'line': i}
    
    # Extract edges to count inputs/outputs
    edges = []  # (from, to, line)
    for i, line in enumerate(lines, 1):
        line = line.strip()
        if not line or line.startswith('//') or line.startswith('%%'):
            continue
        
        # Match edges: A --> B or A -->|label| B
        match = re.search(r'(\w+)\s*(?:-->|--|==>|==)\|?[^\|]*\|?\s*(\w+)', line)
        if match:
            from_node, to_node = match.groups()
            edges.append((from_node, to_node, i))
    
    # Count inputs and outputs for each node
    for node_id in node_defs:
        inputs = [e[0] for e in edges if e[1] == node_id]
        outputs = [e[1] for e in edges if e[0] == node_id]
        gates[node_id] = {
            'inputs': len(inputs),
            'outputs': len(outputs),
            'shape': node_defs[node_id]['shape'],
            'label': node_defs[node_id]['label'],
            'line': node_defs[node_id]['line']
        }
    
    # Extract color from style declarations
    for i, line in enumerate(lines, 1):
        if line.strip().startswith('style'):
            # style A fill:#ff6b6b
            match = re.search(r'style\s+(\w+)\s+fill:([#\w]+)', line)
            if match:
                node_id, color = match.groups()
                if node_id in gates:
                    gates[node_id]['color'] = color
    
    return gates


def validate_mermaid_syntax(mermaid_code: str, process_id: str) -> List[ValidationError]:
    """Enhanced Mermaid syntax validation with duplicate node checks"""
    errors = []
    
    if not mermaid_code or not mermaid_code.strip():
        errors.append(ValidationError(
            process_id,
            "MERMAID_EMPTY",
            "Mermaid code is empty or whitespace only"
        ))
        return errors
    
    # Check for graph declaration
    has_graph_declaration = False
    for pattern, name in MERMAID_ERROR_PATTERNS:
        if re.search(pattern, mermaid_code, re.IGNORECASE):
            has_graph_declaration = True
            break
    
    if not has_graph_declaration:
        errors.append(ValidationError(
            process_id,
            "MERMAID_SYNTAX",
            "Missing graph declaration (graph TD, graph LR, etc.)"
        ))
    
    # Check for duplicate node IDs
    node_ids = extract_node_ids(mermaid_code)
    duplicates = {node_id: lines for node_id, lines in node_ids.items() if len(lines) > 1}
    if duplicates:
        for node_id, lines in duplicates.items():
            errors.append(ValidationError(
                process_id,
                "DUPLICATE_NODE_ID",
                f"Node ID '{node_id}' appears multiple times",
                f"Found on lines: {', '.join(map(str, lines))}"
            ))
    
    # Check for common syntax issues
    lines = mermaid_code.split('\n')
    for i, line in enumerate(lines, 1):
        line = line.strip()
        if not line or line.startswith('//') or line.startswith('%%'):
            continue
        
        # Check for unclosed brackets
        if line.count('[') != line.count(']'):
            errors.append(ValidationError(
                process_id,
                "MERMAID_SYNTAX",
                f"Unclosed brackets in line {i}: {line[:50]}"
            ))
        
        # Check for unclosed parentheses
        if line.count('(') != line.count(')'):
            errors.append(ValidationError(
                process_id,
                "MERMAID_SYNTAX",
                f"Unclosed parentheses in line {i}: {line[:50]}"
            ))
        
        # Check for unclosed braces
        if line.count('{') != line.count('}'):
            errors.append(ValidationError(
                process_id,
                "MERMAID_SYNTAX",
                f"Unclosed braces in line {i}: {line[:50]}"
            ))
    
    # Check for at least one node definition
    node_pattern = r'\w+\s*\[[^\]]+\]|\w+\s*\{[^\}]+\}|\w+\s*\([^\)]+\)'
    if not re.search(node_pattern, mermaid_code):
        errors.append(ValidationError(
            process_id,
            "MERMAID_SYNTAX",
            "No valid node definitions found"
        ))
    
    return errors


def validate_gate_types(mermaid_code: str, process_id: str) -> List[ValidationError]:
    """Validate logic gate types (OR vs AND) based on input/output structure"""
    errors = []
    gates = extract_gate_info(mermaid_code)
    
    # Expected color codes
    OR_GATE_COLOR = '#ff9f43'  # Orange
    AND_GATE_COLOR = '#b4b4dc'  # Lavender (or #c3a6ff)
    NOT_GATE_COLOR = '#e74c3c'  # Red
    
    for node_id, gate_info in gates.items():
        inputs = gate_info['inputs']
        outputs = gate_info['outputs']
        shape = gate_info['shape']
        label = gate_info.get('label', '')
        color = gate_info.get('color', '')
        line = gate_info.get('line', 0)
        
        # Only check diamond-shaped nodes (gates)
        if shape != 'diamond':
            continue
        
        # Check for gates with multiple inputs + single output (should be AND, not OR)
        if inputs > 1 and outputs == 1:
            # This should be an AND gate
            if color == OR_GATE_COLOR:
                errors.append(ValidationError(
                    process_id,
                    "GATE_TYPE_ERROR",
                    f"Node '{node_id}' has {inputs} inputs and 1 output (should be AND gate, not OR)",
                    f"Line {line}: {label[:50]}"
                ))
        
        # Check for gates incorrectly designated as NO/STOP
        label_lower = label.lower()
        is_no_stop = any(term in label_lower for term in ['no ', 'stop', 'block', 'inhibit', 'prevent'])
        
        if is_no_stop and color != NOT_GATE_COLOR:
            # Check if it's actually a NOT gate or just a negative condition
            if '?' in label or '?' in label:
                # It's a decision gate, might be OK
                pass
            else:
                errors.append(ValidationError(
                    process_id,
                    "GATE_DESIGNATION_ERROR",
                    f"Node '{node_id}' appears to be NO/STOP gate but not properly designated",
                    f"Line {line}: {label[:50]}"
                ))
    
    return errors


def validate_colors(mermaid_code: str, process_id: str) -> List[ValidationError]:
    """Validate color assignments against expected color scheme"""
    errors = []
    gates = extract_gate_info(mermaid_code)
    
    # Expected colors from color scheme
    VALID_COLORS = {
        '#ff6b6b': 'Red - Triggers & Inputs',
        '#ffd43b': 'Yellow - Structures & Objects',
        '#51cf66': 'Green - Processing & Operations',
        '#74c0fc': 'Blue - Intermediates & States',
        '#ff9f43': 'Orange - OR Logic Gates',
        '#b4b4dc': 'Lavender - AND Logic Gates',
        '#c3a6ff': 'Lavender (alt) - AND Logic Gates',
        '#e74c3c': 'Red - NOT Logic Gates',
        '#b197fc': 'Violet - Products & Outputs',
        '#000000': 'Black - Terminal outputs',
    }
    
    # Extract style declarations
    lines = mermaid_code.split('\n')
    for i, line in enumerate(lines, 1):
        if line.strip().startswith('style'):
            match = re.search(r'style\s+(\w+)\s+fill:([#\w]+)', line)
            if match:
                node_id, color = match.groups()
                if color not in VALID_COLORS:
                    errors.append(ValidationError(
                        process_id,
                        "INVALID_COLOR",
                        f"Node '{node_id}' has invalid color: {color}",
                        f"Line {i}: Expected one of {list(VALID_COLORS.keys())}"
                    ))
    
    return errors


def validate_process(process_id: str, organism: str) -> List[ValidationError]:
    """Validate a single process"""
    errors = []
    
    # Construct URL
    process_url = f"{PROCESSES_BASE_URL}{organism}/{process_id}.json"
    
    # Fetch process data
    process_data, fetch_error = fetch_json(process_url)
    if fetch_error:
        errors.append(ValidationError(
            process_id,
            "FETCH_ERROR",
            f"Failed to fetch process: {fetch_error}",
            process_url
        ))
        return errors
    
    # Validate JSON structure
    errors.extend(validate_json_structure(process_data, process_id))
    
    # Validate Mermaid syntax
    if 'mermaid' in process_data:
        errors.extend(validate_mermaid_syntax(process_data['mermaid'], process_id))
        errors.extend(validate_gate_types(process_data['mermaid'], process_id))
        errors.extend(validate_colors(process_data['mermaid'], process_id))
    
    return errors


def main():
    """Main validation function"""
    print("🔍 GLMP Collection Validator")
    print("=" * 80)
    print()
    
    # Fetch metadata
    print("📥 Fetching metadata...")
    metadata, error = fetch_json(METADATA_URL)
    if error:
        print(f"❌ Failed to fetch metadata: {error}")
        sys.exit(1)
    
    processes = metadata.get('processes', [])
    print(f"✅ Found {len(processes)} processes to validate\n")
    
    # Validate each process
    all_errors = []
    processes_by_organism = {}
    
    for i, process in enumerate(processes, 1):
        process_id = process.get('id', f'unknown_{i}')
        organism = process.get('organism', 'unknown').lower().replace(' ', '_').replace('.', '')
        if 'ecoli' in organism or 'e. coli' in organism.lower():
            organism = 'ecoli'
        elif 'yeast' in organism or 's. cerevisiae' in organism.lower():
            organism = 'yeast'
        
        print(f"[{i}/{len(processes)}] Validating {process_id}...", end=' ')
        
        errors = validate_process(process_id, organism)
        
        if errors:
            print(f"❌ {len(errors)} error(s)")
            all_errors.extend(errors)
        else:
            print("✅ OK")
        
        # Track by organism
        if organism not in processes_by_organism:
            processes_by_organism[organism] = {'total': 0, 'errors': 0}
        processes_by_organism[organism]['total'] += 1
        if errors:
            processes_by_organism[organism]['errors'] += 1
    
    # Print summary
    print()
    print("=" * 80)
    print("📊 VALIDATION SUMMARY")
    print("=" * 80)
    print(f"Total Processes: {len(processes)}")
    print(f"Processes with Errors: {len(set(e.process_id for e in all_errors))}")
    print(f"Total Errors: {len(all_errors)}")
    print()
    
    # Errors by organism
    if processes_by_organism:
        print("By Organism:")
        for org, stats in processes_by_organism.items():
            print(f"  {org}: {stats['total']} processes, {stats['errors']} with errors")
        print()
    
    # Errors by type
    if all_errors:
        error_types = {}
        for error in all_errors:
            error_types[error.error_type] = error_types.get(error.error_type, 0) + 1
        
        print("Errors by Type:")
        for error_type, count in sorted(error_types.items(), key=lambda x: -x[1]):
            print(f"  {error_type}: {count}")
        print()
        
        # Print detailed errors
        print("=" * 80)
        print("📋 DETAILED ERROR REPORT")
        print("=" * 80)
        for error in all_errors:
            print(error)
            if error.details:
                print(f"    Details: {error.details}")
        print()
        
        # Save report to file
        report = {
            'total_processes': len(processes),
            'processes_with_errors': len(set(e.process_id for e in all_errors)),
            'total_errors': len(all_errors),
            'errors_by_type': error_types,
            'errors': [
                {
                    'process_id': e.process_id,
                    'error_type': e.error_type,
                    'message': e.message,
                    'details': e.details
                }
                for e in all_errors
            ]
        }
        
        with open('validation_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"📄 Detailed report saved to: validation_report.json")
        sys.exit(1)
    else:
        print("✅ All processes validated successfully!")
        sys.exit(0)


if __name__ == '__main__':
    main()

