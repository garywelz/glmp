/**
 * Feedback Handler Module
 * Handles feedback submission and panel initialization
 */

import { FEEDBACK_ENDPOINT } from './config.js';
import { loadComments } from './commentsManager.js';

/**
 * Initialize the feedback panel with process data
 * @param {Object} processData - The process data object
 */
export function initializeFeedbackPanel(processData) {
    console.log('🔧 initializeFeedbackPanel called with:', processData);
    
    const nameEl = document.getElementById('feedback-process-name');
    const idEl = document.getElementById('feedback-process-id');
    
    if (!nameEl || !idEl) {
        console.error('❌ Feedback panel elements not found in DOM');
        return;
    }

    const processName = processData?.name || processData?.title || 'Unknown process';
    const processId = processData?.id || processData?.process_id || 'unknown_id';
    
    // Set text content
    nameEl.textContent = processName;
    idEl.textContent = processId;
    
    // Style the process ID element
    idEl.style.setProperty('font-weight', '600', 'important');
    idEl.style.setProperty('color', 'var(--primary-color)', 'important');
    idEl.style.setProperty('font-size', '0.9rem', 'important');
    idEl.style.setProperty('min-width', '150px', 'important');
    idEl.style.setProperty('display', 'inline-block', 'important');
    idEl.style.setProperty('visibility', 'visible', 'important');
    idEl.style.setProperty('opacity', '1', 'important');
    
    // Store processData for use in submit handler
    window.currentProcessData = processData;

    const submitBtn = document.getElementById('feedback-submit');
    const statusEl = document.getElementById('feedback-status');
    if (!submitBtn || !statusEl) {
        console.error('❌ Feedback submit button or status element not found!');
        return;
    }
    
    // Remove any existing handlers and attach new one
    submitBtn.onclick = null;
    submitBtn.addEventListener('click', async (e) => {
        e.preventDefault();
        e.stopPropagation();
        
        await submitFeedback(processId, processName, statusEl, submitBtn);
    });
    
    // Load comments for this process
    loadComments(processId);
}

/**
 * Submit feedback to the server
 * @param {string} processId - Process ID
 * @param {string} processName - Process name
 * @param {HTMLElement} statusEl - Status element to update
 * @param {HTMLElement} submitBtn - Submit button element
 */
async function submitFeedback(processId, processName, statusEl, submitBtn) {
    console.log('🖱️ Submit button clicked');
    statusEl.textContent = '';

    const issueType   = document.getElementById('feedback-issue-type')?.value || '';
    const nodeRef     = document.getElementById('feedback-node')?.value.trim() || '';
    const suggestion  = document.getElementById('feedback-suggestion')?.value.trim() || '';
    const why         = document.getElementById('feedback-why')?.value.trim() || '';
    const refs        = document.getElementById('feedback-refs')?.value.trim() || '';
    const role        = document.getElementById('feedback-role')?.value || '';
    const email       = document.getElementById('feedback-email')?.value.trim() || '';
    const okContact   = document.getElementById('feedback-ok-contact')?.checked || false;
    const consent     = document.getElementById('feedback-consent')?.checked || false;

    // Validation
    if (!issueType) {
        statusEl.textContent = 'Please select an issue type.';
        return;
    }
    if (!suggestion) {
        statusEl.textContent = 'Please enter your suggestion.';
        return;
    }
    if (!consent) {
        statusEl.textContent = 'Please confirm the consent checkbox before submitting.';
        return;
    }
    
    const payload = {
        processId: processId,
        processName: processName,
        issueType,
        nodeOrEdge: nodeRef,
        suggestion,
        rationale: why,
        references: refs,
        role,
        email,
        okToContact: okContact,
        userAgent: navigator.userAgent,
        submittedAt: new Date().toISOString()
    };
    
    console.log('📤 Submitting feedback:', payload);

    submitBtn.disabled = true;
    submitBtn.style.opacity = '0.7';
    statusEl.textContent = 'Submitting…';

    try {
        const res = await fetch(FEEDBACK_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        const responseText = await res.text();
        console.log('📥 Response status:', res.status, res.statusText);

        if (!res.ok) {
            let errorMsg = `Server responded with ${res.status}`;
            try {
                const errorData = JSON.parse(responseText);
                if (errorData.error) {
                    errorMsg += `: ${errorData.error}`;
                }
            } catch (e) {
                if (responseText) {
                    errorMsg += `: ${responseText}`;
                }
            }
            throw new Error(errorMsg);
        }

        statusEl.textContent = '✅ Thank you — your feedback has been submitted and will appear in the comments section.';
        statusEl.style.color = 'var(--success-color)';

        // Reload comments to show the new one
        setTimeout(() => {
            loadComments(processId);
        }, 1000);

        // Reset form
        resetFeedbackForm();
        
    } catch (error) {
        console.error('❌ Feedback submission failed:', error);
        statusEl.textContent = `❌ Error: ${error.message}. Please check the console for details or try again later.`;
        statusEl.style.color = 'var(--error-color)';
    } finally {
        submitBtn.disabled = false;
        submitBtn.style.opacity = '1';
    }
}

/**
 * Reset the feedback form
 */
function resetFeedbackForm() {
    document.getElementById('feedback-issue-type').value = '';
    document.getElementById('feedback-node').value = '';
    document.getElementById('feedback-suggestion').value = '';
    document.getElementById('feedback-why').value = '';
    document.getElementById('feedback-refs').value = '';
    document.getElementById('feedback-role').value = '';
    document.getElementById('feedback-email').value = '';
    document.getElementById('feedback-ok-contact').checked = false;
    document.getElementById('feedback-consent').checked = false;
    
    // Clear node hint
    const nodeHint = document.getElementById('feedback-node-hint');
    if (nodeHint) {
        nodeHint.textContent = 'Tip: tap a node in the diagram to auto-fill this field.';
        nodeHint.style.color = '';
    }
}



