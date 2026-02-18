#!/usr/bin/env python3
"""
Logical Structure Analyzer for GLMP Biological Processes
Automatically detects and counts logical structures in Mermaid diagrams
"""

import re
import json
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass

@dataclass
class LogicalStructure:
    """Represents a detected logical structure in a biological process"""
    structure_type: str
    count: int
    locations: List[str]  # Node IDs where found
    confidence: float     # 0-1 confidence score

class BiologicalLogicAnalyzer:
    def __init__(self):
        """Initialize the logical structure analyzer"""
        
        # Define logical structure patterns
        self.logic_patterns = {
            'AND_GATE': {
                'mermaid_patterns': [
                    r'(\w+)\s*-->\s*(\w+)\s*{\s*.*?\s*}',  # Multiple inputs to decision
                    r'(\w+)\s*-->\s*(\w+).*?(\w+)\s*-->\s*\2',  # Multiple converging paths
                ],
                'node_patterns': [
                    r'{\s*.*?(AND|&|∧).*?\s*}',  # Explicit AND in decision nodes
                    r'{\s*.*?(Both|All).*?\s*}',  # Natural language AND
                ],
                'description': 'Multiple conditions must be true'
            },
            
            'OR_GATE': {
                'mermaid_patterns': [
                    r'(\w+)\s*-->\|([^|]+)\|\s*(\w+)',  # Decision branches with labels
                    r'(\w+)\s*{\s*.*?\?\s*}',  # Decision diamond nodes
                ],
                'node_patterns': [
                    r'{\s*.*?(OR|\|).*?\s*}',  # Explicit OR in decision nodes
                    r'{\s*.*?(Either|Alternative).*?\s*}',  # Natural language OR
                ],
                'description': 'Alternative pathways or conditions'
            },
            
            'FEEDBACK_LOOP': {
                'mermaid_patterns': [
                    r'(\w+).*?-->\s*(\w+).*?-->\s*.*?\1',  # Circular reference
                    r'(\w+).*?Feedback.*?-->\s*(\w+)',  # Explicit feedback
                ],
                'node_patterns': [
                    r'\[.*?(Feedback|Auto.*regulation|Loop).*?\]',
                    r'\[.*?(Positive|Negative).*?(Feedback|Loop).*?\]',
                ],
                'description': 'Self-reinforcing or self-regulating circuits'
            },
            
            'CHECKPOINT': {
                'mermaid_patterns': [
                    r'{\s*.*?(Complete|Ready|Check).*?\?\s*}',  # Checkpoint decisions
                    r'-->\|.*?(Yes|No|Pass|Fail).*?\|',  # Checkpoint outcomes
                ],
                'node_patterns': [
                    r'\[.*?(Checkpoint|Control|Quality.*Control).*?\]',
                    r'{\s*.*?(Adequate|Sufficient|Ready).*?\?\s*}',
                ],
                'description': 'Quality control and verification points'
            },
            
            'BISTABLE_SWITCH': {
                'mermaid_patterns': [
                    r'(\w+)\s*-->\s*(\w+)\s*-->\s*\1',  # Mutual regulation
                    r'{\s*.*?(High|Low).*?\}.*?{\s*.*?(Low|High).*?\}',  # Binary states
                ],
                'node_patterns': [
                    r'\[.*?(Switch|Toggle|Bistable).*?\]',
                    r'{\s*.*?(On|Off|Active|Inactive).*?\?\s*}',
                ],
                'description': 'Binary state switches with memory'
            },
            
            'AMPLIFICATION': {
                'mermaid_patterns': [
                    r'(\w+).*?-->\s*(\w+).*?-->\s*.*?\1.*?(Amplification|Enhancement)',
                    r'\[.*?(More|Increased|Enhanced).*?\].*?-->\s*\[.*?\1.*?\]',
                ],
                'node_patterns': [
                    r'\[.*?(Amplification|Enhancement|Accumulation).*?\]',
                    r'\[.*?(More|Increased|Enhanced).*?\]',
                ],
                'description': 'Signal or response amplification'
            },
            
            'COMPETITIVE_INHIBITION': {
                'mermaid_patterns': [
                    r'(\w+).*?vs.*?(\w+).*?Competition',
                    r'(\w+).*?-->\s*(\w+).*?(\w+).*?-->\s*\2',  # Competition for same target
                ],
                'node_patterns': [
                    r'\[.*?(Competition|Competitive|vs|Inhibition).*?\]',
                    r'{\s*.*?(Higher|Lower|Stronger).*?\?\s*}',
                ],
                'description': 'Competitive binding or inhibition'
            },
            
            'CASCADE': {
                'mermaid_patterns': [
                    r'(\w+)\s*-->\s*(\w+)\s*-->\s*(\w+)\s*-->\s*(\w+)',  # Sequential chain
                    r'\[.*?Cascade.*?\]',
                ],
                'node_patterns': [
                    r'\[.*?(Cascade|Sequential|Chain).*?\]',
                    r'\[.*?(Step|Stage|Phase).*?[0-9].*?\]',
                ],
                'description': 'Sequential activation chains'
            },
            
            'OSCILLATION': {
                'mermaid_patterns': [
                    r'(\w+).*?Oscillation.*?-->\s*(\w+)',
                    r'(\w+).*?-->\s*(\w+).*?-->\s*\1.*?(Cycle|Oscillat)',
                ],
                'node_patterns': [
                    r'\[.*?(Oscillation|Oscillatory|Cycle|Cycling).*?\]',
                    r'\[.*?(Dynamic|Rhythmic|Periodic).*?\]',
                ],
                'description': 'Rhythmic or cyclical behavior'
            }
        }

    def analyze_mermaid_diagram(self, mermaid_code: str) -> Dict[str, LogicalStructure]:
        """
        Analyze a Mermaid diagram for logical structures
        
        Args:
            mermaid_code: The Mermaid diagram code as string
            
        Returns:
            Dictionary of detected logical structures
        """
        detected_structures = {}
        
        for structure_name, patterns in self.logic_patterns.items():
            locations = []
            total_matches = 0
            
            # Check Mermaid syntax patterns
            for pattern in patterns['mermaid_patterns']:
                matches = re.finditer(pattern, mermaid_code, re.IGNORECASE)
                for match in matches:
                    locations.append(f"Line: {match.group()}")
                    total_matches += 1
            
            # Check node content patterns
            for pattern in patterns['node_patterns']:
                matches = re.finditer(pattern, mermaid_code, re.IGNORECASE)
                for match in matches:
                    locations.append(f"Node: {match.group()}")
                    total_matches += 1
            
            if total_matches > 0:
                # Calculate confidence based on pattern strength and count
                confidence = min(1.0, (total_matches * 0.3) + 0.4)
                
                detected_structures[structure_name] = LogicalStructure(
                    structure_type=structure_name,
                    count=total_matches,
                    locations=locations[:5],  # Limit to first 5 for brevity
                    confidence=confidence
                )
        
        return detected_structures

    def analyze_process_file(self, file_path: str) -> Dict[str, any]:
        """
        Analyze an entire HTML file with multiple processes
        
        Args:
            file_path: Path to the HTML file
            
        Returns:
            Analysis results for all processes in the file
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract process data from JavaScript
            js_match = re.search(r'const allProcesses\s*=\s*({.*?});', content, re.DOTALL)
            if not js_match:
                return {"error": "No allProcesses JavaScript object found"}
            
            # Extract file metadata
            title_match = re.search(r'<title>(.*?)</title>', content)
            organism_match = re.search(r'(E\. coli|Yeast|Human|D\. melanogaster)', content, re.IGNORECASE)
            
            file_info = {
                "file_path": file_path,
                "title": title_match.group(1) if title_match else "Unknown",
                "organism": organism_match.group(1) if organism_match else "Unknown",
                "total_processes": 0,
                "logical_structures_summary": {},
                "process_details": {}
            }
            
            # Extract individual process levels
            process_pattern = r'(\d+):\s*{.*?levels:\s*{(.*?)}\s*}'
            processes = re.finditer(process_pattern, js_match.group(1), re.DOTALL)
            
            for process_match in processes:
                process_id = process_match.group(1)
                levels_content = process_match.group(2)
                
                # Extract Mermaid diagrams for each level
                level_pattern = r'(\d+):\s*`([^`]+)`'
                levels = re.findall(level_pattern, levels_content, re.DOTALL)
                
                process_structures = {}
                for level_num, mermaid_code in levels:
                    structures = self.analyze_mermaid_diagram(mermaid_code)
                    if structures:
                        process_structures[f"level_{level_num}"] = structures
                
                if process_structures:
                    file_info["process_details"][process_id] = process_structures
                    file_info["total_processes"] += 1
            
            # Create summary statistics
            all_structures = {}
            for process_data in file_info["process_details"].values():
                for level_data in process_data.values():
                    for structure_name, structure_obj in level_data.items():
                        if structure_name not in all_structures:
                            all_structures[structure_name] = {
                                "total_count": 0,
                                "process_count": 0,
                                "avg_confidence": 0
                            }
                        all_structures[structure_name]["total_count"] += structure_obj.count
                        all_structures[structure_name]["process_count"] += 1
                        all_structures[structure_name]["avg_confidence"] += structure_obj.confidence
            
            # Calculate averages
            for structure_data in all_structures.values():
                if structure_data["process_count"] > 0:
                    structure_data["avg_confidence"] /= structure_data["process_count"]
            
            file_info["logical_structures_summary"] = all_structures
            
            return file_info
            
        except Exception as e:
            return {"error": f"Analysis failed: {str(e)}"}

    def generate_database_entry(self, analysis_result: Dict) -> Dict:
        """
        Generate database entry with logical structure counts
        
        Args:
            analysis_result: Result from analyze_process_file
            
        Returns:
            Database-compatible entry
        """
        if "error" in analysis_result:
            return analysis_result
        
        # Create logical structure counts for database
        logic_counts = {}
        for structure_name, data in analysis_result["logical_structures_summary"].items():
            logic_counts[f"{structure_name.lower()}_count"] = data["total_count"]
            logic_counts[f"{structure_name.lower()}_confidence"] = round(data["avg_confidence"], 2)
        
        return {
            "file_path": analysis_result["file_path"],
            "organism": analysis_result["organism"],
            "total_processes": analysis_result["total_processes"],
            "has_and_gates": logic_counts.get("and_gate_count", 0) > 0,
            "has_or_gates": logic_counts.get("or_gate_count", 0) > 0,
            "has_feedback_loops": logic_counts.get("feedback_loop_count", 0) > 0,
            "has_checkpoints": logic_counts.get("checkpoint_count", 0) > 0,
            "has_bistable_switches": logic_counts.get("bistable_switch_count", 0) > 0,
            "total_logic_structures": sum([
                logic_counts.get("and_gate_count", 0),
                logic_counts.get("or_gate_count", 0),
                logic_counts.get("feedback_loop_count", 0),
                logic_counts.get("checkpoint_count", 0),
                logic_counts.get("bistable_switch_count", 0),
                logic_counts.get("amplification_count", 0),
                logic_counts.get("competitive_inhibition_count", 0),
                logic_counts.get("cascade_count", 0),
                logic_counts.get("oscillation_count", 0)
            ]),
            "logic_complexity_score": self._calculate_complexity_score(logic_counts),
            **logic_counts
        }

    def _calculate_complexity_score(self, logic_counts: Dict) -> float:
        """Calculate a complexity score based on logical structures present"""
        weights = {
            'and_gate_count': 1.0,
            'or_gate_count': 1.0,
            'feedback_loop_count': 2.0,      # More complex
            'checkpoint_count': 1.5,
            'bistable_switch_count': 3.0,    # Most complex
            'amplification_count': 1.5,
            'competitive_inhibition_count': 2.0,
            'cascade_count': 1.0,
            'oscillation_count': 2.5
        }
        
        score = 0
        for structure, count in logic_counts.items():
            if structure in weights:
                score += count * weights[structure]
        
        return round(score, 2)

    def analyze_collection(self, folder_path: str) -> Dict:
        """
        Analyze an entire collection of biological process files
        
        Args:
            folder_path: Path to folder containing HTML files
            
        Returns:
            Complete analysis of the collection
        """
        import os
        import glob
        
        html_files = glob.glob(os.path.join(folder_path, "*.html"))
        
        collection_analysis = {
            "collection_path": folder_path,
            "total_files": len(html_files),
            "files_analyzed": 0,
            "total_processes": 0,
            "collection_logic_summary": {},
            "file_analyses": {}
        }
        
        all_logic_structures = {}
        
        for file_path in html_files:
            print(f"Analyzing: {os.path.basename(file_path)}")
            
            file_analysis = self.analyze_process_file(file_path)
            if "error" not in file_analysis:
                collection_analysis["files_analyzed"] += 1
                collection_analysis["total_processes"] += file_analysis["total_processes"]
                collection_analysis["file_analyses"][os.path.basename(file_path)] = file_analysis
                
                # Aggregate logical structures
                for structure_name, data in file_analysis["logical_structures_summary"].items():
                    if structure_name not in all_logic_structures:
                        all_logic_structures[structure_name] = {
                            "total_count": 0,
                            "file_count": 0,
                            "avg_confidence": 0
                        }
                    all_logic_structures[structure_name]["total_count"] += data["total_count"]
                    all_logic_structures[structure_name]["file_count"] += 1
                    all_logic_structures[structure_name]["avg_confidence"] += data["avg_confidence"]
        
        # Calculate collection averages
        for structure_data in all_logic_structures.values():
            if structure_data["file_count"] > 0:
                structure_data["avg_confidence"] /= structure_data["file_count"]
                structure_data["avg_confidence"] = round(structure_data["avg_confidence"], 2)
        
        collection_analysis["collection_logic_summary"] = all_logic_structures
        
        return collection_analysis

def main():
    """Example usage of the logical structure analyzer"""
    analyzer = BiologicalLogicAnalyzer()
    
    # Analyze E. coli collection
    print("🧬 Analyzing E. coli Collection...")
    ecoli_analysis = analyzer.analyze_collection("/workspace/biological_processes/ecoli/")
    
    print(f"\n📊 E. coli Collection Results:")
    print(f"Files analyzed: {ecoli_analysis['files_analyzed']}")
    print(f"Total processes: {ecoli_analysis['total_processes']}")
    
    print(f"\n🔍 Logical Structures Found:")
    for structure_name, data in ecoli_analysis["collection_logic_summary"].items():
        print(f"  {structure_name}: {data['total_count']} instances across {data['file_count']} files")
    
    # Generate database entries
    print(f"\n📋 Database Entries Generated:")
    for file_name, file_analysis in ecoli_analysis["file_analyses"].items():
        db_entry = analyzer.generate_database_entry(file_analysis)
        print(f"  {file_name}:")
        print(f"    Logic complexity score: {db_entry['logic_complexity_score']}")
        print(f"    Has AND gates: {db_entry['has_and_gates']}")
        print(f"    Has OR gates: {db_entry['has_or_gates']}")
        print(f"    Has feedback loops: {db_entry['has_feedback_loops']}")
        print(f"    Total logic structures: {db_entry['total_logic_structures']}")

if __name__ == "__main__":
    main()