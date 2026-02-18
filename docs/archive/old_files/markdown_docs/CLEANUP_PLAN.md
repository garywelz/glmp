# GLMP Directory Cleanup Plan

## Status: Stringent Response Fix Attempts
- **Note**: Multiple attempts to fix `ecoli_stringent_response.json` failed
- **Action**: May need to delete this process or regenerate from scratch
- **Scripts to remove**: All `fix_stringent_*.py` scripts in `/scripts/`

## Cleanup Categories

### 1. Temporary Fix Scripts (Can be removed)
- `scripts/fix_stringent_*.py` (all 8 files)
- `scripts/fix_fatty_acid_slash_issue.py` (already fixed)
- `scripts/fix_remaining_syntax_errors.py` (already fixed)
- `scripts/fix_three_syntax_errors.py` (already fixed)
- `scripts/regenerate_stringent_mermaid.py` (temporary)

### 2. Old HTML Files (Archive or remove)
- Multiple `ecoli_batch*.html` files
- Old `lac_operon_*.html` files
- `beta_galactosidase_*.html` files
- Various standalone HTML files

### 3. Old Deployment Scripts (Archive)
- Multiple `DEPLOY_*.sh` scripts (many are outdated)
- Keep only current deployment scripts

### 4. Documentation Files (Organize)
- Many handoff/summary MD files (archive to `docs/archive/`)
- Keep only current/active documentation

### 5. Temporary/Test Files
- `__pycache__/` directories
- `*.pyc` files
- Test JSON files in root

### 6. Old Scripts (Review and archive)
- Many one-time fix scripts that are no longer needed
- Keep only reusable utility scripts

## Priority Actions

1. **Immediate**: Remove stringent response fix scripts
2. **High**: Archive old HTML files
3. **Medium**: Organize documentation
4. **Low**: Clean up old deployment scripts



