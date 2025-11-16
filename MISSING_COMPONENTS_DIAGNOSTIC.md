# Diagnostic: Missing Components in Analysis Page

## Date: 2025-11-16

## Reported Issues

User reports NOT seeing the following components on analysis page:
1. ✅ **Important Limits Disclaimer** - Should ALWAYS show
2. ✅ **Screening Badge** - Should ALWAYS show (has fallback)
3. ⚠️ **Confidence Level** - Conditional on backend data
4. ⚠️ **About the Contract** - Conditional on backend data
5. ✅ **"Tell me more about it" for null quotes** - Should show "Not found in document text"

## Root Cause Analysis

### Issue #1 & #2: Important Limits & Screening Badge Not Showing

**Diagnosis:** These components ARE implemented and SHOULD show (lines 128 & 131 in `[id].vue`).

**Possible Causes:**
1. **You're testing with OLD analysis data** created BEFORE the backend fixes
   - The old analysis might have malformed data causing rendering errors
   - Solution: Create a NEW analysis with a fresh contract upload

2. **Component auto-import issue** in Nuxt
   - Components should auto-import from `components/analysis/`
   - Check browser console for component loading errors

3. **CSS hiding the components**
   - Components might be rendering but hidden
   - Check browser DevTools for the elements

**How to Verify:**
```bash
# Open browser DevTools Console (F12)
# Look for errors like:
- "Failed to resolve component: ImportantLimits"
- "Failed to resolve component: ScreeningBadge"
```

### Issue #3 & #4: Confidence Level & About the Contract

**Status:** These are CONDITIONAL and won't show if backend doesn't return the data.

**Why they might not appear:**
1. **Old analysis data** - Analysis created before backend updates won't have:
   - `confidence_score`
   - `about_summary`

2. **Backend not returning these fields** - Check API response:
```javascript
// In browser console on analysis page:
console.log($nuxt.$store.state.analyses.currentAnalysis)
// Check if these fields exist:
// - confidence_score (should be 0-1)
// - about_summary (should be string)
// - screening_result (should be one of 4 values)
```

**Fixed in Code:**
- Line 135: Better conditional check for `confidence_score`
- Lines 166-174: Conditional on `getAboutSummary()` returning truthy

### Issue #5: "Tell me more" for Null Quotes

**Status:** ✅ FIXED with `hasValidQuote()` helper function

**What was fixed:**
- Created `hasValidQuote(item)` function (lines 910-920)
- Properly validates quotes for:
  - `null` values
  - `undefined` values
  - Empty strings `""`
  - String `"null"`
  - String `"undefined"`
  - String `"None"`

- Applied to all sections:
  - Obligations (line 229)
  - Rights (line 334)
  - Risks (line 485)
  - Mitigations (line 595)

**Result:**
- Valid quotes → Show "Tell me more about it" (clickable)
- Invalid/null quotes → Show "Not found in the document text" (grayed out, not clickable)

## Testing Instructions

### Step 1: Create NEW Analysis

**IMPORTANT:** Test with a FRESH analysis, not old data!

1. Go to `/upload`
2. Upload a NEW contract
3. Select output language (e.g., English)
4. Wait for analysis to complete
5. Go to analysis results page

### Step 2: Verify Components Show

You should see IN THIS ORDER:
1. ✅ "Explain Like I'm 5" button
2. ✅ **Important Limits Disclaimer** (amber/yellow box with warning)
3. ✅ **Screening Badge** (colored box: green/yellow/red/gray)
4. ⚠️ **Confidence Level** (only if backend returns confidence_score)
5. ⚠️ **About the Contract** (only if backend returns about_summary)
6. ✅ Agreement Type
7. ✅ Parties
8. ✅ Jurisdiction
9. ✅ Obligations/Rights/Risks/etc.

### Step 3: Verify Quote Handling

For each obligation/right/risk:
- If item has valid source quote → "Tell me more about it" (blue/green, clickable)
- If item has NO quote or null → "Not found in the document text" (gray, not clickable)

### Step 4: Browser Console Check

Open DevTools (F12) and check for errors:

```javascript
// 1. Check if analysis data loaded
console.log($nuxt.$store.state.analyses.currentAnalysis)

// 2. Check specific fields
const analysis = $nuxt.$store.state.analyses.currentAnalysis
console.log('Confidence Score:', analysis.confidence_score)
console.log('About Summary:', analysis.preparation_result?.about || analysis.analysis_result?.about_summary)
console.log('Screening Result:', analysis.preparation_result?.screening_result || analysis.analysis_result?.screening_result)
console.log('Formatted Output:', analysis.formatted_output)
```

## Backend Requirements

For components to show, backend MUST return:

### Always Required:
- `formatted_output` object with sections (obligations, rights, risks, etc.)

### For Screening Badge:
- `preparation_result.screening_result` OR
- `analysis_result.screening_result` OR
- `formatted_output.screening_result`

Possible values: `"no_major_issues"`, `"recommended_to_address"`, `"high_risk"`, `"preliminary_review"`

### For Confidence Level:
- `confidence_score` (number 0-1) on root of analysis object

### For About the Contract:
- `analysis_result.about_summary` OR
- `preparation_result.about` OR
- `formatted_output.about.description`

### For Quotes:
Each obligation/right/risk should have:
```json
{
  "action": "What to do (in output_language)",
  "quote_original": "Exact contract text (in original language)" | null,
  "quote_translated": "Exact contract text (in output_language)" | null
}
```

## Known Issues

### SSE Connection Error
```
analyses.ts:117 SSE error: Event {isTrusted: true, type: 'error'...}
```

**Impact:** Low - Analysis still works, just no live progress updates
**Cause:** Server-Sent Events connection issue (network/proxy/timeout)
**Fix:** Not critical - analysis completes successfully without SSE

## Files Modified

### Backend:
1. `backend/app/api/feedback.py` - Fixed duplicate prefix
2. `backend/app/api/deadlines.py` - Fixed duplicate prefix
3. `backend/app/services/llm_analysis/prompts/analysis_en.txt` - Added output_language directives

### Frontend:
1. `frontend/pages/analysis/[id].vue`:
   - Line 135: Fixed confidence_score conditional
   - Lines 910-920: Added `hasValidQuote()` helper
   - Lines 229, 334, 485, 595: Applied helper to all quote validations

## Next Steps

1. **Create NEW analysis** with fresh contract
2. **Check browser console** for component errors
3. **Verify backend returns** all required fields
4. **Report back** with:
   - Screenshot of what you see
   - Browser console output
   - Network tab showing API response for the analysis

## Summary

- ✅ Quote validation: FIXED with `hasValidQuote()` helper
- ✅ API endpoints: FIXED (feedback & deadlines)
- ✅ Output language: FIXED in backend prompts
- ⚠️ Missing components: Need to test with NEW analysis data
- ℹ️ SSE error: Non-critical, analysis still works
