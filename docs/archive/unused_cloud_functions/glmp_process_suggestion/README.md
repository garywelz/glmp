# glmp_process_suggestion - Archived Function

## Status: ARCHIVED (Unused)

**Date Archived**: 2025-01-XX  
**Reason**: Replaced by simpler `glmp_simple_suggestion` system

## Original Purpose

This Cloud Function provided an AI-powered chat interface for process suggestion and generation. Users could:
1. Suggest a process via chat
2. Receive clarifying questions from AI
3. Approve/decline process generation
4. Automatically generate Mermaid diagrams and JSON files

## Why It Was Replaced

1. **Complexity**: Required session management, conversation history, and complex AI interactions
2. **Reliability Issues**: AI model initialization and availability problems
3. **User Experience**: Simple form is more straightforward for users
4. **Maintenance**: Complex codebase difficult to maintain

## Replacement

Replaced by:
- **glmp_simple_suggestion**: Simple form-based suggestion storage
- **glmp_view_suggestions**: View stored suggestions

## Files Archived

- `main.py` - Main function (475+ lines)
- `comments_storage.py` - Comment storage utilities
- `deploy.sh` - Deployment script
- `requirements.txt` - Python dependencies

## If Needed in Future

To restore:
1. Copy files back to `cloud-functions/glmp_process_suggestion/`
2. Deploy using `deploy.sh`
3. Update frontend to use the endpoint
4. Test thoroughly

## Notes

- Function is still deployed but not used
- Frontend references removed
- Consider undeploying to save resources



