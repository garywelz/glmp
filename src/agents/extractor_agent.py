#!/usr/bin/env python3
"""
Extractor AI Agent for GLMP
Task: Read papers, extract logic from text
"""

import re
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from pathlib import Path

@dataclass
class LogicElement:
    """Represents a logical element extracted from text."""
    element_type: str  # 'conditional', 'loop', 'subroutine', 'trigger', 'state'
    description: str
    confidence: float  # 0.0 to 1.0
    source_text: str
    line_number: Optional[int] = None
    context: Optional[str] = None

@dataclass
class ExtractedLogic:
    """Container for extracted logic from a document."""
    document_id: str
    logic_elements: List[LogicElement]
    summary: str
    metadata: Dict[str, Any]

class ExtractorAgent:
    """AI agent for extracting computational logic from biological papers."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.logic_patterns = self._initialize_patterns()
        
    def _initialize_patterns(self) -> Dict[str, List[str]]:
        """Initialize regex patterns for different logic types."""
        return {
            'conditional': [
                r'if\s+([^,]+)\s+then',
                r'when\s+([^,]+)',
                r'provided\s+that\s+([^,]+)',
                r'conditional\s+on\s+([^,]+)',
                r'([^,]+)\s+activates\s+([^,]+)',
                r'([^,]+)\s+inhibits\s+([^,]+)'
            ],
            'loop': [
                r'cycle\s+([^,]+)',
                r'loop\s+([^,]+)',
                r'repeated\s+([^,]+)',
                r'iterative\s+([^,]+)',
                r'feedback\s+loop',
                r'circadian\s+([^,]+)'
            ],
            'subroutine': [
                r'pathway\s+([^,]+)',
                r'cascade\s+([^,]+)',
                r'network\s+([^,]+)',
                r'circuit\s+([^,]+)',
                r'mechanism\s+([^,]+)',
                r'process\s+([^,]+)'
            ],
            'trigger': [
                r'triggered\s+by\s+([^,]+)',
                r'activated\s+by\s+([^,]+)',
                r'initiated\s+by\s+([^,]+)',
                r'stimulated\s+by\s+([^,]+)',
                r'induced\s+by\s+([^,]+)'
            ],
            'state': [
                r'state\s+([^,]+)',
                r'phase\s+([^,]+)',
                r'stage\s+([^,]+)',
                r'condition\s+([^,]+)',
                r'status\s+([^,]+)'
            ]
        }
    
    def extract_from_text(self, text: str, document_id: str = "unknown") -> ExtractedLogic:
        """Extract logic elements from text."""
        logic_elements = []
        
        # Split text into sentences for analysis
        sentences = self._split_into_sentences(text)
        
        for line_num, sentence in enumerate(sentences, 1):
            sentence = sentence.strip()
            if not sentence:
                continue
                
            # Check each pattern type
            for element_type, patterns in self.logic_patterns.items():
                for pattern in patterns:
                    matches = re.finditer(pattern, sentence, re.IGNORECASE)
                    for match in matches:
                        confidence = self._calculate_confidence(match, sentence, element_type)
                        if confidence > 0.3:  # Minimum confidence threshold
                            logic_element = LogicElement(
                                element_type=element_type,
                                description=match.group(0),
                                confidence=confidence,
                                source_text=sentence,
                                line_number=line_num,
                                context=self._get_context(sentences, line_num)
                            )
                            logic_elements.append(logic_element)
        
        # Generate summary
        summary = self._generate_summary(logic_elements, text)
        
        # Create metadata
        metadata = {
            'total_elements': len(logic_elements),
            'element_types': self._count_element_types(logic_elements),
            'avg_confidence': self._calculate_avg_confidence(logic_elements),
            'text_length': len(text),
            'sentences_analyzed': len(sentences)
        }
        
        return ExtractedLogic(
            document_id=document_id,
            logic_elements=logic_elements,
            summary=summary,
            metadata=metadata
        )
    
    def _split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences."""
        # Simple sentence splitting - could be improved with NLP libraries
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _calculate_confidence(self, match, sentence: str, element_type: str) -> float:
        """Calculate confidence score for a logic element."""
        base_confidence = 0.5
        
        # Boost confidence for biological terms
        biological_terms = ['gene', 'protein', 'enzyme', 'dna', 'rna', 'cell', 'molecule', 'pathway']
        sentence_lower = sentence.lower()
        
        for term in biological_terms:
            if term in sentence_lower:
                base_confidence += 0.1
        
        # Boost for computational terms
        computational_terms = ['logic', 'program', 'algorithm', 'function', 'process', 'system']
        for term in computational_terms:
            if term in sentence_lower:
                base_confidence += 0.1
        
        # Penalize for very short matches
        if len(match.group(0)) < 10:
            base_confidence -= 0.2
        
        return min(1.0, max(0.0, base_confidence))
    
    def _get_context(self, sentences: List[str], line_num: int, context_lines: int = 2) -> str:
        """Get context around a sentence."""
        start = max(0, line_num - context_lines - 1)
        end = min(len(sentences), line_num + context_lines)
        return " ".join(sentences[start:end])
    
    def _generate_summary(self, logic_elements: List[LogicElement], original_text: str) -> str:
        """Generate a summary of extracted logic."""
        if not logic_elements:
            return "No computational logic elements found in the text."
        
        element_counts = self._count_element_types(logic_elements)
        
        summary_parts = []
        summary_parts.append(f"Extracted {len(logic_elements)} logic elements:")
        
        for element_type, count in element_counts.items():
            summary_parts.append(f"- {count} {element_type} elements")
        
        # Add most confident elements
        top_elements = sorted(logic_elements, key=lambda x: x.confidence, reverse=True)[:3]
        if top_elements:
            summary_parts.append("\nTop logic elements:")
            for elem in top_elements:
                summary_parts.append(f"- {elem.element_type}: {elem.description[:100]}...")
        
        return "\n".join(summary_parts)
    
    def _count_element_types(self, logic_elements: List[LogicElement]) -> Dict[str, int]:
        """Count elements by type."""
        counts = {}
        for elem in logic_elements:
            counts[elem.element_type] = counts.get(elem.element_type, 0) + 1
        return counts
    
    def _calculate_avg_confidence(self, logic_elements: List[LogicElement]) -> float:
        """Calculate average confidence of all elements."""
        if not logic_elements:
            return 0.0
        return sum(elem.confidence for elem in logic_elements) / len(logic_elements)
    
    def extract_from_file(self, file_path: str) -> ExtractedLogic:
        """Extract logic from a file."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        return self.extract_from_text(text, document_id=path.name)
    
    def save_results(self, extracted_logic: ExtractedLogic, output_path: str):
        """Save extraction results to JSON file."""
        results = {
            'document_id': extracted_logic.document_id,
            'summary': extracted_logic.summary,
            'metadata': extracted_logic.metadata,
            'logic_elements': [
                {
                    'element_type': elem.element_type,
                    'description': elem.description,
                    'confidence': elem.confidence,
                    'source_text': elem.source_text,
                    'line_number': elem.line_number,
                    'context': elem.context
                }
                for elem in extracted_logic.logic_elements
            ]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

def main():
    """Example usage of the Extractor Agent."""
    agent = ExtractorAgent()
    
    # Example text from a biological paper
    sample_text = """
    The lac operon is a classic example of gene regulation. When lactose is present, 
    the repressor protein is inactivated, allowing transcription to proceed. If glucose 
    is also present, cAMP levels are low, and the operon is only partially activated. 
    This creates a feedback loop where the system responds to environmental conditions. 
    The entire pathway functions as a genetic circuit that processes multiple inputs.
    """
    
    # Extract logic
    results = agent.extract_from_text(sample_text, "lac_operon_example")
    
    # Print results
    print("=== Extractor Agent Results ===")
    print(f"Document: {results.document_id}")
    print(f"Summary: {results.summary}")
    print(f"Total elements: {results.metadata['total_elements']}")
    print(f"Average confidence: {results.metadata['avg_confidence']:.2f}")
    
    # Save results
    agent.save_results(results, "extraction_results.json")
    print("\nResults saved to extraction_results.json")

if __name__ == "__main__":
    main()