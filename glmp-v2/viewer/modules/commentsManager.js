/**
 * Comments Manager Module
 * Handles loading and displaying comments for processes
 */

import { FEEDBACK_ENDPOINT } from './config.js';
import { escapeHtml } from './utils.js';

/**
 * Load and display comments for a process
 * @param {string} processId - The process ID
 */
export async function loadComments(processId) {
    const commentsSection = document.getElementById('comments-section');
    const commentsContainer = document.getElementById('comments-container');
    
    if (!commentsSection || !commentsContainer) {
        console.warn('Comments section not found in DOM');
        return;
    }
    
    // Show loading state
    commentsContainer.innerHTML = '<p class="comments-loading">Loading comments...</p>';
    commentsSection.style.display = 'block';
    
    try {
        const response = await fetch(`${FEEDBACK_ENDPOINT}?processId=${encodeURIComponent(processId)}`);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const data = await response.json();
        const comments = data.comments || [];
        
        if (comments.length === 0) {
            commentsContainer.innerHTML = '<p class="comments-empty">No comments yet. Be the first to suggest an improvement!</p>';
            return;
        }
        
        // Sort comments by date (newest first)
        comments.sort((a, b) => {
            const dateA = new Date(a.createdAt || 0);
            const dateB = new Date(b.createdAt || 0);
            return dateB - dateA;
        });
        
        // Render comments
        renderComments(comments, commentsContainer);
        
    } catch (error) {
        console.error('Error loading comments:', error);
        commentsContainer.innerHTML = '<p class="comments-loading" style="color: var(--error-color);">Error loading comments. Please try again later.</p>';
    }
}

/**
 * Render comments to the container
 * @param {Array} comments - Array of comment objects
 * @param {HTMLElement} container - Container element to render into
 */
export function renderComments(comments, container) {
    let html = '';
    comments.forEach(comment => {
        const status = comment.status || 'pending';
        const createdAt = comment.createdAt ? new Date(comment.createdAt).toLocaleDateString() : 'Unknown date';
        const author = comment.author || 'Anonymous';
        const role = comment.role ? ` (${comment.role})` : '';
        
        html += `<div class="comment-item">`;
        html += `<div class="comment-header">`;
        html += `<div>`;
        html += `<span class="comment-author">${escapeHtml(author)}${escapeHtml(role)}</span>`;
        html += `<div class="comment-meta">`;
        html += `<span>${createdAt}</span>`;
        if (comment.nodeOrEdge) {
            html += `<span class="comment-node-ref">${escapeHtml(comment.nodeOrEdge)}</span>`;
        }
        html += `<span class="comment-status ${status}">${status.replace('_', ' ')}</span>`;
        html += `</div>`;
        html += `</div>`;
        html += `</div>`;
        
        html += `<div class="comment-content">`;
        html += `<div class="comment-suggestion">${escapeHtml(comment.suggestion || '')}</div>`;
        if (comment.rationale) {
            html += `<div class="comment-rationale">${escapeHtml(comment.rationale)}</div>`;
        }
        if (comment.references) {
            html += `<div class="comment-rationale"><strong>References:</strong> ${escapeHtml(comment.references)}</div>`;
        }
        html += `</div>`;
        
        // Show replies if any
        if (comment.replies && comment.replies.length > 0) {
            html += `<div class="comment-replies">`;
            comment.replies.forEach(reply => {
                const replyDate = reply.createdAt ? new Date(reply.createdAt).toLocaleDateString() : '';
                html += `<div class="comment-reply">`;
                html += `<div class="comment-reply-author">${escapeHtml(reply.author || 'System')} <small>${replyDate}</small></div>`;
                html += `<div class="comment-reply-message">${escapeHtml(reply.message || '')}</div>`;
                html += `</div>`;
            });
            html += `</div>`;
        }
        
        html += `</div>`;
    });
    
    container.innerHTML = html;
}



