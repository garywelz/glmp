"""
Vertex AI Integration for GLMP Cloud Service
Provides process generation and validation using Google's Gemini models
"""

from google.cloud import aiplatform
from vertexai.preview.generative_models import GenerativeModel, ChatSession
import vertexai
import json
import logging

logger = logging.getLogger(__name__)

# Initialize Vertex AI
PROJECT_ID = "regal-scholar-453620-r7"
REGION = "us-central1"

# Initialize Vertex AI
vertexai.init(project=PROJECT_ID, location=REGION)


class ProcessGenerator:
    """Generate biological process flowcharts using Vertex AI"""
    
    def __init__(self):
        """Initialize Gemini model"""
        self.model = GenerativeModel("gemini-pro")
        logger.info("✓ Initialized Vertex AI Gemini model")
    
    def generate_process_from_description(self, name, organism, category, description, sources=None):
        """
        Generate a complete process JSON from description
        
        Args:
            name: Process name
            organism: Organism name
            category: Process category
            description: Detailed description of the process
            sources: Optional list of source papers/citations
        
        Returns:
            Complete process JSON dict
        """
        
        prompt = f"""You are a biological process expert. Generate a detailed biological process flowchart in JSON format.

PROCESS DETAILS:
- Name: {name}
- Organism: {organism}
- Category: {category}
- Description: {description}

REQUIREMENTS:
1. Create a Mermaid flowchart with 30-50 unique nodes (use IDs: A, B, C, ..., AA, AB, etc.)
2. Identify all logic gates:
   - OR gates: Single input, binary yes/no decision (diamond shape)
   - AND gates: Multiple inputs converging (diamond shape with multiple arrows in)
3. Apply 7-color scheme:
   - Red (#ff6b6b): Triggers & Inputs
   - Yellow (#ffd43b): Structures & Objects (proteins, enzymes)
   - Green (#51cf66): Processing & Operations
   - Blue (#74c0fc): Intermediates & States
   - Orange (#ff9f43): OR Logic Gates (diamonds)
   - Lavender (#b4b4dc): AND Logic Gates (diamonds)
   - Violet (#b197fc): Products & Outputs
4. Style EVERY node explicitly
5. Include 3-5 scientific citations with PubMed IDs
6. Add scientific accuracy statement
7. Count nodes and logic gates

Generate ONLY valid JSON matching this exact schema:
{{
  "id": "organism_process_name",
  "name": "Process Name",
  "organism": "Organism",
  "category": "Category",
  "description": "Detailed description",
  "scientificAccuracy": "Statement about validation",
  "complexity": {{
    "nodes": 0,
    "uniqueIdentifiers": true,
    "colorCoded": true,
    "detailLevel": "detailed",
    "logicGates": {{"orGates": 0, "andGates": 0, "total": 0}}
  }},
  "colorScheme": {{
    "red": {{"hex": "#ff6b6b", "category": "Triggers & Inputs", "description": "..."}},
    "yellow": {{"hex": "#ffd43b", "category": "Structures & Objects", "description": "..."}},
    "green": {{"hex": "#51cf66", "category": "Processing & Operations", "description": "..."}},
    "blue": {{"hex": "#74c0fc", "category": "Intermediates & States", "description": "..."}},
    "orange": {{"hex": "#ff9f43", "category": "OR Logic Gates", "description": "..."}},
    "lavender": {{"hex": "#b4b4dc", "category": "AND Logic Gates", "description": "..."}},
    "violet": {{"hex": "#b197fc", "category": "Products & Outputs", "description": "..."}}
  }},
  "mermaid": "graph TD\\n...",
  "sources": [...],
  "keywords": [...],
  "relatedProcesses": [...],
  "created": "2025-10-10",
  "lastUpdated": "2025-10-10",
  "verified": true,
  "verifiedBy": "...",
  "notes": "..."
}}

Generate the complete JSON now:"""

        try:
            logger.info(f"Generating process: {name}")
            response = self.model.generate_content(prompt)
            
            # Extract JSON from response
            response_text = response.text
            
            # Try to parse as JSON
            # Remove markdown code blocks if present
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0]
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0]
            
            process_data = json.loads(response_text.strip())
            
            logger.info(f"✓ Generated process with {process_data.get('complexity', {}).get('nodes', 0)} nodes")
            return process_data
            
        except Exception as e:
            logger.error(f"Failed to generate process: {e}")
            return None
    
    
    def validate_biological_accuracy(self, process_data):
        """
        Validate biological accuracy of a process using Vertex AI
        
        Args:
            process_data: Process JSON dict
        
        Returns:
            Validation report dict
        """
        
        prompt = f"""You are a molecular biology expert. Validate this biological process flowchart for scientific accuracy.

PROCESS: {process_data.get('name')}
ORGANISM: {process_data.get('organism')}
DESCRIPTION: {process_data.get('description')}

MERMAID DIAGRAM:
{process_data.get('mermaid', '')[:2000]}...

CITATIONS:
{json.dumps(process_data.get('sources', []), indent=2)}

Analyze and provide:
1. Biological accuracy (0-10 score)
2. Citation quality (0-10 score)
3. Any factual errors or inconsistencies
4. Suggestions for improvement
5. Missing key mechanisms

Respond in JSON format:
{{
  "accuracy_score": 0-10,
  "citation_score": 0-10,
  "errors": ["list of errors"],
  "suggestions": ["list of suggestions"],
  "missing_mechanisms": ["list"],
  "overall_assessment": "text"
}}"""

        try:
            logger.info(f"Validating process: {process_data.get('name')}")
            response = self.model.generate_content(prompt)
            
            response_text = response.text
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0]
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0]
            
            validation = json.loads(response_text.strip())
            
            logger.info(f"✓ Validation complete - Accuracy: {validation.get('accuracy_score')}/10")
            return validation
            
        except Exception as e:
            logger.error(f"Failed to validate process: {e}")
            return {
                "accuracy_score": 0,
                "citation_score": 0,
                "errors": [str(e)],
                "suggestions": [],
                "missing_mechanisms": [],
                "overall_assessment": "Validation failed"
            }
    
    
    def suggest_logic_gates(self, mermaid_diagram):
        """
        Analyze mermaid diagram and suggest logic gate identification
        
        Args:
            mermaid_diagram: Mermaid flowchart string
        
        Returns:
            List of suggested logic gates
        """
        
        prompt = f"""Analyze this Mermaid flowchart and identify all logic gates.

MERMAID DIAGRAM:
{mermaid_diagram}

Identify:
1. OR gates - Diamond nodes with single input, binary yes/no branches
2. AND gates - Multiple input arrows converging to a single node

For each gate, specify:
- Node ID
- Gate type (OR or AND)
- Reason (why it's that type)
- Recommended color (orange for OR, lavender for AND)

Respond in JSON:
{{
  "or_gates": [{{"node": "X", "reason": "...", "color": "#ff9f43"}}],
  "and_gates": [{{"node": "Y", "reason": "...", "color": "#b4b4dc"}}],
  "total_gates": 0
}}"""

        try:
            response = self.model.generate_content(prompt)
            response_text = response.text
            
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0]
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0]
            
            gates = json.loads(response_text.strip())
            return gates
            
        except Exception as e:
            logger.error(f"Failed to analyze logic gates: {e}")
            return {"or_gates": [], "and_gates": [], "total_gates": 0}


class ProcessEnricher:
    """Enrich processes with AI-powered insights"""
    
    def __init__(self):
        """Initialize Gemini model"""
        self.model = GenerativeModel("gemini-pro")
        logger.info("✓ Initialized Process Enricher")
    
    
    def generate_scientific_accuracy_statement(self, process_data):
        """
        Generate a scientific accuracy statement for a process
        
        Args:
            process_data: Process JSON dict
        
        Returns:
            Scientific accuracy statement string
        """
        
        prompt = f"""Generate a concise scientific accuracy statement for this biological process.

PROCESS: {process_data.get('name')}
ORGANISM: {process_data.get('organism')}
DESCRIPTION: {process_data.get('description')}
CITATIONS: {len(process_data.get('sources', []))} peer-reviewed sources

Write 2-3 sentences that:
1. State the research basis (decades of work, Nobel Prize, etc.)
2. Mention validation methods (genetic, biochemical, structural)
3. Affirm accuracy against primary sources

Style: Authoritative, scientific, concise."""

        try:
            response = self.model.generate_content(prompt)
            statement = response.text.strip()
            
            # Remove quotes if present
            if statement.startswith('"') and statement.endswith('"'):
                statement = statement[1:-1]
            
            return statement
            
        except Exception as e:
            logger.error(f"Failed to generate accuracy statement: {e}")
            return "This flowchart is based on verified scientific research."
    
    
    def suggest_related_processes(self, process_data):
        """
        Suggest related processes based on biological connections
        
        Args:
            process_data: Process JSON dict
        
        Returns:
            List of suggested related process IDs
        """
        
        prompt = f"""Suggest 3-5 related biological processes for this process.

PROCESS: {process_data.get('name')}
ORGANISM: {process_data.get('organism')}
CATEGORY: {process_data.get('category')}
DESCRIPTION: {process_data.get('description')}

Suggest processes that are:
- Mechanistically related
- Share regulatory components
- Occur in same organism
- Part of same pathway/system

Respond with JSON list of process IDs (snake_case):
{{
  "related": ["organism_process_name", ...]
}}"""

        try:
            response = self.model.generate_content(prompt)
            response_text = response.text
            
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0]
            
            result = json.loads(response_text.strip())
            return result.get('related', [])
            
        except Exception as e:
            logger.error(f"Failed to suggest related processes: {e}")
            return []


# Global instances
generator = None
enricher = None

def get_generator():
    """Get or create ProcessGenerator instance"""
    global generator
    if generator is None:
        generator = ProcessGenerator()
    return generator

def get_enricher():
    """Get or create ProcessEnricher instance"""
    global enricher
    if enricher is None:
        enricher = ProcessEnricher()
    return enricher
