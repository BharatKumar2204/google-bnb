# Dynamic Verification Scoring System

## Overview

Implemented a dynamic verification scoring system based on the number of credible sources found, replacing the static 75/100 score.

## Scoring Formula

### Base Score (Based on Number of Sources)

The base score increases with the number of sources found:

| Sources | Base Score | Percentage |
| ------- | ---------- | ---------- |
| 0       | 5          | 5%         |
| 1       | 5          | 5%         |
| 2       | 10         | 10%        |
| 3       | 15         | 15%        |
| 4       | 20         | 20%        |
| 5       | 25         | 25%        |
| 6       | 30         | 30%        |
| 7       | 33         | 33%        |
| 8       | 36         | 36%        |
| 9       | 38         | 38%        |
| 10+     | 40         | 40%        |

### Quality Bonus

Additional points are awarded based on source reliability:

- **High-Reliability Sources** (+15 points each):

  - Reuters
  - AP News
  - BBC
  - Associated Press
  - NPR
  - The Guardian
  - The New York Times
  - Washington Post

- **Medium-Reliability Sources** (+8 points each):
  - CNN
  - Fox News
  - MSNBC
  - ABC News
  - CBS News
  - NBC News
  - USA Today
  - Bloomberg

### Total Score Calculation

```
Total Score = Base Score + Quality Bonus (max 100)
```

### Example Calculations

#### Example 1: Single Unknown Source

- Sources: 1
- High-reliability: 0
- Medium-reliability: 0
- **Score: 5/100** (5% base + 0 bonus)

#### Example 2: Three Medium Sources

- Sources: 3
- High-reliability: 0
- Medium-reliability: 3
- **Score: 39/100** (15% base + 24 bonus)

#### Example 3: Ten Sources with Mix

- Sources: 10
- High-reliability: 3
- Medium-reliability: 2
- **Score: 101 → 100/100** (40% base + 45 + 16 bonus, capped at 100)

## Implementation

### Backend Changes

#### 1. Deep Analysis Agent (`deep_analysis_agent.py`)

Updated `_calculate_source_score()` method:

- Progressive base scoring from 5% to 40%
- Enhanced quality bonus system
- More granular score distribution

#### 2. API Endpoint

- `/agents/deep_analysis` returns dynamic scores
- Includes source breakdown in response

### Frontend Changes

#### 1. API Service (`api.js`)

Updated `verifyNews()` function:

- Now uses deep analysis endpoint
- Returns score, verdict, source count, and details
- Provides comprehensive verification data

#### 2. Trending News Component (`TrendingNews.jsx`)

Enhanced verification display:

- Shows dynamic scores instead of static 75/100
- Displays loading state during verification
- Color-coded scores (green ≥70, yellow ≥40, red <40)
- Stores verification scores per article
- Shows detailed breakdown in alert

#### 3. Visual Improvements

- Verification button shows score after verification
- Loading spinner during verification
- Color-coded score display
- Disabled state during loading

## Score Interpretation

### Score Ranges

- **80-100**: Highly Credible - Multiple Reliable Sources
- **60-79**: Credible - Multiple Sources Found
- **40-59**: Moderately Credible - Limited Sources
- **20-39**: Low Credibility - Few Sources
- **0-19**: Unverifiable - Insufficient Sources

## User Experience

### Before

- All trending news showed static 75/100 score
- No indication of actual source verification
- No transparency in scoring

### After

- Dynamic scores based on actual sources found
- Real-time verification with loading states
- Detailed breakdown of sources
- Color-coded visual feedback
- Transparent scoring methodology

## Benefits

1. **Accuracy**: Scores reflect actual source availability
2. **Transparency**: Users see exactly how many sources were found
3. **Trust**: Clear methodology builds user confidence
4. **Actionable**: Low scores indicate need for caution
5. **Educational**: Users learn to evaluate news critically

## Testing Examples

### Test Case 1: Major News Event

**Input**: "NASA announces Mars discovery"
**Expected**:

- 10+ sources found
- Multiple high-reliability sources
- Score: 85-95/100

### Test Case 2: Niche Topic

**Input**: "Local community event in small town"
**Expected**:

- 1-2 sources found
- No high-reliability sources
- Score: 5-15/100

### Test Case 3: Fake News

**Input**: "Aliens land in New York City"
**Expected**:

- 0 sources found
- Score: 5/100
- Verdict: "No Sources Found"

## Future Enhancements

1. **Source Age**: Factor in how recent the sources are
2. **Geographic Diversity**: Bonus for sources from different regions
3. **Cross-referencing**: Check if sources cite each other
4. **Historical Accuracy**: Track source reliability over time
5. **User Feedback**: Allow users to report inaccurate scores
6. **Caching**: Store verification results to reduce API calls
