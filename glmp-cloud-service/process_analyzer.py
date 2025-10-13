"""
Process Analyzer - Extract Logic Gates and Metrics from Mermaid Flowcharts
Analyzes biological processes to quantify computational structure
"""

import re
import json
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)


class MermaidLogicAnalyzer:
    """Analyze Mermaid flowcharts for logic gates and computational patterns"""
    
    def __init__(self):
        self.node_pattern = re.compile(r'([A-Z][A-Z0-9]*)\[([^\]]+)\]|\{([^}]+)\}')
        self.edge_pattern = re.compile(r'([A-Z][A-Z0-9]*)\s*-->(\|[^|]+\|)?\s*([A-Z][A-Z0-9]*)')
        self.style_pattern = re.compile(r'style\s+([A-Z][A-Z0-9]*)\s+fill:#([0-9a-fA-F]+)')
        
    def analyze_process(self, process_data):
        """
        Complete analysis of a biological process
        
        Args:
            process_data: Process JSON dict
        
        Returns:
            Analysis dict with all metrics
        """
        mermaid = process_data.get('mermaid', '')
        
        analysis = {
            'process_id': process_data.get('id'),
            'process_name': process_data.get('name'),
            'organism': process_data.get('organism'),
            'nodes': self.extract_nodes(mermaid),
            'edges': self.extract_edges(mermaid),
            'logic_gates': self.identify_logic_gates(mermaid),
            'colors': self.extract_color_scheme(mermaid),
            'complexity': self.calculate_complexity(mermaid),
            'patterns': self.detect_patterns(mermaid),
            'citations': len(process_data.get('sources', []))
        }
        
        # Add gate counts
        analysis['gate_counts'] = {
            'or_gates': len(analysis['logic_gates']['or_gates']),
            'and_gates': len(analysis['logic_gates']['and_gates']),
            'total_gates': len(analysis['logic_gates']['or_gates']) + len(analysis['logic_gates']['and_gates'])
        }
        
        # Add node count
        analysis['node_count'] = len(analysis['nodes'])
        
        return analysis
    
    def extract_nodes(self, mermaid):
        """Extract all nodes with their types and labels"""
        nodes = {}
        
        # Find rectangle nodes: A[Label]
        rect_pattern = re.compile(r'([A-Z][A-Z0-9]*)\[([^\]]+)\]')
        for match in rect_pattern.finditer(mermaid):
            node_id = match.group(1)
            label = match.group(2)
            nodes[node_id] = {
                'id': node_id,
                'label': label,
                'type': 'process',
                'shape': 'rectangle'
            }
        
        # Find diamond nodes: A{Label}
        diamond_pattern = re.compile(r'([A-Z][A-Z0-9]*)\{([^}]+)\}')
        for match in diamond_pattern.finditer(mermaid):
            node_id = match.group(1)
            label = match.group(2)
            nodes[node_id] = {
                'id': node_id,
                'label': label,
                'type': 'decision',
                'shape': 'diamond'
            }
        
        return nodes
    
    def extract_edges(self, mermaid):
        """Extract all edges (connections between nodes)"""
        edges = []
        
        edge_pattern = re.compile(r'([A-Z][A-Z0-9]*)\s*-->(\|[^|]+\|)?\s*([A-Z][A-Z0-9]*)')
        
        for match in edge_pattern.finditer(mermaid):
            source = match.group(1)
            label = match.group(2).strip('|') if match.group(2) else None
            target = match.group(3)
            
            edges.append({
                'source': source,
                'target': target,
                'label': label
            })
        
        return edges
    
    def identify_logic_gates(self, mermaid):
        """Identify OR gates, AND gates, and composite gates"""
        nodes = self.extract_nodes(mermaid)
        edges = self.extract_edges(mermaid)
        
        # Count incoming edges for each node
        incoming = defaultdict(list)
        outgoing = defaultdict(list)
        
        for edge in edges:
            incoming[edge['target']].append(edge)
            outgoing[edge['source']].append(edge)
        
        or_gates = []
        and_gates = []
        
        for node_id, node_data in nodes.items():
            if node_data['shape'] == 'diamond':
                in_count = len(incoming.get(node_id, []))
                out_count = len(outgoing.get(node_id, []))
                
                # OR gate: Single input, binary output (yes/no)
                if in_count <= 1 and out_count >= 2:
                    or_gates.append({
                        'id': node_id,
                        'label': node_data['label'],
                        'inputs': in_count,
                        'outputs': out_count
                    })
                
                # AND gate: Multiple inputs converge
                elif in_count >= 2:
                    and_gates.append({
                        'id': node_id,
                        'label': node_data['label'],
                        'inputs': in_count,
                        'outputs': out_count
                    })
        
        return {
            'or_gates': or_gates,
            'and_gates': and_gates,
            'total_gates': len(or_gates) + len(and_gates)
        }
    
    def extract_color_scheme(self, mermaid):
        """Extract color coding for each node"""
        colors = {}
        
        style_pattern = re.compile(r'style\s+([A-Z][A-Z0-9]*)\s+fill:#([0-9a-fA-F]+)')
        
        for match in style_pattern.finditer(mermaid):
            node_id = match.group(1)
            color = f"#{match.group(2)}"
            colors[node_id] = color
        
        # Count by color
        color_distribution = defaultdict(int)
        for color in colors.values():
            color_distribution[color] += 1
        
        return {
            'node_colors': colors,
            'distribution': dict(color_distribution)
        }
    
    def calculate_complexity(self, mermaid):
        """Calculate complexity metrics"""
        nodes = self.extract_nodes(mermaid)
        edges = self.extract_edges(mermaid)
        gates = self.identify_logic_gates(mermaid)
        
        # Build adjacency for graph analysis
        incoming = defaultdict(list)
        outgoing = defaultdict(list)
        
        for edge in edges:
            incoming[edge['target']].append(edge['source'])
            outgoing[edge['source']].append(edge['target'])
        
        # Calculate metrics
        max_fan_in = max([len(incoming[n]) for n in nodes.keys()]) if nodes else 0
        max_fan_out = max([len(outgoing[n]) for n in nodes.keys()]) if nodes else 0
        
        # Estimate depth (longest path)
        depth = self._estimate_depth(nodes, edges)
        
        return {
            'node_count': len(nodes),
            'edge_count': len(edges),
            'gate_count': gates['total_gates'],
            'max_fan_in': max_fan_in,
            'max_fan_out': max_fan_out,
            'estimated_depth': depth,
            'complexity_score': self._complexity_score(len(nodes), len(edges), gates['total_gates'])
        }
    
    def _estimate_depth(self, nodes, edges):
        """Estimate maximum depth of flowchart"""
        # Simple heuristic: count sequential stages
        # A better implementation would do topological sort
        return min(len(nodes) // 5, 20)  # Rough estimate
    
    def _complexity_score(self, nodes, edges, gates):
        """Calculate overall complexity score (0-10)"""
        # Weighted combination of factors
        node_score = min(nodes / 50, 1) * 4  # 0-4 points for nodes
        edge_score = min(edges / 60, 1) * 3  # 0-3 points for edges
        gate_score = min(gates / 10, 1) * 3  # 0-3 points for gates
        
        return round(node_score + edge_score + gate_score, 2)
    
    def detect_patterns(self, mermaid):
        """Detect higher-order patterns"""
        nodes = self.extract_nodes(mermaid)
        edges = self.extract_edges(mermaid)
        gates = self.identify_logic_gates(mermaid)
        
        patterns = {
            'feedback_loops': self._detect_feedback_loops(edges),
            'parallel_paths': self._detect_parallel_paths(edges),
            'sequential_gates': self._detect_sequential_gates(gates, edges),
            'branching_factor': self._calculate_branching_factor(edges)
        }
        
        return patterns
    
    def _detect_feedback_loops(self, edges):
        """Detect feedback loops in the process"""
        # Build graph
        graph = defaultdict(list)
        for edge in edges:
            graph[edge['source']].append(edge['target'])
        
        # Simple cycle detection (rough heuristic)
        loops = []
        visited = set()
        
        for edge in edges:
            if edge['target'] in graph and edge['source'] in graph[edge['target']]:
                loops.append([edge['source'], edge['target']])
        
        return loops
    
    def _detect_parallel_paths(self, edges):
        """Detect parallel pathways"""
        # Find nodes with multiple outgoing edges
        outgoing = defaultdict(list)
        for edge in edges:
            outgoing[edge['source']].append(edge['target'])
        
        parallel = [node for node, targets in outgoing.items() if len(targets) > 2]
        return len(parallel)
    
    def _detect_sequential_gates(self, gates, edges):
        """Detect gates that feed into other gates"""
        gate_ids = set([g['id'] for g in gates['or_gates']] + [g['id'] for g in gates['and_gates']])
        
        sequential = 0
        for edge in edges:
            if edge['source'] in gate_ids and edge['target'] in gate_ids:
                sequential += 1
        
        return sequential
    
    def _calculate_branching_factor(self, edges):
        """Average branching factor"""
        outgoing = defaultdict(int)
        for edge in edges:
            outgoing[edge['source']] += 1
        
        if not outgoing:
            return 0
        
        return round(sum(outgoing.values()) / len(outgoing), 2)


class ProcessDatabaseBuilder:
    """Build structured database from process collection"""
    
    def __init__(self, analyzer=None):
        self.analyzer = analyzer or MermaidLogicAnalyzer()
    
    def analyze_all_processes(self, processes):
        """
        Analyze all processes and generate database records
        
        Args:
            processes: List of process JSON dicts
        
        Returns:
            Database-ready records
        """
        records = []
        
        for process in processes:
            analysis = self.analyzer.analyze_process(process)
            
            record = {
                'id': process.get('id'),
                'name': process.get('name'),
                'organism': process.get('organism'),
                'category': process.get('category'),
                'created': process.get('created'),
                'verified': process.get('verified'),
                
                # Quantitative metrics
                'node_count': analysis['node_count'],
                'edge_count': analysis['complexity']['edge_count'],
                'or_gates': analysis['gate_counts']['or_gates'],
                'and_gates': analysis['gate_counts']['and_gates'],
                'total_gates': analysis['gate_counts']['total_gates'],
                'complexity_score': analysis['complexity']['complexity_score'],
                
                # Pattern metrics
                'feedback_loops': len(analysis['patterns']['feedback_loops']),
                'parallel_paths': analysis['patterns']['parallel_paths'],
                'sequential_gates': analysis['patterns']['sequential_gates'],
                'branching_factor': analysis['patterns']['branching_factor'],
                
                # Metadata
                'citations': analysis['citations'],
                'max_fan_in': analysis['complexity']['max_fan_in'],
                'max_fan_out': analysis['complexity']['max_fan_out'],
                'estimated_depth': analysis['complexity']['estimated_depth'],
                
                # Full analysis
                'full_analysis': analysis
            }
            
            records.append(record)
        
        return records
    
    def generate_statistics(self, records):
        """Generate statistical summary of all processes"""
        if not records:
            return {}
        
        total = len(records)
        
        stats = {
            'total_processes': total,
            'total_nodes': sum(r['node_count'] for r in records),
            'total_gates': sum(r['total_gates'] for r in records),
            'total_or_gates': sum(r['or_gates'] for r in records),
            'total_and_gates': sum(r['and_gates'] for r in records),
            'total_citations': sum(r['citations'] for r in records),
            
            'avg_nodes_per_process': round(sum(r['node_count'] for r in records) / total, 2),
            'avg_gates_per_process': round(sum(r['total_gates'] for r in records) / total, 2),
            'avg_complexity': round(sum(r['complexity_score'] for r in records) / total, 2),
            
            'max_complexity': max(r['complexity_score'] for r in records),
            'min_complexity': min(r['complexity_score'] for r in records),
            
            'organisms': list(set(r['organism'] for r in records)),
            'categories': list(set(r['category'] for r in records))
        }
        
        return stats
    
    def export_to_csv(self, records, filename='process_database.csv'):
        """Export records to CSV format"""
        import csv
        
        if not records:
            return False
        
        keys = ['id', 'name', 'organism', 'category', 'node_count', 'or_gates', 
                'and_gates', 'total_gates', 'complexity_score', 'citations',
                'feedback_loops', 'parallel_paths', 'branching_factor']
        
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            
            for record in records:
                row = {k: record.get(k, '') for k in keys}
                writer.writerow(row)
        
        logger.info(f"✓ Exported {len(records)} records to {filename}")
        return True
    
    def export_to_json(self, records, filename='process_database.json'):
        """Export full analysis to JSON"""
        with open(filename, 'w') as f:
            json.dump(records, f, indent=2)
        
        logger.info(f"✓ Exported {len(records)} records to {filename}")
        return True


# Global instance
analyzer = None

def get_analyzer():
    """Get or create analyzer instance"""
    global analyzer
    if analyzer is None:
        analyzer = MermaidLogicAnalyzer()
    return analyzer
