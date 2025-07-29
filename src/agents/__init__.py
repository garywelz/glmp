"""
GLMP AI Agents Package

This package contains AI agents for the Genome Logic Modeling Project (GLMP).
Each agent specializes in a specific aspect of biological logic analysis.
"""

from .extractor_agent import ExtractorAgent, ExtractedLogic, LogicElement
from .diagram_synthesizer import DiagramSynthesizer, Flowchart, FlowchartElement, FlowchartConnection
from .agent_coordinator import AgentCoordinator, GLMPWorkflow, WorkflowStep, AgentTask

__version__ = "1.0.0"
__author__ = "GLMP Team"

__all__ = [
    # Extractor Agent
    'ExtractorAgent',
    'ExtractedLogic', 
    'LogicElement',
    
    # Diagram Synthesizer
    'DiagramSynthesizer',
    'Flowchart',
    'FlowchartElement',
    'FlowchartConnection',
    
    # Agent Coordinator
    'AgentCoordinator',
    'GLMPWorkflow',
    'WorkflowStep',
    'AgentTask'
]