// Example of how to extend the D. melanogaster file with additional processes
// Add this to the allProcesses object in your HTML file

// Process 4: Neural Development
4: {
    levels: {
        1: `graph TD
            A[Neural Precursors] --> B[Neuroblast Formation]
            B --> C[Neural Differentiation]
            C --> D[Nervous System]
            
            style A fill:#ff6b6b,color:#fff
            style B fill:#ffd43b,color:#000
            style C fill:#51cf66,color:#fff
            style D fill:#b197fc,color:#fff`,
            
        2: `graph TD
            A[Neural Precursors] --> B[Neuroblast Delamination]
            B --> C[Asymmetric Division]
            C --> D[Neural Stem Cells]
            C --> E[Ganglion Mother Cells]
            D --> F[Self-Renewal]
            E --> G[Terminal Differentiation]
            F --> H[Neural Development]
            G --> H
            H --> I[Functional Nervous System]
            
            style A fill:#ff6b6b,color:#fff
            style B fill:#ffd43b,color:#000
            style C fill:#ffd43b,color:#000
            style D fill:#74c0fc,color:#fff
            style E fill:#74c0fc,color:#fff
            style F fill:#51cf66,color:#fff
            style G fill:#51cf66,color:#fff
            style H fill:#51cf66,color:#fff
            style I fill:#b197fc,color:#fff`,
            
        3: `graph TD
            A[Neuroectodermal Cells] --> B[proneural Gene Expression]
            B --> C[achaete-scute Complex]
            C --> D[Neuroblast Specification]
            D --> E[Notch Signaling]
            E --> F[Lateral Inhibition]
            F --> G[Neuroblast Delamination]
            G --> H[inscuteable Expression]
            H --> I[Asymmetric Division]
            I --> J[Basal Localization]
            I --> K[Apical Localization]
            J --> L[Ganglion Mother Cell]
            K --> M[Neuroblast Identity]
            L --> N[Terminal Division]
            M --> O[Continued Division]
            N --> P[Differentiated Neurons]
            O --> Q[Neural Lineage]
            P --> R[Neural Circuit Formation]
            Q --> R
            R --> S[Functional Neural Network]
            
            style A fill:#ff6b6b,color:#fff
            style B fill:#ffd43b,color:#000
            style C fill:#74c0fc,color:#fff
            style D fill:#51cf66,color:#fff
            style E fill:#ffd43b,color:#000
            style F fill:#51cf66,color:#fff
            style G fill:#51cf66,color:#fff
            style H fill:#ffd43b,color:#000
            style I fill:#51cf66,color:#fff
            style J fill:#74c0fc,color:#fff
            style K fill:#74c0fc,color:#fff
            style L fill:#74c0fc,color:#fff
            style M fill:#74c0fc,color:#fff
            style N fill:#51cf66,color:#fff
            style O fill:#51cf66,color:#fff
            style P fill:#74c0fc,color:#fff
            style Q fill:#74c0fc,color:#fff
            style R fill:#51cf66,color:#fff
            style S fill:#b197fc,color:#fff`,
            
        4: `graph TD
            A[Neuroectodermal Specification] --> B[proneural Cluster Formation]
            B --> C[achaete Expression]
            B --> D[scute Expression]
            C --> E[Proneural Protein Accumulation]
            D --> E
            E --> F[E(spl) Complex Activation]
            F --> G[Notch-Delta Signaling]
            G --> H[Lateral Inhibition Network]
            H --> I[Single Neuroblast Selection]
            I --> J[Neuroblast Identity Genes]
            J --> K[gooseberry Expression]
            J --> L[engrailed Expression]
            K --> M[Neuroblast Delamination]
            L --> M
            M --> N[inscuteable Localization]
            N --> O[Miranda Protein Complex]
            O --> P[Prospero Localization]
            P --> Q[Asymmetric Spindle Formation]
            Q --> R[Unequal Cell Division]
            R --> S[Large Neuroblast Cell]
            R --> T[Small GMC Cell]
            S --> U[numb Inheritance]
            T --> V[prospero Inheritance]
            U --> W[Neuroblast Maintenance]
            V --> X[GMC Differentiation Program]
            W --> Y[Continued Proliferation]
            X --> Z[Terminal Neuronal Differentiation]
            Y --> AA[Neural Lineage Expansion]
            Z --> BB[Synaptic Target Recognition]
            AA --> CC[Circuit Assembly]
            BB --> CC
            CC --> DD[Functional Neural Circuits]
            
            style A fill:#ff6b6b,color:#fff
            style B fill:#ffd43b,color:#000
            style C fill:#74c0fc,color:#fff
            style D fill:#74c0fc,color:#fff
            style E fill:#51cf66,color:#fff
            style F fill:#ffd43b,color:#000
            style G fill:#51cf66,color:#fff
            style H fill:#51cf66,color:#fff
            style I fill:#51cf66,color:#fff
            style J fill:#ffd43b,color:#000
            style K fill:#74c0fc,color:#fff
            style L fill:#74c0fc,color:#fff
            style M fill:#51cf66,color:#fff
            style N fill:#ffd43b,color:#000
            style O fill:#74c0fc,color:#fff
            style P fill:#74c0fc,color:#fff
            style Q fill:#51cf66,color:#fff
            style R fill:#51cf66,color:#fff
            style S fill:#74c0fc,color:#fff
            style T fill:#74c0fc,color:#fff
            style U fill:#51cf66,color:#fff
            style V fill:#51cf66,color:#fff
            style W fill:#51cf66,color:#fff
            style X fill:#51cf66,color:#fff
            style Y fill:#74c0fc,color:#fff
            style Z fill:#51cf66,color:#fff
            style AA fill:#74c0fc,color:#fff
            style BB fill:#51cf66,color:#fff
            style CC fill:#51cf66,color:#fff
            style DD fill:#b197fc,color:#fff`,
            
        5: `graph TD
            A[Dorsal-Ventral Patterning] --> B[Neuroectodermal Subdivision]
            C[Segment Polarity Genes] --> B
            B --> D[proneural Cluster Specification]
            D --> E[achaete-scute Complex Regulation]
            E --> F[AS-C Enhancer Modules]
            F --> G[achaete Transcription]
            F --> H[scute Transcription]
            G --> I[Achaete Protein Function]
            H --> J[Scute Protein Function]
            I --> K[E-box Binding]
            J --> K
            K --> L[Proneural Target Activation]
            L --> M[Delta Ligand Expression]
            M --> N[Notch Receptor Activation]
            N --> O[Su(H) Transcriptional Complex]
            O --> P[E(spl) Complex Induction]
            P --> Q[HLH Repressor Proteins]
            Q --> R[Proneural Gene Repression]
            R --> S[Lateral Inhibition Feedback]
            S --> T[Winner-Take-All Selection]
            T --> U[Neuroblast Specification]
            U --> V[Neuroblast Identity Network]
            V --> W[gooseberry Regulatory Logic]
            V --> X[engrailed Autoregulation]
            W --> Y[NB Identity Commitment]
            X --> Y
            Y --> Z[Delamination Machinery]
            Z --> AA[E-cadherin Downregulation]
            AA --> BB[Apical-Basal Polarity Loss]
            BB --> CC[Neuroblast Ingression]
            CC --> DD[inscuteable mRNA Localization]
            DD --> EE[Inscuteable Protein Asymmetry]
            EE --> FF[Partner of Inscuteable]
            FF --> GG[Spindle Orientation Control]
            GG --> HH[Miranda-Prospero Complex]
            HH --> II[Basal Crescent Formation]
            II --> JJ[Cell Cycle Progression]
            JJ --> KK[Asymmetric Spindle Assembly]
            KK --> LL[Chromosome Segregation]
            LL --> MM[Cytokinesis Completion]
            MM --> NN[Large NB + Small GMC]
            NN --> OO[numb Protein Segregation]
            OO --> PP[Notch Pathway Regulation]
            PP --> QQ[NB vs GMC Fate Decision]
            QQ --> RR[Self-Renewal Program]
            QQ --> SS[Differentiation Program]
            RR --> TT[Cyclin Expression]
            SS --> UU[Cell Cycle Exit]
            TT --> VV[Continued Proliferation]
            UU --> WW[Neuronal Differentiation]
            VV --> XX[Lineage Progression]
            WW --> YY[Axon Guidance]
            XX --> ZZ[Circuit Integration]
            YY --> ZZ
            ZZ --> AAA[Functional Nervous System]
            
            style A fill:#ff6b6b,color:#fff
            style C fill:#ff6b6b,color:#fff
            style B fill:#ffd43b,color:#000
            style D fill:#ffd43b,color:#000
            style E fill:#ffd43b,color:#000
            style F fill:#51cf66,color:#fff
            style G fill:#51cf66,color:#fff
            style H fill:#51cf66,color:#fff
            style I fill:#74c0fc,color:#fff
            style J fill:#74c0fc,color:#fff
            style K fill:#51cf66,color:#fff
            style L fill:#51cf66,color:#fff
            style M fill:#74c0fc,color:#fff
            style N fill:#ffd43b,color:#000
            style O fill:#74c0fc,color:#fff
            style P fill:#51cf66,color:#fff
            style Q fill:#74c0fc,color:#fff
            style R fill:#51cf66,color:#fff
            style S fill:#51cf66,color:#fff
            style T fill:#51cf66,color:#fff
            style U fill:#51cf66,color:#fff
            style V fill:#ffd43b,color:#000
            style W fill:#51cf66,color:#fff
            style X fill:#51cf66,color:#fff
            style Y fill:#51cf66,color:#fff
            style Z fill:#ffd43b,color:#000
            style AA fill:#51cf66,color:#fff
            style BB fill:#51cf66,color:#fff
            style CC fill:#51cf66,color:#fff
            style DD fill:#ffd43b,color:#000
            style EE fill:#74c0fc,color:#fff
            style FF fill:#74c0fc,color:#fff
            style GG fill:#51cf66,color:#fff
            style HH fill:#74c0fc,color:#fff
            style II fill:#74c0fc,color:#fff
            style JJ fill:#ffd43b,color:#000
            style KK fill:#51cf66,color:#fff
            style LL fill:#51cf66,color:#fff
            style MM fill:#51cf66,color:#fff
            style NN fill:#74c0fc,color:#fff
            style OO fill:#74c0fc,color:#fff
            style PP fill:#51cf66,color:#fff
            style QQ fill:#51cf66,color:#fff
            style RR fill:#51cf66,color:#fff
            style SS fill:#51cf66,color:#fff
            style TT fill:#74c0fc,color:#fff
            style UU fill:#74c0fc,color:#fff
            style VV fill:#51cf66,color:#fff
            style WW fill:#51cf66,color:#fff
            style XX fill:#74c0fc,color:#fff
            style YY fill:#51cf66,color:#fff
            style ZZ fill:#51cf66,color:#fff
            style AAA fill:#b197fc,color:#fff`
    }
},

// Process 5: Behavioral Genetics
5: {
    levels: {
        1: `graph TD
            A[Genetic Variants] --> B[Behavioral Phenotypes]
            B --> C[Neural Circuits]
            C --> D[Behavior Expression]
            
            style A fill:#ff6b6b,color:#fff
            style B fill:#ffd43b,color:#000
            style C fill:#51cf66,color:#fff
            style D fill:#b197fc,color:#fff`,
            
        2: `graph TD
            A[Behavioral Mutations] --> B[fruitless Gene]
            A --> C[period Gene]
            B --> D[Courtship Behavior]
            C --> E[Circadian Rhythm]
            D --> F[Mating Success]
            E --> G[Activity Patterns]
            F --> H[Reproductive Fitness]
            G --> H
            
            style A fill:#ff6b6b,color:#fff
            style B fill:#74c0fc,color:#fff
            style C fill:#74c0fc,color:#fff
            style D fill:#51cf66,color:#fff
            style E fill:#51cf66,color:#fff
            style F fill:#51cf66,color:#fff
            style G fill:#51cf66,color:#fff
            style H fill:#b197fc,color:#fff`,
            
        // Additional levels 3-5 would follow the same pattern
        3: `graph TD
            A[Behavioral Gene Network] --> B[fruitless Splicing]
            A --> C[doublesex Regulation]
            B --> D[Male-Specific fru]
            C --> E[Sex Determination]
            D --> F[P1 Neuron Specification]
            E --> G[Sexual Dimorphism]
            F --> H[Courtship Circuit]
            G --> I[Behavioral Dimorphism]
            H --> J[Courtship Song]
            I --> K[Mating Behavior]
            J --> K
            K --> L[Species Recognition]
            
            style A fill:#ff6b6b,color:#fff
            style B fill:#ffd43b,color:#000
            style C fill:#ffd43b,color:#000
            style D fill:#74c0fc,color:#fff
            style E fill:#74c0fc,color:#fff
            style F fill:#51cf66,color:#fff
            style G fill:#51cf66,color:#fff
            style H fill:#51cf66,color:#fff
            style I fill:#51cf66,color:#fff
            style J fill:#74c0fc,color:#fff
            style K fill:#51cf66,color:#fff
            style L fill:#b197fc,color:#fff`,
            
        4: `graph TD
            A[Sex Determination Cascade] --> B[doublesex Splicing]
            A --> C[fruitless Splicing]
            B --> D[DsxM Protein]
            B --> E[DsxF Protein]
            C --> F[FruM Protein]
            D --> G[Male Behavioral Program]
            E --> H[Female Behavioral Program]
            F --> I[Male Courtship Network]
            G --> J[Male-Specific Neurons]
            H --> K[Female-Specific Neurons]
            I --> L[P1 Cluster Activation]
            J --> M[Courtship Initiation]
            K --> N[Receptivity Modulation]
            L --> O[Courtship Song Production]
            M --> P[Courtship Sequence]
            N --> Q[Mating Acceptance]
            O --> R[Species-Specific Song]
            P --> S[Mating Behavior]
            Q --> S
            R --> T[Acoustic Communication]
            S --> U[Reproductive Success]
            T --> U
            
            style A fill:#ff6b6b,color:#fff
            style B fill:#ffd43b,color:#000
            style C fill:#ffd43b,color:#000
            style D fill:#74c0fc,color:#fff
            style E fill:#74c0fc,color:#fff
            style F fill:#74c0fc,color:#fff
            style G fill:#51cf66,color:#fff
            style H fill:#51cf66,color:#fff
            style I fill:#51cf66,color:#fff
            style J fill:#51cf66,color:#fff
            style K fill:#51cf66,color:#fff
            style L fill:#51cf66,color:#fff
            style M fill:#74c0fc,color:#fff
            style N fill:#74c0fc,color:#fff
            style O fill:#74c0fc,color:#fff
            style P fill:#51cf66,color:#fff
            style Q fill:#51cf66,color:#fff
            style R fill:#74c0fc,color:#fff
            style S fill:#51cf66,color:#fff
            style T fill:#74c0fc,color:#fff
            style U fill:#b197fc,color:#fff`,
            
        5: `graph TD
            A[Chromosomal Sex Determination] --> B[Sex-lethal Regulation]
            B --> C[transformer Splicing Control]
            C --> D[doublesex Alternative Splicing]
            C --> E[fruitless Alternative Splicing]
            D --> F[DsxM Transcription Factor]
            D --> G[DsxF Transcription Factor]
            E --> H[FruM Transcription Factor]
            F --> I[Male Behavioral Gene Network]
            G --> J[Female Behavioral Gene Network]
            H --> K[Male Courtship Gene Network]
            I --> L[takeout Expression]
            I --> M[Ion Channel Regulation]
            J --> N[Receptivity Genes]
            J --> O[Egg-laying Behavior]
            K --> P[P1 Neuron Differentiation]
            K --> Q[Courtship Song Circuitry]
            L --> R[Male Pheromone Production]
            M --> S[Neural Excitability]
            N --> T[Female Receptivity]
            O --> U[Oviposition Behavior]
            P --> V[Courtship Initiation Circuit]
            Q --> W[Wing Extension Motor Program]
            R --> X[Chemical Communication]
            S --> Y[Behavioral Responsiveness]
            T --> Z[Mating Acceptance]
            U --> AA[Reproductive Behavior]
            V --> BB[Visual Courtship Tracking]
            W --> CC[Acoustic Courtship Signals]
            X --> DD[Pheromonal Recognition]
            Y --> EE[Behavioral Integration]
            Z --> FF[Copulation Success]
            AA --> FF
            BB --> GG[Multimodal Courtship]
            CC --> GG
            DD --> GG
            EE --> HH[Behavioral Flexibility]
            FF --> II[Reproductive Fitness]
            GG --> II
            HH --> II
            II --> JJ[Evolutionary Success]
            
            style A fill:#ff6b6b,color:#fff
            style B fill:#ffd43b,color:#000
            style C fill:#ffd43b,color:#000
            style D fill:#ffd43b,color:#000
            style E fill:#ffd43b,color:#000
            style F fill:#74c0fc,color:#fff
            style G fill:#74c0fc,color:#fff
            style H fill:#74c0fc,color:#fff
            style I fill:#51cf66,color:#fff
            style J fill:#51cf66,color:#fff
            style K fill:#51cf66,color:#fff
            style L fill:#74c0fc,color:#fff
            style M fill:#74c0fc,color:#fff
            style N fill:#74c0fc,color:#fff
            style O fill:#74c0fc,color:#fff
            style P fill:#51cf66,color:#fff
            style Q fill:#51cf66,color:#fff
            style R fill:#74c0fc,color:#fff
            style S fill:#74c0fc,color:#fff
            style T fill:#74c0fc,color:#fff
            style U fill:#74c0fc,color:#fff
            style V fill:#51cf66,color:#fff
            style W fill:#51cf66,color:#fff
            style X fill:#51cf66,color:#fff
            style Y fill:#51cf66,color:#fff
            style Z fill:#51cf66,color:#fff
            style AA fill:#51cf66,color:#fff
            style BB fill:#51cf66,color:#fff
            style CC fill:#51cf66,color:#fff
            style DD fill:#51cf66,color:#fff
            style EE fill:#51cf66,color:#fff
            style FF fill:#74c0fc,color:#fff
            style GG fill:#74c0fc,color:#fff
            style HH fill:#74c0fc,color:#fff
            style II fill:#74c0fc,color:#fff
            style JJ fill:#b197fc,color:#fff`
    }
}

// To add these to your HTML file:
// 1. Open collections/eukaryotic/d_melanogaster_batch01_development_genetics.html
// 2. Find the allProcesses object in the JavaScript section
// 3. Add the processes above after process 3
// 4. Add corresponding HTML sections for processes 4 and 5 following the same pattern
// 5. Update the table of contents with the new process links

// You can also add the HTML sections for these processes:

/*
<!-- Process 4: Neural Development -->
<div class="process-item" id="neural-development">
    <h3><a href="#neural-development" class="anchor-link">4. Neural Development</a></h3>
    <p>Interactive analysis of D. melanogaster neural development with 5 detail levels showing neuroblast formation and neural circuit assembly.</p>
    <div class="slider-container">
        <label for="slider-4">Detail Level: <span id="level-4">1</span></label>
        <input type="range" id="slider-4" class="slider" min="1" max="5" value="1" oninput="updateFlowchart(4, this.value)">
        <div class="slider-labels">
            <span>Basic</span><span>Detailed</span><span>Complex</span><span>Advanced</span><span>Complete</span>
        </div>
    </div>
    <div class="mermaid-container">
        <div class="mermaid" id="chart-4"></div>
    </div>
    <div class="color-legend">
        <span><span class="color-box" style="background:#ff6b6b;"></span>Triggers & Conditions</span>
        <span><span class="color-box" style="background:#ffd43b;"></span>Catalysts & Enzymes</span>
        <span><span class="color-box" style="background:#51cf66;"></span>Chemical Processing</span>
        <span><span class="color-box" style="background:#74c0fc;"></span>Intermediates</span>
        <span><span class="color-box" style="background:#b197fc;"></span>Products</span>
    </div>
</div>

<!-- Process 5: Behavioral Genetics -->
<div class="process-item" id="behavioral-genetics">
    <h3><a href="#behavioral-genetics" class="anchor-link">5. Behavioral Genetics</a></h3>
    <p>Interactive analysis of D. melanogaster behavioral genetics with 5 detail levels showing genetic control of behavior.</p>
    <div class="slider-container">
        <label for="slider-5">Detail Level: <span id="level-5">1</span></label>
        <input type="range" id="slider-5" class="slider" min="1" max="5" value="1" oninput="updateFlowchart(5, this.value)">
        <div class="slider-labels">
            <span>Basic</span><span>Detailed</span><span>Complex</span><span>Advanced</span><span>Complete</span>
        </div>
    </div>
    <div class="mermaid-container">
        <div class="mermaid" id="chart-5"></div>
    </div>
    <div class="color-legend">
        <span><span class="color-box" style="background:#ff6b6b;"></span>Triggers & Conditions</span>
        <span><span class="color-box" style="background:#ffd43b;"></span>Catalysts & Enzymes</span>
        <span><span class="color-box" style="background:#51cf66;"></span>Chemical Processing</span>
        <span><span class="color-box" style="background:#74c0fc;"></span>Intermediates</span>
        <span><span class="color-box" style="background:#b197fc;"></span>Products</span>
    </div>
</div>
*/