# Viewer.js Modularization Plan

## Current State
- **File**: `viewer.js`
- **Size**: 1,365 lines
- **Functions**: 32 functions
- **Issues**: Monolithic, difficult to maintain

## Target Structure

```
glmp-v2/viewer/
├── index.html
├── styles.css
├── viewer.js (main entry point, ~100 lines)
├── modules/
│   ├── config.js (configuration)
│   ├── processLoader.js (process loading logic)
│   ├── mermaidRenderer.js (Mermaid rendering)
│   ├── feedbackHandler.js (feedback submission)
│   ├── commentsManager.js (comments loading/display)
│   ├── navigation.js (view switching)
│   └── uiRenderer.js (UI rendering functions)
```

## Module Breakdown

### 1. config.js (~30 lines)
**Purpose**: Centralized configuration
**Exports**:
- `CONFIG` - Paths and endpoints
- `FEEDBACK_ENDPOINT`
- Mermaid initialization settings

### 2. processLoader.js (~200 lines)
**Purpose**: Process loading and data management
**Functions**:
- `loadProcessList()`
- `loadProcess(processId)`
- `scanForProcesses()`
- `loadProcessFromCard(processId)`

**State**:
- `currentProcess`
- `processList`

### 3. mermaidRenderer.js (~200 lines)
**Purpose**: Mermaid diagram rendering
**Functions**:
- `renderDiagram()`
- `updateDetailLevel(level)`
- Node click handlers
- Error handling

### 4. feedbackHandler.js (~300 lines)
**Purpose**: Feedback submission and panel management
**Functions**:
- `initializeFeedbackPanel(processData)`
- `submitFeedback()`
- `loadComments(processId)`
- `renderComments(comments)`
- `escapeHtml(text)`

### 5. commentsManager.js (~150 lines)
**Purpose**: Comments loading and display
**Functions**:
- `loadComments(processId)`
- `renderComments(comments)`
- `addComment(comment)`
- `formatCommentDate(timestamp)`

### 6. navigation.js (~100 lines)
**Purpose**: View navigation and UI state
**Functions**:
- `showHome()`
- `showProcessList()`
- `showProcessView()`
- `showAbout()`
- `hideAllViews()`

### 7. uiRenderer.js (~300 lines)
**Purpose**: UI rendering functions
**Functions**:
- `renderProcess()`
- `renderScientificAccuracy()`
- `renderColorLegend()`
- `renderCitations()`
- `renderMetadata()`
- `renderProcessList()`
- `showLoadingSpinner()`

### 8. viewer.js (main) (~100 lines)
**Purpose**: Entry point and initialization
**Functions**:
- `initializeViewer()`
- Event listeners
- Global state initialization

## Implementation Steps

### Phase 1: Remove Unused Code
1. ✅ Remove chat modal code (unused)
2. Remove unused functions
3. Clean up dead code

### Phase 2: Extract Configuration
1. Create `modules/config.js`
2. Move CONFIG and endpoints
3. Move Mermaid initialization

### Phase 3: Extract Process Loading
1. Create `modules/processLoader.js`
2. Move process loading functions
3. Export state management

### Phase 4: Extract Rendering
1. Create `modules/mermaidRenderer.js`
2. Create `modules/uiRenderer.js`
3. Move rendering functions

### Phase 5: Extract Feedback
1. Create `modules/feedbackHandler.js`
2. Create `modules/commentsManager.js`
3. Move feedback-related code

### Phase 6: Extract Navigation
1. Create `modules/navigation.js`
2. Move view switching functions

### Phase 7: Refactor Main File
1. Update `viewer.js` to import modules
2. Keep only initialization code
3. Test thoroughly

## Benefits

1. **Maintainability**: Easier to find and fix bugs
2. **Testability**: Modules can be tested independently
3. **Reusability**: Modules can be reused elsewhere
4. **Readability**: Smaller files are easier to understand
5. **Collaboration**: Multiple developers can work on different modules

## Migration Strategy

1. **Incremental**: Extract one module at a time
2. **Test**: Test after each extraction
3. **Backup**: Keep original file until complete
4. **Documentation**: Update as we go

## Notes

- Use ES6 modules (import/export)
- Maintain backward compatibility
- Keep global state minimal
- Document module interfaces



