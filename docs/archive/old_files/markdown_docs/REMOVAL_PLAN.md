# Code Removal Plan - Unused Chat Modal

## Files to Update

### 1. viewer.js
**Lines to Remove**: 1141-1365 (chat modal code)
**Functions to Remove**:
- `openChatModal()`
- `closeChatModal()`
- `addChatMessage()`
- `sendChatMessage()`
- `showApprovalButtons()`
- `hideApprovalButtons()`
- `approveProcessGeneration()`
- `declineProcessGeneration()`

**Constants to Remove**:
- `PROCESS_SUGGESTION_ENDPOINT`
- `chatSessionId`
- `currentProcessSuggestion`

**Event Listeners to Remove**:
- Chat modal initialization (lines 1147-1197)

### 2. index.html
**Elements to Remove**:
- `process-suggestion-modal` div (line 326+)
- Any related CSS classes

**Note**: Check if modal HTML exists and remove it

## Impact Assessment

### Breaking Changes
- None - feature was unused
- No external dependencies

### Testing Required
- Verify viewer still loads
- Verify process loading works
- Verify feedback submission works
- Verify no console errors

## Implementation

1. Remove chat modal code from viewer.js
2. Remove modal HTML from index.html
3. Test thoroughly
4. Commit changes



