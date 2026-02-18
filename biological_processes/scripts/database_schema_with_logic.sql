-- GLMP Biological Processes Database Schema with Logical Structure Analysis
-- Designed for 2,000-10,000 process scale with automated logic detection

-- Main processes table
CREATE TABLE processes (
    process_id VARCHAR(100) PRIMARY KEY,
    kingdom VARCHAR(20) NOT NULL,
    organism VARCHAR(100) NOT NULL,
    batch_name VARCHAR(100) NOT NULL,
    process_name VARCHAR(200) NOT NULL,
    process_description TEXT,
    html_file_path VARCHAR(300) NOT NULL,
    anchor_id VARCHAR(100) NOT NULL,
    direct_link VARCHAR(400) NOT NULL,
    
    -- Process metadata
    conservation_level VARCHAR(20), -- universal, kingdom, species
    functional_category VARCHAR(50),
    complexity_score INT DEFAULT 1,
    process_count_in_batch INT DEFAULT 8,
    
    -- Logical structure analysis (automated detection)
    has_and_gates BOOLEAN DEFAULT FALSE,
    has_or_gates BOOLEAN DEFAULT FALSE,
    has_feedback_loops BOOLEAN DEFAULT FALSE,
    has_checkpoints BOOLEAN DEFAULT FALSE,
    has_bistable_switches BOOLEAN DEFAULT FALSE,
    has_amplification BOOLEAN DEFAULT FALSE,
    has_competitive_inhibition BOOLEAN DEFAULT FALSE,
    has_cascades BOOLEAN DEFAULT FALSE,
    has_oscillation BOOLEAN DEFAULT FALSE,
    
    -- Logical structure counts
    and_gate_count INT DEFAULT 0,
    or_gate_count INT DEFAULT 0,
    feedback_loop_count INT DEFAULT 0,
    checkpoint_count INT DEFAULT 0,
    bistable_switch_count INT DEFAULT 0,
    amplification_count INT DEFAULT 0,
    competitive_inhibition_count INT DEFAULT 0,
    cascade_count INT DEFAULT 0,
    oscillation_count INT DEFAULT 0,
    
    -- Computed metrics
    total_logic_structures INT DEFAULT 0,
    logic_complexity_score FLOAT DEFAULT 0.0,
    
    -- Confidence scores for automated detection
    and_gate_confidence FLOAT DEFAULT 0.0,
    or_gate_confidence FLOAT DEFAULT 0.0,
    feedback_loop_confidence FLOAT DEFAULT 0.0,
    checkpoint_confidence FLOAT DEFAULT 0.0,
    bistable_switch_confidence FLOAT DEFAULT 0.0,
    
    -- Timestamps
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_analyzed TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Cross-species relationships for comparative analysis
CREATE TABLE process_orthologs (
    ortholog_id VARCHAR(100) PRIMARY KEY,
    process_group_name VARCHAR(100) NOT NULL,
    conservation_type VARCHAR(30), -- ortholog, paralog, convergent
    species_processes JSON NOT NULL, -- Array of process_ids
    conservation_score FLOAT,
    evolutionary_distance JSON,
    comparative_html_path VARCHAR(300),
    
    -- Logical structure conservation
    conserved_logic_structures JSON, -- Which logical structures are conserved
    variable_logic_structures JSON,  -- Which vary across species
    
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Organism metadata
CREATE TABLE organisms (
    organism_id VARCHAR(50) PRIMARY KEY,
    scientific_name VARCHAR(100) NOT NULL,
    common_name VARCHAR(100),
    kingdom VARCHAR(20) NOT NULL,
    phylum VARCHAR(50),
    is_model_organism BOOLEAN DEFAULT FALSE,
    genome_size BIGINT,
    total_processes INT DEFAULT 0,
    
    -- Organism-level logical structure statistics
    avg_logic_complexity FLOAT DEFAULT 0.0,
    dominant_logic_structures JSON, -- Most common structures in this organism
    unique_logic_patterns JSON,     -- Structures unique to this organism
    
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Functional categories
CREATE TABLE functional_categories (
    category_id VARCHAR(50) PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL,
    parent_category VARCHAR(50),
    description TEXT,
    typical_process_count INT DEFAULT 8,
    
    -- Category-level logical patterns
    common_logic_structures JSON, -- Structures typical for this category
    category_complexity_range JSON, -- Min/max complexity for category
    
    FOREIGN KEY (parent_category) REFERENCES functional_categories(category_id)
);

-- Logical structure definitions
CREATE TABLE logical_structures (
    structure_id VARCHAR(50) PRIMARY KEY,
    structure_name VARCHAR(100) NOT NULL,
    structure_type VARCHAR(50), -- gate, loop, switch, etc.
    description TEXT,
    complexity_weight FLOAT DEFAULT 1.0,
    detection_patterns JSON, -- Regex patterns for automated detection
    biological_significance TEXT,
    
    -- Examples and references
    example_processes JSON, -- Process IDs that demonstrate this structure
    literature_references JSON
);

-- Analysis results log
CREATE TABLE analysis_log (
    log_id SERIAL PRIMARY KEY,
    file_path VARCHAR(300) NOT NULL,
    analysis_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    analyzer_version VARCHAR(20),
    structures_detected JSON,
    confidence_scores JSON,
    analysis_duration_ms INT,
    
    -- Quality metrics
    detection_quality_score FLOAT,
    manual_verification_status VARCHAR(20) -- pending, verified, corrected
);

-- Views for common queries

-- Processes with specific logical structures
CREATE VIEW processes_with_and_gates AS
SELECT process_id, organism, process_name, and_gate_count, and_gate_confidence
FROM processes 
WHERE has_and_gates = TRUE
ORDER BY and_gate_count DESC;

CREATE VIEW processes_with_feedback_loops AS
SELECT process_id, organism, process_name, feedback_loop_count, feedback_loop_confidence
FROM processes 
WHERE has_feedback_loops = TRUE
ORDER BY feedback_loop_count DESC;

-- Most complex processes by organism
CREATE VIEW complexity_by_organism AS
SELECT 
    organism,
    COUNT(*) as process_count,
    AVG(logic_complexity_score) as avg_complexity,
    MAX(logic_complexity_score) as max_complexity,
    SUM(total_logic_structures) as total_structures
FROM processes 
GROUP BY organism
ORDER BY avg_complexity DESC;

-- Cross-kingdom logical structure comparison
CREATE VIEW logic_structures_by_kingdom AS
SELECT 
    kingdom,
    SUM(and_gate_count) as total_and_gates,
    SUM(or_gate_count) as total_or_gates,
    SUM(feedback_loop_count) as total_feedback_loops,
    SUM(bistable_switch_count) as total_bistable_switches,
    AVG(logic_complexity_score) as avg_complexity
FROM processes 
GROUP BY kingdom
ORDER BY avg_complexity DESC;

-- Sample queries for database integration

-- Find all processes with bistable switches
-- SELECT * FROM processes WHERE has_bistable_switches = TRUE;

-- Find most logically complex processes
-- SELECT process_name, organism, logic_complexity_score, total_logic_structures 
-- FROM processes ORDER BY logic_complexity_score DESC LIMIT 10;

-- Compare logical complexity across kingdoms
-- SELECT * FROM logic_structures_by_kingdom;

-- Find processes suitable for teaching specific logical concepts
-- SELECT process_name, organism, feedback_loop_count, direct_link
-- FROM processes 
-- WHERE has_feedback_loops = TRUE AND feedback_loop_confidence > 0.8
-- ORDER BY feedback_loop_count DESC;