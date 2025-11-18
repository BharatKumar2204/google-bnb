# Fake News Detection System

## Problem
The system was giving high scores (55/100) to obviously fake headlines like "Scientists Confirm Cats Are Now Eligible for Tax Returns" because:
1. Keyword extraction found "cats" 
2. Search returned 10+ articles about cats (unrelated to tax returns)
3. Score was based only on quantity, not relevance

## Solution
Implemented a **3-layer fake news detection system**:

### Layer 1: Absurdity Detection (AI-Powered)
Uses Gemini 2.5 Pro to detect obviously fake or absurd claims by checking:
- Physical impossibility or violation of natural laws
- Satirical content (like The Onion)
- Obvious contradictions
- Extraordinary claims that would be major world news

**Example Detection:**
```
Headline: "Scientists Confirm Cats Are Now Eligible for Tax Returns"
Result: ABSURD - Animals cannot file tax returns; this violates legal and logical principles
Score: 5/100
Verdict: "Likely Fake/Satirical"
```

### Layer 2: Relevance Filtering
Filters search results to ensure articles actually match the headline topic.

**How it works:**
1. Extracts key terms from headline (excluding stop words)
2. Calculates relevance score for each article (0-1)
3. Filters out articles below 30% relevance threshold
4. Only counts relevant articles in scoring

**Example:**
```
Headline: "Scientists Confirm Cats Are Now Eligible for Tax Returns"
Keywords: ["Scientists", "Cats", "Eligible", "Tax", "Returns"]

Article 1: "New Cat Breed Discovered" 
- Matches: 1/5 (only "Cats")
- Relevance: 20%
- Result: FILTERED OUT ✗

Article 2: "IRS Announces New Tax Rules for Pet Owners"
- Matches: 3/5 ("Tax", "Returns", related to pets)
- Relevance: 60%
- Result: INCLUDED ✓
```

### Layer 3: No Relevant Sources Detection
If search returns articles but none are relevant:
- Score: 5/100
- Verdict: "Unverifiable - No Relevant Sources"
- Message: "No credible sources found covering this specific topic"

## Implementation Details

### New Methods in `DeepAnalysisAgent`

#### 1. `_detect_absurd_claims(headline)`
```python
# Uses AI to detect absurd/impossible claims
# Returns: {"is_absurd": bool, "reason": str}
```

#### 2. `_calculate_relevance_score(headline, article_title, article_description)`
```python
# Calculates 0-1 relevance score
# Compares headline keywords with article content
# Returns: float (0.0 to 1.0)
```

#### 3. `_filter_relevant_articles(headline, articles, min_relevance=0.3)`
```python
# Filters articles by relevance threshold
# Default: 30% minimum relevance
# Returns: List of relevant articles only
```

## Test Cases

### Test Case 1: Obviously Fake
**Input:** "Scientists Confirm Cats Are Now Eligible for Tax Returns"

**Expected Output:**
```json
{
  "verification_score": 5,
  "verdict": "Likely Fake/Satirical",
  "source_analysis": {
    "score": 5,
    "reason": "Headline contains absurd or impossible claims",
    "source_count": 0
  },
  "absurdity_detected": true
}
```

### Test Case 2: Real News with Many Sources
**Input:** "NASA Announces New Mars Mission"

**Expected Output:**
```json
{
  "verification_score": 85,
  "verdict": "Highly Credible - Multiple Reliable Sources",
  "source_analysis": {
    "score": 85,
    "source_count": 10,
    "high_quality_sources": 4
  }
}
```

### Test Case 3: Misleading Headline
**Input:** "Doctors Hate This One Weird Trick"

**Expected Output:**
```json
{
  "verification_score": 5,
  "verdict": "Unverifiable - No Relevant Sources",
  "source_analysis": {
    "score": 5,
    "reason": "Found 8 articles but none match the headline topic",
    "source_count": 0
  }
}
```

### Test Case 4: Niche but Real News
**Input:** "Local School Wins State Championship"

**Expected Output:**
```json
{
  "verification_score": 15,
  "verdict": "Low Credibility - Few Sources",
  "source_analysis": {
    "score": 15,
    "source_count": 2,
    "high_quality_sources": 0
  }
}
```

## Scoring Logic Flow

```
1. Check for Absurdity (AI)
   ├─ If absurd → Score: 5/100, Stop
   └─ If not absurd → Continue

2. Search for News Articles
   └─ Found articles → Continue

3. Filter by Relevance (30% threshold)
   ├─ No relevant articles → Score: 5/100, Stop
   └─ Has relevant articles → Continue

4. Calculate Score Based on:
   ├─ Number of relevant sources (5-40%)
   └─ Quality of sources (+15 or +8 per source)

5. Return Final Score (5-100)
```

## Benefits

### Before
- "Cats Tax Returns" → 55/100 (10 unrelated cat articles)
- No fake news detection
- Keyword-only matching
- Misleading scores

### After
- "Cats Tax Returns" → 5/100 (absurdity detected)
- AI-powered fake news detection
- Relevance-based filtering
- Accurate, trustworthy scores

## Configuration

### Relevance Threshold
Default: 30% (adjustable in code)
- Lower threshold: More lenient, includes loosely related articles
- Higher threshold: Stricter, only highly relevant articles

### Absurdity Detection
Powered by: Gemini 2.5 Pro
- Requires: GEMINI_API_KEY in config
- Fallback: If AI unavailable, skips absurdity check

## Future Enhancements

1. **Fact-Checking APIs**: Integrate with Snopes, FactCheck.org
2. **Historical Patterns**: Track sources that frequently publish fake news
3. **Social Media Signals**: Check if story is viral on social media
4. **Image Verification**: Reverse image search for manipulated photos
5. **Domain Reputation**: Maintain blacklist of known fake news sites
6. **User Reports**: Allow users to flag fake news
7. **Satire Detection**: Better detection of satirical sources (The Onion, Babylon Bee)

## Error Handling

- If AI fails: Falls back to relevance filtering only
- If search fails: Returns error message
- If no articles found: Score 5/100 with clear message
- Logs all filtering decisions for debugging

## Performance

- Absurdity check: ~1-2 seconds (AI call)
- Relevance filtering: <100ms (local computation)
- Total overhead: ~1-2 seconds per verification
- Caching recommended for repeated queries
