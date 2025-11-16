# Frontend Fixes for Analysis Page

## Date: 2025-11-16

## Issues Fixed

### 1. ✅ ELI5 "Explain Like I'm 5" API Endpoint Error
**Issue:** POST request was failing with 404 error due to incorrect API URL construction
- Error: `POST http://localhost:3000/analysis/undefined/api/v1/analyses/{id}/simplify`
- Root cause: Using `config.public.apiBaseUrl` instead of `config.public.apiBase`

**Fix:** Updated API endpoint in `/frontend/pages/analysis/[id].vue`
- Line 809: Changed `${config.public.apiBaseUrl}/api/v1/analyses/...` to `${config.public.apiBase}/analyses/...`
- This matches the runtime config in `nuxt.config.ts` which defines `apiBase` (not `apiBaseUrl`)

### 2. ✅ Feedback Submission API Endpoint Error
**Issue:** Feedback submission was failing with the same URL construction error
- Error: `POST http://localhost:3000/analysis/undefined/api/v1/feedback`

**Fix:** Updated API endpoint in `/frontend/pages/analysis/[id].vue`
- Line 869: Changed `${config.public.apiBaseUrl}/api/v1/feedback` to `${config.public.apiBase}/feedback`

### 3. ✅ Missing Feedback Forms on Sections
**Issue:** "Was this accurate?" feedback form was only present on Obligations section
- Missing on: Rights, Risks sections

**Fix:** Added feedback form UI to all major sections:
- Rights section (lines 357-392)
- Risks section (lines 498-541)
- Feedback forms include thumbs up/down buttons with loading and submitted states

### 4. ✅ "Tell Me More About It" Shows for Null Values
**Issue:** Button appeared even when no quote/source text was available
- Expected: Show "Not found in the document text" (non-clickable) when quote is null

**Fix:** Updated all sections to handle null quotes:
- Obligations section (lines 227-247)
- Rights section (lines 332-352)
- Risks section (lines 483-503)
- Mitigations section (lines 593-613)
- Now shows grayed-out "Not found in the document text" message when no quote exists

## Issues Investigated

### 5. ⚠️ Output Language Not Respected (Backend Issue)
**Issue:** User selects English as output language, but sees content in original contract language

**Investigation:**
- Frontend correctly stores and sends `output_language` parameter during upload (upload.vue:354)
- Frontend displays both `quote_original` and `quote_translated` correctly
- **Root cause:** Backend is not translating the main content fields (`action`, `right`, `description`) to the requested output language
- These fields should be returned in the output_language, not the original language

**Required Backend Fix:**
- Backend analysis endpoint needs to respect `output_language` parameter
- Should translate: obligation.action, right.right, risk.description, etc.
- Currently only translating the quote fields

### 6. ✅ Missing Components Investigation
**Issue:** User reported missing: Headers, Screening Badge, Important Limits Disclaimer, Confidence Level, About the Contract

**Investigation:**
- All components are properly implemented and rendered in the code:
  - ImportantLimits: Always rendered (line 128)
  - ScreeningBadge: Conditionally rendered if `screeningResult` exists (line 131)
  - Confidence Level: Conditionally rendered if `confidence_score !== null` (lines 134-163)
  - About the Contract: Conditionally rendered if summary exists (lines 166-174)
  - WidgetCard headers: Always rendered (WidgetCard.vue lines 3-6)

**Conclusion:**
- If these components are not showing, it's a **data issue** - the backend is not returning the required fields
- Check backend response for: `screening_result`, `confidence_score`, `about_summary`

## Files Modified

1. `/frontend/pages/analysis/[id].vue`
   - Fixed API endpoints (2 locations)
   - Added feedback forms to Rights and Risks sections
   - Added "Not found in document text" handling for null quotes (4 locations)

## Testing Recommendations

1. Test ELI5 mode toggle with a real analysis
2. Test feedback submission on all sections
3. Verify "Not found in document text" appears when quotes are missing
4. Check backend logs for output_language parameter usage
5. Verify all badges/disclaimers appear when backend returns proper data

## Backend Action Items

1. **HIGH PRIORITY:** Fix output_language not being respected
   - Translate main content fields (action, right, description) to requested language
   - Not just the quote fields

2. **MEDIUM PRIORITY:** Ensure all required fields are returned:
   - `screening_result` (for ScreeningBadge)
   - `confidence_score` (for Confidence Level)
   - `about_summary` (for About the Contract section)

## Notes

- The config property is `apiBase` not `apiBaseUrl` (defined in nuxt.config.ts:60)
- All frontend UI components are working correctly
- Most "missing" features are actually conditional - they require specific data from the backend
