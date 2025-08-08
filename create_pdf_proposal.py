#!/usr/bin/env python3
"""
Create a PDF version of the ProcessDSL proposal with embedded images.
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import os

def create_pdf():
    # Create the PDF document
    doc = SimpleDocTemplate("ProcessDSL_FlowCell10_Proposal.pdf", pagesize=A4)
    story = []
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.darkblue
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        spaceBefore=20,
        textColor=colors.darkblue
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=6,
        alignment=TA_JUSTIFY
    )
    
    code_style = ParagraphStyle(
        'CustomCode',
        parent=styles['Normal'],
        fontSize=9,
        fontName='Courier',
        leftIndent=20,
        spaceAfter=6
    )
    
    # Title
    story.append(Paragraph("ProcessDSL + FlowCell-10 Proposal", title_style))
    story.append(Spacer(1, 20))
    
    # Introduction
    intro_text = """
    This proposal outlines a pilot initiative to integrate the <b>"genome as program"</b> concept and 
    <b>cellular process flowcharting</b> into the Virtual Cell project. The goal is to formalize biological 
    processes as executable, interpretable programs that can be learned, simulated, and manipulated by AI.
    """
    story.append(Paragraph(intro_text, body_style))
    story.append(Spacer(1, 20))
    
    # Section 1
    story.append(Paragraph("1. ProcessDSL Specification", heading_style))
    story.append(Paragraph("""
    <b>ProcessDSL</b> is a domain-specific language for representing cellular processes. 
    It compiles human-readable flowcharts into machine-executable forms such as stochastic rule systems, 
    Petri nets, or hybrid ODE/event simulators.
    """, body_style))
    
    story.append(Paragraph("<b>Key features:</b>", body_style))
    features = [
        "Reactions as rules with explicit guards and rate constants.",
        "Conditional logic (IF/ELSE) for regulation.",
        "Iterative loops (WHILE) for cyclic processes.",
        "Event triggers for environmental or signaling changes.",
        "Support for compartments (nucleus, cytosol, organelles)."
    ]
    for feature in features:
        story.append(Paragraph(f"• {feature}", body_style))
    
    story.append(Spacer(1, 20))
    
    # Section 2
    story.append(Paragraph("2. FlowCell-10 Pilot Dataset", heading_style))
    story.append(Paragraph("""
    <b>FlowCell-10</b> is a curated set of ten well-characterized yeast pathways, each represented as:
    """, body_style))
    
    dataset_items = [
        "A canonical flowchart",
        "A ProcessDSL file", 
        "Reference simulation outputs from literature data"
    ]
    for item in dataset_items:
        story.append(Paragraph(f"• {item}", body_style))
    
    story.append(Spacer(1, 12))
    story.append(Paragraph("<b>Example pathways:</b>", body_style))
    pathways = [
        "Glycolysis", "TOR nutrient sensing pathway", "Heat shock response",
        "Autophagy initiation", "Unfolded protein response (UPR)",
        "Cell cycle G1/S transition", "Mitochondrial respiration control",
        "Amino acid biosynthesis regulation", "Gluconeogenesis", "Alcoholic fermentation"
    ]
    for i, pathway in enumerate(pathways, 1):
        story.append(Paragraph(f"{i}. {pathway}", body_style))
    
    story.append(Spacer(1, 20))
    
    # Section 3
    story.append(Paragraph("3. Example ProcessDSL (Glycolysis)", heading_style))
    
    code_text = """
process Glycolysis in Cytosol:
  state: [Glucose, G6P, F6P, F16BP, G3P, DHAP, PEP, Pyruvate, ATP, ADP, NAD+, NADH]
  rule Hexokinase: Glucose + ATP -> G6P + ADP  [guard: ATP>θ1]
  rule PFK: F6P + ATP -> F16BP + ADP           [guard: ATP<θ2 & AMP>θ3]
  rule Aldolase: F16BP -> G3P + DHAP
  rule TPI: DHAP <-> G3P
  rule PyruvateKinase: PEP + ADP -> Pyruvate + ATP [allosteric: F16BP activates]
  event GlucosePulse(t=0..T): inflow rate r_in
    """
    story.append(Paragraph(code_text, code_style))
    
    story.append(Spacer(1, 20))
    
    # Section 4 with image
    story.append(Paragraph("4. Expanded Glycolysis Flowchart", heading_style))
    story.append(Paragraph("""
    Below is an example from FlowCell-10 showing <b>Glycolysis in Yeast</b> with branch and loop structure:
    """, body_style))
    
    # Add the image if it exists
    if os.path.exists("YeastFlowchart1.drawio.png"):
        # Add title for the image
        story.append(Paragraph("4. Expanded Glycolysis Flowchart", heading_style))
        story.append(Paragraph("Below is an example from FlowCell-10 showing <b>Glycolysis in Yeast</b> with branch and loop structure:", body_style))
        story.append(Spacer(1, 12))
        
        # Add image with proper aspect ratio
        img = Image("YeastFlowchart1.drawio.png", width=7*inch, height=8*inch, kind='proportional')
        story.append(img)
        story.append(Spacer(1, 20))
        
        # Add page break before Mermaid code
        story.append(PageBreak())
        
        # Add Mermaid code on separate page
        story.append(Paragraph("5. Original Mermaid Code (Reference)", heading_style))
        story.append(Paragraph("The original Mermaid code is preserved below for reference and future rendering:", body_style))
        story.append(Spacer(1, 12))
    
    story.append(Paragraph("""
    <i>Note: The original Mermaid code is preserved below for reference and future rendering.</i>
    """, body_style))
    
    mermaid_code = """
flowchart TD
    A[Glucose Uptake<br/>(Transport into cell)]
      --> B[Hexokinase<br/>Glucose → G6P]
    B --> C[Isomerase<br/>G6P → F6P]
    C --> D[Phosphofructokinase (PFK)<br/>F6P → F1,6BP]

    %% Branch
    D --> E1[DHAP<br/>(Dihydroxyacetone phosphate)]
    D --> E2[G3P<br/>(Glyceraldehyde‑3‑phosphate)]
    E1 -- TPI forward --> E2
    E2 -- TPI reverse --> E1

    %% Payoff phase
    E2 --> F[G3P Oxidation & Phosphorylation<br/>(NADH + ATP yield)]
    F --> G[Phosphoglycerate Mutase & Enolase<br/>→ PEP]
    G --> H[Pyruvate Kinase<br/>PEP → Pyruvate + ATP]
    H --> I[End Product:<br/>2 Pyruvate Molecules]
    """
    story.append(Paragraph(mermaid_code, code_style))
    
    story.append(Spacer(1, 20))
    
    # Section 5
    story.append(Paragraph("5. Deliverables", heading_style))
    deliverables = [
        "ProcessDSL specification and parser.",
        "FlowCell-10 diagrams, DSL files, and simulation benchmarks.",
        "Jupyter notebook demo: diagram → ProcessDSL → simulation → data comparison.",
        "Documentation for extending the dataset."
    ]
    for deliverable in deliverables:
        story.append(Paragraph(f"• {deliverable}", body_style))
    
    story.append(Spacer(1, 20))
    
    # Section 6
    story.append(Paragraph("6. Benefits to the Virtual Cell Project", heading_style))
    benefits = [
        "Provides an interpretable, executable representation of cellular processes.",
        "Bridges molecular prediction tools (e.g., AlphaFold 3) to systems-level dynamics.",
        "Enables counterfactual simulations and intervention planning.",
        "Creates training data for AI models to learn biological program induction."
    ]
    for benefit in benefits:
        story.append(Paragraph(f"• {benefit}", body_style))
    
    # Build the PDF
    doc.build(story)
    print("PDF created: ProcessDSL_FlowCell10_Proposal.pdf")

if __name__ == "__main__":
    create_pdf() 