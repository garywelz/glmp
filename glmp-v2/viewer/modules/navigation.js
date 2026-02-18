/**
 * Navigation Module
 * Handles view switching and UI state management
 */

/**
 * Show the home view with process list
 */
export function showHome() {
    hideAllViews();
    document.getElementById('home-view').style.display = 'block';
}

/**
 * Show the process list view (same as home)
 */
export function showProcessList() {
    showHome();
}

/**
 * Show the process detail view
 */
export function showProcessView() {
    hideAllViews();
    document.getElementById('process-view').style.display = 'block';
}

/**
 * Show the about page
 */
export function showAbout() {
    hideAllViews();
    // About view would go here if implemented
}

/**
 * Hide all views
 */
export function hideAllViews() {
    const views = ['home-view', 'process-view', 'about-view'];
    views.forEach(viewId => {
        const view = document.getElementById(viewId);
        if (view) {
            view.style.display = 'none';
        }
    });
}



