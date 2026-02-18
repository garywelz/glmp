// GLMP Viewer - Main JavaScript
// Handles process loading, navigation, and Mermaid rendering

// Import modules
import { CONFIG, FEEDBACK_ENDPOINT, MERMAID_CONFIG } from './modules/config.js';
import { showHome, showProcessList, showProcessView, showAbout, hideAllViews } from './modules/navigation.js';
import { loadProcessList, loadProcess, getCurrentProcess, getProcessList, setCurrentProcess } from './modules/processLoader.js';
import { renderDiagram, updateDetailLevel, getDetailLevel } from './modules/mermaidRenderer.js';
import { initializeFeedbackPanel } from './modules/feedbackHandler.js';
import { loadComments } from './modules/commentsManager.js';
import { renderProcessList, renderProcess, renderColorLegend, renderCitations, renderMetadata, showLoadingSpinner } from './modules/uiRenderer.js';

// Initialize Mermaid
mermaid.initialize(MERMAID_CONFIG);

// Create debug function immediately (before page loads)
window.debugFeedbackPanel = () => {
    const el = document.getElementById('feedback-process-id');
    if (!el) {
        console.error('❌ feedback-process-id element not found!');
        return;
    }
    const rect = el.getBoundingClientRect();
    const computed = window.getComputedStyle(el);
    console.log('🔍 Process ID Element Debug:', {
        textContent: el.textContent,
        innerHTML: el.innerHTML,
        innerText: el.innerText,
        width: rect.width,
        height: rect.height,
        top: rect.top,
        left: rect.left,
        display: computed.display,
        visibility: computed.visibility,
        opacity: computed.opacity,
        color: computed.color,
        backgroundColor: computed.backgroundColor,
        fontSize: computed.fontSize,
        fontWeight: computed.fontWeight,
        zIndex: computed.zIndex,
        parent: el.parentElement?.tagName,
        parentDisplay: el.parentElement ? window.getComputedStyle(el.parentElement).display : 'N/A',
        isVisible: rect.width > 0 && rect.height > 0 && computed.display !== 'none' && computed.visibility !== 'hidden'
    });
    console.log('🔍 Element in DOM:', el);
    return el;
};

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    initializeViewer();
});

/**
 * Initialize the viewer
 */
async function initializeViewer() {
    console.log('🚀 Initializing GLMP Viewer...');
    
    try {
        // Check URL parameters for direct process loading
        const params = new URLSearchParams(window.location.search);
        const processId = params.get('process');
        
        if (processId) {
            console.log('📄 Loading specific process:', processId);
            
            // Show process view with loading state IMMEDIATELY (no double loading!)
            showProcessView();
            
            // Add back button immediately
            addBackToTableButton();
            
            document.getElementById('process-title').textContent = 'Loading process...';
            document.getElementById('mermaid-diagram').innerHTML = `
                <div class="loading-spinner">
                    <div class="spinner"></div>
                    <p>🔄 Loading process diagram...</p>
                </div>
            `;
            
            // Then load the actual process
            await loadProcessFromCard(processId);
        } else {
            // No process parameter - this shouldn't happen when accessed from database table
            // But if it does, just show empty state
            console.log('⚠️ No process parameter - showing empty state');
            hideAllViews();
            const homeView = document.getElementById('home-view');
            if (homeView) {
                homeView.style.display = 'block';
                homeView.innerHTML = '<p>No process specified. Please access this page from the database table.</p>';
            }
        }
        
        console.log('✅ Viewer initialized successfully');
        
    } catch (error) {
        console.error('❌ Failed to initialize viewer:', error);
        // Show error in main container
        const homeView = document.getElementById('home-view');
        if (homeView) {
            homeView.innerHTML = `
                <div class="error-message">
                    <h3>⚠️ Viewer Initialization Failed</h3>
                    <p><strong>Error:</strong> ${error.message}</p>
                    <button onclick="location.reload()" class="retry-btn">🔄 Reload Page</button>
                </div>
            `;
        }
    }
}

/**
 * Load and render the process list
 */
async function loadAndRenderProcessList() {
    // Show loading spinner immediately
    showLoadingSpinner();
    
    try {
        const processList = await loadProcessList();
        
        // Small delay to ensure DOM is ready
        await new Promise(resolve => setTimeout(resolve, 100));
        
        // Render the list
        renderProcessList(processList);
        
    } catch (error) {
        console.error('❌ Error loading process list:', error);
        console.error('Error details:', {
            name: error.name,
            message: error.message,
            stack: error.stack
        });
        
        // Check if we have cached process list
        const cachedList = getProcessList();
        if (cachedList && cachedList.length > 0) {
            console.log('⚠️ Using cached process list due to fetch error');
            renderProcessList(cachedList);
            // Show a warning but don't block the UI
            const listContainer = document.getElementById('process-list');
            if (listContainer) {
                const warning = document.createElement('div');
                warning.className = 'warning-message';
                warning.style.cssText = 'padding: 10px; margin: 10px 0; background: #fff3cd; border: 1px solid #ffc107; border-radius: 4px;';
                warning.innerHTML = `
                    <p><strong>⚠️ Warning:</strong> Could not refresh process list. Showing cached data.</p>
                    <p><small>Error: ${error.message}</small></p>
                `;
                listContainer.insertBefore(warning, listContainer.firstChild);
            }
        } else {
            // No cached data, show detailed error
            const listContainer = document.getElementById('process-list');
            if (listContainer) {
                const errorDetails = error.name === 'TypeError' && error.message.includes('fetch') 
                    ? 'This is likely a CORS (Cross-Origin) issue. The viewer needs to be served from the same origin as the data, or the server needs CORS headers configured.'
                    : error.message;
                
                listContainer.innerHTML = `
                    <div class="error-message">
                        <h3>⚠️ Failed to Load Processes</h3>
                        <p><strong>Error Type:</strong> ${error.name}</p>
                        <p><strong>Error Message:</strong> ${errorDetails}</p>
                        <details style="margin-top: 10px;">
                            <summary style="cursor: pointer;">Show technical details</summary>
                            <pre style="background: #f5f5f5; padding: 10px; margin-top: 5px; overflow-x: auto; font-size: 12px;">${error.stack || 'No stack trace available'}</pre>
                        </details>
                        <p style="margin-top: 15px;"><strong>Possible solutions:</strong></p>
                        <ul style="text-align: left; display: inline-block;">
                            <li>Check your internet connection</li>
                            <li>Try refreshing the page</li>
                            <li>Check browser console (F12) for more details</li>
                            <li>If testing locally, deploy to GCS for full functionality</li>
                        </ul>
                        <button onclick="location.reload()" class="retry-btn" style="margin-top: 15px;">🔄 Retry</button>
                    </div>
                `;
            }
        }
    }
}

/**
 * Load a process from a card click
 */
async function loadProcessFromCard(processId) {
    try {
        // Load the process
        const processData = await loadProcess(processId);
        
        // Store in module state
        setCurrentProcess(processData);
        
        // Show process view FIRST so elements exist in DOM
        showProcessView();
        
        // Add back button immediately after showing view
        addBackToTableButton();
        
        // Render the process
        renderProcessView(processData);
        
        // Initialize feedback panel with process context (after view is shown)
        // Try multiple times to ensure DOM is ready
        const initFeedback = () => {
            const nameEl = document.getElementById('feedback-process-name');
            const idEl = document.getElementById('feedback-process-id');
            if (nameEl && idEl) {
                console.log('✅ Feedback panel elements found, initializing...');
                initializeFeedbackPanel({
                    id: processData.id || processId,
                    name: processData.name,
                    process_id: processId
                });
            } else {
                console.warn('⚠️ Feedback panel elements not yet available, retrying...', { nameEl: !!nameEl, idEl: !!idEl });
                setTimeout(initFeedback, 50);
            }
        };
        setTimeout(initFeedback, 50);
        
        // Update URL without reload
        const url = new URL(window.location);
        url.searchParams.set('process', processId);
        window.history.pushState({}, '', url);
        
    } catch (error) {
        console.error('Error loading process:', error);
        alert(`Error loading process: ${error.message}`);
    }
}

/**
 * Add back button to process view
 */
function addBackToTableButton() {
    const processView = document.getElementById('process-view');
    if (!processView) return;
    
    // Check if button already exists
    let backBtn = document.getElementById('back-to-table-btn');
    if (!backBtn) {
        backBtn = document.createElement('button');
        backBtn.id = 'back-to-table-btn';
        backBtn.className = 'back-to-table-btn';
        backBtn.innerHTML = '← Back to GLMP Database Table';
        backBtn.onclick = () => {
            window.location.href = 'https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-database-table.html';
        };
        
        // Insert at the very top of process view
        processView.insertBefore(backBtn, processView.firstChild);
    }
}

/**
 * Render the process view
 */
function renderProcessView(process) {
    if (!process) return;
    
    console.log('🎨 renderProcessView called, process:', { 
        id: process.id, 
        name: process.name 
    });
    
    // Add back button at the top (always show it)
    addBackToTableButton();
    
    // Update title and metadata
    const titleEl = document.getElementById('process-title');
    const organismEl = document.getElementById('process-organism');
    const categoryEl = document.getElementById('process-category');
    const descEl = document.getElementById('process-desc');
    
    if (titleEl) titleEl.textContent = process.name;
    if (organismEl) organismEl.textContent = process.organism || 'Unknown';
    if (categoryEl) categoryEl.textContent = process.category || 'Uncategorized';
    if (descEl) descEl.textContent = process.description || '';
    
    // Also try to set feedback panel values here as a fallback
    const nameEl = document.getElementById('feedback-process-name');
    const idEl = document.getElementById('feedback-process-id');
    if (nameEl && idEl) {
        console.log('🔄 Fallback: Setting feedback values in renderProcessView');
        nameEl.textContent = process.name || 'Unknown process';
        idEl.textContent = process.id || 'unknown_id';
        // Force visibility
        nameEl.style.display = '';
        idEl.style.display = '';
        nameEl.style.visibility = 'visible';
        idEl.style.visibility = 'visible';
    }
    
    // Use the module's renderProcess function which handles all rendering
    renderProcess(process);
    
    // Render diagram separately (needs detail level)
    renderDiagram(process, getDetailLevel());
    
    // Load comments for this process
    if (process.id) {
        loadComments(process.id);
    }
    
    // Show/hide detail selector if process has multiple detail levels
    const detailSelector = document.getElementById('detail-selector');
    if (detailSelector) {
        if (process.detailLevels && process.detailLevels.length > 1) {
            detailSelector.style.display = 'block';
        } else {
            detailSelector.style.display = 'none';
        }
    }
}


/**
 * Handle detail level change
 */
function handleDetailLevelChange(level) {
    const updatedLevel = updateDetailLevel(level);
    
    // Re-render diagram with new detail level
    const currentProcess = getCurrentProcess();
    if (currentProcess) {
        renderDiagram(currentProcess, updatedLevel);
    }
}

// Make loadProcessFromCard available globally for onclick handlers
window.loadProcessFromCard = loadProcessFromCard;

// Handle browser back/forward buttons
window.addEventListener('popstate', () => {
    initializeViewer();
});

// Database Table navigation
document.addEventListener('DOMContentLoaded', () => {
    const dbTableBtn = document.getElementById('database-table-btn');
    if (dbTableBtn) {
        dbTableBtn.addEventListener('click', () => {
            window.open('https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-database-table.html', '_blank');
        });
    }
    
    // Handle detail level selector
    const detailSelector = document.getElementById('detail-selector');
    if (detailSelector) {
        const detailInput = detailSelector.querySelector('input[type="range"]');
        if (detailInput) {
            detailInput.addEventListener('input', (e) => {
                handleDetailLevelChange(parseInt(e.target.value));
            });
        }
    }
});
