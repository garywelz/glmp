#!/usr/bin/env python3
"""
GLMP System Demo
Demonstrates the complete Genome Logic Modeling Project AI agent system
"""

import os
import sys
import json
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from agents import AgentCoordinator, ExtractorAgent, DiagramSynthesizer

def create_sample_papers():
    """Create sample biological papers for demonstration."""
    papers = {
        "lac_operon.txt": """
        The lac operon is a classic example of gene regulation in bacteria. 
        When lactose is present in the environment, the repressor protein is inactivated, 
        allowing transcription of the lac genes to proceed. If glucose is also present, 
        cAMP levels are low, and the operon is only partially activated. 
        This creates a feedback loop where the system responds to environmental conditions. 
        The entire pathway functions as a genetic circuit that processes multiple inputs 
        and produces appropriate outputs based on the current state of the environment.
        """,
        
        "circadian_rhythm.txt": """
        Circadian rhythms are biological processes that follow a 24-hour cycle. 
        The circadian clock is controlled by a feedback loop involving several genes. 
        When light is detected, the clock genes are activated, which then inhibit 
        their own expression through a negative feedback mechanism. This creates 
        an oscillatory pattern that regulates various physiological processes. 
        The system operates as a molecular oscillator that maintains temporal 
        coordination of biological activities.
        """,
        
        "apoptosis.txt": """
        Apoptosis, or programmed cell death, is a tightly regulated process. 
        When cells receive death signals, they activate a cascade of proteases. 
        If the cell has sufficient energy and the damage is not too severe, 
        repair mechanisms may be activated instead. The decision between survival 
        and death depends on the balance of pro-survival and pro-death signals. 
        This process functions as a cellular decision-making system that determines 
        whether a cell should continue living or undergo programmed death.
        """
    }
    
    # Create papers directory
    papers_dir = Path("sample_papers")
    papers_dir.mkdir(exist_ok=True)
    
    # Write papers to files
    for filename, content in papers.items():
        filepath = papers_dir / filename
        with open(filepath, 'w') as f:
            f.write(content.strip())
    
    return papers_dir

def demo_extractor_agent():
    """Demonstrate the Extractor Agent."""
    print("=== Extractor Agent Demo ===")
    
    agent = ExtractorAgent()
    
    # Sample text from a biological paper
    sample_text = """
    The lac operon is a classic example of gene regulation. When lactose is present, 
    the repressor protein is inactivated, allowing transcription to proceed. If glucose 
    is also present, cAMP levels are low, and the operon is only partially activated. 
    This creates a feedback loop where the system responds to environmental conditions. 
    The entire pathway functions as a genetic circuit that processes multiple inputs.
    """
    
    # Extract logic
    results = agent.extract_from_text(sample_text, "lac_operon_demo")
    
    print(f"Document: {results.document_id}")
    print(f"Total elements extracted: {results.metadata['total_elements']}")
    print(f"Average confidence: {results.metadata['avg_confidence']:.2f}")
    print(f"Element types: {results.metadata['element_types']}")
    
    # Show top elements
    print("\nTop logic elements:")
    top_elements = sorted(results.logic_elements, key=lambda x: x.confidence, reverse=True)[:3]
    for i, elem in enumerate(top_elements, 1):
        print(f"{i}. {elem.element_type}: {elem.description}")
        print(f"   Confidence: {elem.confidence:.2f}")
    
    # Save results
    agent.save_results(results, "demo_extraction_results.json")
    print("\nResults saved to demo_extraction_results.json")
    
    return results

def demo_diagram_synthesizer():
    """Demonstrate the Diagram Synthesizer Agent."""
    print("\n=== Diagram Synthesizer Demo ===")
    
    synthesizer = DiagramSynthesizer()
    
    # Example logic elements (from Extractor Agent output)
    logic_elements = [
        {
            'element_type': 'conditional',
            'description': 'When lactose is present',
            'confidence': 0.8
        },
        {
            'element_type': 'process',
            'description': 'Repressor protein is inactivated',
            'confidence': 0.9
        },
        {
            'element_type': 'conditional',
            'description': 'If glucose is also present',
            'confidence': 0.7
        },
        {
            'element_type': 'process',
            'description': 'cAMP levels are low',
            'confidence': 0.8
        },
        {
            'element_type': 'loop',
            'description': 'Feedback loop responds to environmental conditions',
            'confidence': 0.6
        }
    ]
    
    # Synthesize flowchart
    flowchart = synthesizer.synthesize_from_logic(logic_elements, "Lac Operon Regulation Demo")
    
    print(f"Title: {flowchart.title}")
    print(f"Total elements: {flowchart.metadata['total_elements']}")
    print(f"Element types: {flowchart.metadata['element_types']}")
    
    # Render and save
    synthesizer.render_flowchart(flowchart, "demo_flowchart.png")
    synthesizer.save_flowchart_data(flowchart, "demo_flowchart.json")
    
    print("\nFlowchart saved as demo_flowchart.png")
    print("Flowchart data saved as demo_flowchart.json")
    
    return flowchart

def demo_agent_coordinator():
    """Demonstrate the Agent Coordinator."""
    print("\n=== Agent Coordinator Demo ===")
    
    coordinator = AgentCoordinator()
    
    # Create sample papers
    papers_dir = create_sample_papers()
    
    # Process a paper through the complete workflow
    paper_file = papers_dir / "lac_operon.txt"
    results = coordinator.process_paper(str(paper_file), "Lac Operon Analysis Demo")
    
    print(f"Workflow ID: {results['workflow_id']}")
    print(f"Output files: {len(results['output_files'])}")
    
    for output_file in results['output_files']:
        if os.path.exists(output_file):
            print(f"✓ {output_file}")
        else:
            print(f"✗ {output_file} (not found)")
    
    # List workflows
    workflows = coordinator.list_workflows()
    print(f"\nTotal workflows: {len(workflows)}")
    
    # Get workflow status
    status = coordinator.get_workflow_status(results['workflow_id'])
    print(f"Workflow status: {status['status']}")
    
    return results

def demo_complete_system():
    """Demonstrate the complete GLMP system."""
    print("=" * 60)
    print("GLMP SYSTEM DEMONSTRATION")
    print("Genome Logic Modeling Project AI Agent System")
    print("=" * 60)
    
    try:
        # Demo individual agents
        extraction_results = demo_extractor_agent()
        flowchart_results = demo_diagram_synthesizer()
        workflow_results = demo_agent_coordinator()
        
        print("\n" + "=" * 60)
        print("DEMONSTRATION COMPLETE")
        print("=" * 60)
        
        print("\nGenerated Files:")
        files_to_check = [
            "demo_extraction_results.json",
            "demo_flowchart.png",
            "demo_flowchart.json",
            "output/extracted_logic.json",
            "output/flowchart.png",
            "output/flowchart.json"
        ]
        
        for file_path in files_to_check:
            if os.path.exists(file_path):
                size = os.path.getsize(file_path)
                print(f"✓ {file_path} ({size} bytes)")
            else:
                print(f"✗ {file_path} (not found)")
        
        print("\nSystem Status: SUCCESS")
        print("All AI agents are functioning correctly!")
        
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        print("System Status: FAILED")
        return False
    
    return True

def create_system_documentation():
    """Create system documentation."""
    print("\n=== Creating System Documentation ===")
    
    docs = {
        "system_overview": {
            "title": "GLMP AI Agent System Overview",
            "description": "The Genome Logic Modeling Project uses AI agents to analyze biological papers and extract computational logic.",
            "agents": [
                {
                    "name": "Extractor Agent",
                    "purpose": "Read papers and extract logic from text",
                    "capabilities": [
                        "Pattern recognition for logic elements",
                        "Confidence scoring",
                        "Context extraction",
                        "JSON output generation"
                    ]
                },
                {
                    "name": "Diagram Synthesizer",
                    "purpose": "Convert logic into standardized flowcharts",
                    "capabilities": [
                        "Flowchart generation",
                        "Multiple element types",
                        "Professional styling",
                        "PNG and JSON output"
                    ]
                },
                {
                    "name": "Agent Coordinator",
                    "purpose": "Manage and orchestrate all AI agents",
                    "capabilities": [
                        "Workflow management",
                        "Task coordination",
                        "Error handling",
                        "Status tracking"
                    ]
                }
            ]
        },
        "usage_examples": {
            "extractor": "agent.extract_from_text(text, document_id)",
            "synthesizer": "synthesizer.synthesize_from_logic(logic_elements, title)",
            "coordinator": "coordinator.process_paper(paper_file, title)"
        }
    }
    
    with open("glmp_system_documentation.json", 'w') as f:
        json.dump(docs, f, indent=2)
    
    print("System documentation saved to glmp_system_documentation.json")

def main():
    """Main demonstration function."""
    print("Starting GLMP System Demonstration...")
    
    # Run complete system demo
    success = demo_complete_system()
    
    if success:
        # Create documentation
        create_system_documentation()
        
        print("\n" + "=" * 60)
        print("GLMP SYSTEM READY FOR USE")
        print("=" * 60)
        print("\nThe system can now:")
        print("• Extract logic from biological papers")
        print("• Generate professional flowcharts")
        print("• Coordinate multi-agent workflows")
        print("• Process multiple papers automatically")
        print("\nNext steps:")
        print("• Add more AI agents (Pattern Recognizer, Meta-Modeler, etc.)")
        print("• Integrate with external databases")
        print("• Deploy as a web service")
        print("• Scale to process large paper collections")
    else:
        print("\nSystem demonstration failed. Please check error messages above.")

if __name__ == "__main__":
    main()