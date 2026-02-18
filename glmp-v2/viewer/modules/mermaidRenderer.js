/**
 * Mermaid Renderer Module
 * Handles Mermaid diagram rendering and node interaction
 */

let currentDetailLevel = 1;

/**
 * Render the Mermaid diagram
 * @param {Object} process - The process data object
 * @param {number} detailLevel - Current detail level (1-based)
 */
export async function renderDiagram(process, detailLevel = 1) {
    const diagramContainer = document.getElementById('mermaid-diagram');
    if (!diagramContainer) {
        console.error('Diagram container not found');
        return;
    }
    
    // Get Mermaid code (either single or based on detail level)
    let mermaidCode = process.mermaid;
    
    // If process has detail levels, use the current one
    if (process.detailLevels) {
        const detailLevelObj = process.detailLevels[detailLevel - 1];
        if (detailLevelObj && detailLevelObj.mermaid) {
            mermaidCode = detailLevelObj.mermaid;
        }
    }
    
    // Trim any leading/trailing whitespace and ensure proper format
    mermaidCode = mermaidCode.trim();
    
    // Clear previous diagram
    diagramContainer.innerHTML = '';
    
    try {
        // Create a unique ID for this diagram
        const diagramId = 'mermaid-' + Date.now();
        const mermaidDiv = document.createElement('div');
        mermaidDiv.id = diagramId;
        mermaidDiv.className = 'mermaid';
        mermaidDiv.textContent = mermaidCode;
        diagramContainer.appendChild(mermaidDiv);
        
        // Render using mermaid.render() - the modern async API
        console.log('🎨 Rendering Mermaid diagram...');
        const { svg } = await mermaid.render(diagramId + '-svg', mermaidCode);
        mermaidDiv.innerHTML = svg;
        console.log('✅ Mermaid diagram rendered, SVG length:', svg.length);

        // Wire up node click handlers
        wireNodeClickHandlers(mermaidDiv, mermaidCode);
        
    } catch (error) {
        console.error('🔴 MERMAID RENDER ERROR:', error);
        console.error('Error message:', error.message);
        console.error('Error stack:', error.stack);
        console.error('Mermaid code (first 500 chars):', mermaidCode.substring(0, 500));
        
        // Display error in diagram container
        diagramContainer.innerHTML = `
            <div class="error-message" style="padding: 20px; background: #fee; border: 2px solid #f00; border-radius: 8px;">
                <h3 style="color: #c00; margin-top: 0;">❌ Mermaid Syntax Error</h3>
                <p><strong>Error:</strong> ${error.message || 'Unknown error'}</p>
                <details style="margin-top: 10px;">
                    <summary style="cursor: pointer; color: #0066cc;">Show error details</summary>
                    <pre style="background: #fff; padding: 10px; overflow-x: auto; margin-top: 10px;">${error.stack || JSON.stringify(error, null, 2)}</pre>
                </details>
            </div>
        `;
    }
}

/**
 * Wire up click handlers for nodes to populate feedback form
 */
function wireNodeClickHandlers(mermaidDiv, mermaidCode) {
    try {
        const svgElement = mermaidDiv.querySelector('svg');
        if (!svgElement) return;
        
        const nodeGroups = svgElement.querySelectorAll('g.node');
        const nodeInput = document.getElementById('feedback-node');
        const nodeHint = document.getElementById('feedback-node-hint');

        console.log(`🔍 Found ${nodeGroups.length} node groups, wiring click handlers...`);
        
        if (nodeGroups && nodeGroups.length && nodeInput) {
            let nodesWired = 0;
            nodeGroups.forEach((nodeGroup) => {
                // Make the entire node group clickable
                nodeGroup.style.cursor = 'pointer';
                
                // Find the node ID from the group's ID attribute
                const groupId = nodeGroup.getAttribute('id') || '';
                
                // Extract node ID (format: flowchart-XXX-YY or node-XXX-YY)
                let nodeId = '';
                const idMatch = groupId.match(/(?:flowchart-|node-)?([A-Z][A-Z0-9]*)(?:-\d+)?/);
                if (idMatch && idMatch[1]) {
                    nodeId = idMatch[1];
                }
                
                // Try to extract label text from the node's text elements
                const labelEl = nodeGroup.querySelector('.nodeLabel, .label, text');
                let labelText = '';
                if (labelEl) {
                    labelText = labelEl.textContent || labelEl.innerText || '';
                    if (!labelText) {
                        const allTexts = nodeGroup.querySelectorAll('text, tspan');
                        const texts = Array.from(allTexts).map(t => t.textContent).filter(t => t && t.trim());
                        labelText = texts.join(' ').trim();
                    }
                    labelText = labelText.trim();
                }
                
                // If we couldn't get nodeId from group ID, try to find it in the Mermaid code
                if (!nodeId && labelText) {
                    const escapedLabel = labelText.substring(0, 20).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
                    const labelPattern = new RegExp(`([A-Z][A-Z0-9]*)\\[.*?${escapedLabel}.*?\\]`, 'i');
                    const codeMatch = mermaidCode.match(labelPattern);
                    if (codeMatch && codeMatch[1]) {
                        nodeId = codeMatch[1];
                    }
                }
                
                // Add title attribute for hover tooltip
                if (nodeId || labelText) {
                    const tooltipText = labelText ? `${nodeId || 'Node'}: ${labelText}` : (nodeId || 'Node');
                    nodeGroup.setAttribute('title', tooltipText);
                    
                    // Also add to all child elements for better hover coverage
                    const childElements = nodeGroup.querySelectorAll('rect, circle, ellipse, polygon, path, text, g');
                    childElements.forEach(el => {
                        if (!el.getAttribute('title')) {
                            el.setAttribute('title', tooltipText);
                        }
                    });
                    
                    // Store node info in data attributes
                    nodeGroup.setAttribute('data-node-id', nodeId || '');
                    nodeGroup.setAttribute('data-node-label', labelText || '');
                }

                // Add click handler
                nodeGroup.addEventListener('click', (e) => {
                    e.stopPropagation();
                    if (nodeId) {
                        nodeInput.value = nodeId;
                        if (nodeHint) {
                            const displayText = labelText ? `${nodeId} (${labelText.substring(0, 40)}${labelText.length > 40 ? '...' : ''})` : nodeId;
                            nodeHint.textContent = `Selected: ${displayText}`;
                            nodeHint.style.color = 'var(--primary-color)';
                        }
                        // Scroll feedback panel into view
                        const feedbackPanel = document.getElementById('feedback-panel');
                        if (feedbackPanel) {
                            feedbackPanel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                        }
                    }
                });
                nodesWired++;
            });
            console.log(`✅ Wired ${nodesWired} nodes with click handlers`);
        }
    } catch (wiringError) {
        console.warn('Could not wire feedback node click handlers:', wiringError);
    }
}

/**
 * Update detail level
 * @param {number} level - Detail level (1-based)
 * @returns {number} Updated detail level
 */
export function updateDetailLevel(level) {
    currentDetailLevel = parseInt(level);
    const labels = ['Basic', 'Detailed', 'Complex', 'Advanced', 'Complete'];
    const detailLabel = document.getElementById('detail-label');
    if (detailLabel) {
        detailLabel.textContent = `${labels[currentDetailLevel - 1]} (${currentDetailLevel})`;
    }
    return currentDetailLevel;
}

/**
 * Get current detail level
 */
export function getDetailLevel() {
    return currentDetailLevel;
}

