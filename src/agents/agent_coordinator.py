#!/usr/bin/env python3
"""
Agent Coordinator for GLMP
Manages and orchestrates all AI agents in the Genome Logic Modeling Project
"""

import json
import os
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
from datetime import datetime

# Import our agents
from .extractor_agent import ExtractorAgent, ExtractedLogic
from .diagram_synthesizer import DiagramSynthesizer, Flowchart

@dataclass
class AgentTask:
    """Represents a task for an agent."""
    task_id: str
    agent_type: str
    input_data: Dict[str, Any]
    status: str = "pending"  # pending, running, completed, failed
    result: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    created_at: str = ""
    completed_at: Optional[str] = None

@dataclass
class WorkflowStep:
    """Represents a step in the GLMP workflow."""
    step_id: str
    name: str
    description: str
    agent_type: str
    input_dependencies: List[str]
    output_files: List[str]
    status: str = "pending"

@dataclass
class GLMPWorkflow:
    """Complete GLMP workflow definition."""
    workflow_id: str
    title: str
    description: str
    steps: List[WorkflowStep]
    created_at: str
    status: str = "pending"

class AgentCoordinator:
    """Coordinates all AI agents in the GLMP project."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.output_dir = self.config.get('output_dir', 'output')
        self.agents = self._initialize_agents()
        self.workflows = {}
        self.tasks = {}
        
        # Create output directory
        Path(self.output_dir).mkdir(exist_ok=True)
        
    def _initialize_agents(self) -> Dict[str, Any]:
        """Initialize all AI agents."""
        return {
            'extractor': ExtractorAgent(),
            'diagram_synthesizer': DiagramSynthesizer(),
            # Future agents can be added here
            # 'pattern_recognizer': PatternRecognizer(),
            # 'meta_modeler': MetaModeler(),
            # 'critic': Critic(),
            # 'experiment_prescriber': ExperimentPrescriber()
        }
    
    def create_workflow(self, title: str, description: str) -> GLMPWorkflow:
        """Create a new GLMP workflow."""
        workflow_id = f"workflow_{int(time.time())}"
        
        # Define standard GLMP workflow steps
        steps = [
            WorkflowStep(
                step_id="extract_logic",
                name="Extract Logic from Text",
                description="Extract computational logic elements from biological papers",
                agent_type="extractor",
                input_dependencies=[],
                output_files=["extracted_logic.json"]
            ),
            WorkflowStep(
                step_id="synthesize_diagram",
                name="Synthesize Flowchart",
                description="Convert extracted logic into standardized flowcharts",
                agent_type="diagram_synthesizer",
                input_dependencies=["extracted_logic.json"],
                output_files=["flowchart.png", "flowchart.json"]
            )
        ]
        
        workflow = GLMPWorkflow(
            workflow_id=workflow_id,
            title=title,
            description=description,
            steps=steps,
            created_at=datetime.now().isoformat()
        )
        
        self.workflows[workflow_id] = workflow
        return workflow
    
    def execute_workflow(self, workflow_id: str, input_files: Dict[str, str]) -> Dict[str, Any]:
        """Execute a complete GLMP workflow."""
        if workflow_id not in self.workflows:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        workflow = self.workflows[workflow_id]
        workflow.status = "running"
        results = {}
        
        print(f"=== Executing Workflow: {workflow.title} ===")
        print(f"Description: {workflow.description}")
        print(f"Steps: {len(workflow.steps)}")
        
        for step in workflow.steps:
            print(f"\n--- Executing Step: {step.name} ---")
            step.status = "running"
            
            try:
                # Execute the step
                step_result = self._execute_step(step, input_files, results)
                results[step.step_id] = step_result
                step.status = "completed"
                
                print(f"✓ Step completed: {step.name}")
                
            except Exception as e:
                step.status = "failed"
                workflow.status = "failed"
                print(f"✗ Step failed: {step.name} - {str(e)}")
                raise
        
        workflow.status = "completed"
        print(f"\n=== Workflow Completed Successfully ===")
        
        return results
    
    def _execute_step(self, step: WorkflowStep, input_files: Dict[str, str], 
                     previous_results: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single workflow step."""
        agent = self.agents[step.agent_type]
        
        if step.agent_type == "extractor":
            return self._execute_extractor_step(step, input_files, agent)
        elif step.agent_type == "diagram_synthesizer":
            return self._execute_diagram_synthesizer_step(step, previous_results, agent)
        else:
            raise ValueError(f"Unknown agent type: {step.agent_type}")
    
    def _execute_extractor_step(self, step: WorkflowStep, input_files: Dict[str, str], 
                               agent: ExtractorAgent) -> Dict[str, Any]:
        """Execute the extractor agent step."""
        # Get input file
        if 'text_file' not in input_files:
            raise ValueError("Input file 'text_file' required for extractor step")
        
        text_file = input_files['text_file']
        
        # Extract logic from file
        extracted_logic = agent.extract_from_file(text_file)
        
        # Save results
        output_file = os.path.join(self.output_dir, "extracted_logic.json")
        agent.save_results(extracted_logic, output_file)
        
        return {
            'extracted_logic': extracted_logic,
            'output_file': output_file,
            'metadata': extracted_logic.metadata
        }
    
    def _execute_diagram_synthesizer_step(self, step: WorkflowStep, 
                                        previous_results: Dict[str, Any],
                                        agent: DiagramSynthesizer) -> Dict[str, Any]:
        """Execute the diagram synthesizer step."""
        # Get extracted logic from previous step
        if 'extract_logic' not in previous_results:
            raise ValueError("Extractor step results required for diagram synthesis")
        
        extracted_logic = previous_results['extract_logic']['extracted_logic']
        
        # Convert to format expected by diagram synthesizer
        logic_elements = []
        for elem in extracted_logic.logic_elements:
            logic_elements.append({
                'element_type': elem.element_type,
                'description': elem.description,
                'confidence': elem.confidence
            })
        
        # Synthesize flowchart
        flowchart = agent.synthesize_from_logic(logic_elements, 
                                               f"GLMP Flowchart - {extracted_logic.document_id}")
        
        # Save results
        flowchart_png = os.path.join(self.output_dir, "flowchart.png")
        flowchart_json = os.path.join(self.output_dir, "flowchart.json")
        
        agent.render_flowchart(flowchart, flowchart_png)
        agent.save_flowchart_data(flowchart, flowchart_json)
        
        return {
            'flowchart': flowchart,
            'flowchart_png': flowchart_png,
            'flowchart_json': flowchart_json,
            'metadata': flowchart.metadata
        }
    
    def process_paper(self, paper_file: str, title: str = "GLMP Paper Analysis") -> Dict[str, Any]:
        """Process a biological paper through the complete GLMP workflow."""
        # Create workflow
        workflow = self.create_workflow(
            title=title,
            description=f"Analysis of paper: {paper_file}"
        )
        
        # Prepare input files
        input_files = {
            'text_file': paper_file
        }
        
        # Execute workflow
        results = self.execute_workflow(workflow.workflow_id, input_files)
        
        return {
            'workflow_id': workflow.workflow_id,
            'results': results,
            'output_files': self._get_output_files(results)
        }
    
    def _get_output_files(self, results: Dict[str, Any]) -> List[str]:
        """Get list of output files from workflow results."""
        output_files = []
        
        for step_result in results.values():
            if isinstance(step_result, dict):
                for key, value in step_result.items():
                    if key.endswith('_file') or key.endswith('_png') or key.endswith('_json'):
                        if isinstance(value, str) and os.path.exists(value):
                            output_files.append(value)
        
        return output_files
    
    def get_workflow_status(self, workflow_id: str) -> Dict[str, Any]:
        """Get status of a workflow."""
        if workflow_id not in self.workflows:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        workflow = self.workflows[workflow_id]
        return {
            'workflow_id': workflow.workflow_id,
            'title': workflow.title,
            'status': workflow.status,
            'steps': [
                {
                    'step_id': step.step_id,
                    'name': step.name,
                    'status': step.status
                }
                for step in workflow.steps
            ]
        }
    
    def list_workflows(self) -> List[Dict[str, Any]]:
        """List all workflows."""
        return [
            {
                'workflow_id': workflow.workflow_id,
                'title': workflow.title,
                'status': workflow.status,
                'created_at': workflow.created_at
            }
            for workflow in self.workflows.values()
        ]
    
    def save_workflow_data(self, workflow_id: str, output_path: str):
        """Save workflow data to JSON file."""
        if workflow_id not in self.workflows:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        workflow = self.workflows[workflow_id]
        
        data = {
            'workflow': asdict(workflow),
            'tasks': {
                task_id: asdict(task) 
                for task_id, task in self.tasks.items() 
                if task_id.startswith(workflow_id)
            }
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

def main():
    """Example usage of the Agent Coordinator."""
    coordinator = AgentCoordinator()
    
    # Example: Process a sample paper
    sample_paper = """
    The lac operon is a classic example of gene regulation in bacteria. 
    When lactose is present in the environment, the repressor protein is inactivated, 
    allowing transcription of the lac genes to proceed. If glucose is also present, 
    cAMP levels are low, and the operon is only partially activated. 
    This creates a feedback loop where the system responds to environmental conditions. 
    The entire pathway functions as a genetic circuit that processes multiple inputs 
    and produces appropriate outputs based on the current state of the environment.
    """
    
    # Write sample paper to file
    sample_file = "sample_paper.txt"
    with open(sample_file, 'w') as f:
        f.write(sample_paper)
    
    try:
        # Process the paper
        results = coordinator.process_paper(sample_file, "Lac Operon Analysis")
        
        print("\n=== GLMP Analysis Complete ===")
        print(f"Workflow ID: {results['workflow_id']}")
        print(f"Output files: {results['output_files']}")
        
        # List workflows
        workflows = coordinator.list_workflows()
        print(f"\nTotal workflows: {len(workflows)}")
        
        # Get workflow status
        status = coordinator.get_workflow_status(results['workflow_id'])
        print(f"Workflow status: {status['status']}")
        
    finally:
        # Clean up
        if os.path.exists(sample_file):
            os.remove(sample_file)

if __name__ == "__main__":
    main()