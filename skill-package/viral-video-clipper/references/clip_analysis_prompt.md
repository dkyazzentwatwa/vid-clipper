# AI Video Clip Analysis Task

## Objective
Analyze the provided YouTube video transcript and identify 3-7 viral-worthy moments suitable for Instagram Reels and TikTok (9:16 vertical format).

## Video Metadata
{metadata}

## Video Transcript (with timestamps)
{transcript}

## Selection Criteria

Identify clips that have HIGH viral potential based on:

1. **Strong Hooks** (0-3 seconds)
   - Bold claims or surprising statements
   - Visual demonstrations that grab attention
   - Questions that create curiosity

2. **Value Bombs** (quick insights)
   - Actionable tips or techniques
   - "Aha!" moments or revelations
   - Problem-solution demonstrations

3. **Emotional Peaks**
   - Excitement, surprise, or humor
   - Relatable frustrations solved
   - Impressive demonstrations

4. **Story Arcs** (complete narratives)
   - Setup → Demonstration → Payoff
   - Before → After transformations
   - Challenge → Solution sequences

## Constraints

- **Duration**: 15-60 seconds per clip (optimal: 20-45 seconds)
- **Self-contained**: Each clip must make sense on its own
- **No mid-sentence cuts**: Start and end at natural speech boundaries
- **Audience**: Tech enthusiasts, developers, and early adopters on social media
- **Platform**: Instagram Reels and TikTok (9:16 vertical, mobile-first)

## Output Format

Return ONLY valid JSON in this exact format (no markdown code blocks, no additional text):

```json
{
  "clips": [
    {
      "clip_number": 1,
      "start_time": 5.2,
      "end_time": 32.8,
      "duration": 27.6,
      "title": "Hook: AI Creates Apple Shortcuts",
      "description": "Opens with bold claim and immediate demonstration of AI creating shortcuts",
      "virality_score": 9,
      "virality_factors": ["strong_hook", "visual_demo", "trending_topic"],
      "suggested_caption": "🤯 I made AI create Apple Shortcuts from scratch!",
      "content_type": "hook",
      "target_audience": "iOS users, automation enthusiasts",
      "key_moments": ["0:05 - Bold claim", "0:15 - First demo", "0:28 - Payoff"]
    }
  ],
  "video_summary": "Brief 1-2 sentence summary of the full video content and main topic",
  "overall_theme": "Main theme or category (e.g., 'AI Automation', 'Tech Tutorial', 'Product Demo')",
  "target_audience": "Primary audience for these clips",
  "hashtag_suggestions": ["#apple", "#AI", "#automation", "#shortcuts", "#tech"]
}
```

## Field Definitions

- **clip_number**: Sequential number (1, 2, 3...)
- **start_time**: Start timestamp in seconds (decimal allowed, e.g., 5.2)
- **end_time**: End timestamp in seconds
- **duration**: Calculated duration (end_time - start_time)
- **title**: Short, punchy title (max 60 characters)
- **description**: 1-2 sentence description of what happens in the clip
- **virality_score**: 1-10 rating (8+ recommended for clips worth creating)
- **virality_factors**: Array of factors from: ["strong_hook", "visual_demo", "trending_topic", "emotional_peak", "value_bomb", "surprise_factor", "relatable_problem", "quick_win", "story_arc"]
- **suggested_caption**: Ready-to-use Instagram/TikTok caption with emojis
- **content_type**: One of: "hook", "demo", "tutorial", "value_bomb", "story", "payoff"
- **target_audience**: Specific audience segment for this clip
- **key_moments**: Array of 2-4 specific timestamps with brief descriptions

## Examples of High-Performing Clips

### Example 1: Tech Demo Hook
- **Duration**: 28 seconds
- **Structure**: Bold claim (3s) → Visual proof (20s) → Call-to-action (5s)
- **Why it works**: Immediate demonstration, trending topic, shareable moment

### Example 2: Problem-Solution Value Bomb
- **Duration**: 35 seconds
- **Structure**: Relatable problem (8s) → Solution demo (22s) → Results (5s)
- **Why it works**: Addresses pain point, shows clear before/after, actionable

### Example 3: Story Arc
- **Duration**: 45 seconds
- **Structure**: Setup/challenge (10s) → Process (25s) → Payoff/result (10s)
- **Why it works**: Complete narrative, emotional journey, satisfying conclusion

## Quality Guidelines

- Prioritize clips with **visual** demonstrations over talking heads
- Favor clips where the speaker's energy/enthusiasm is high
- Avoid clips that require prior context from earlier in the video
- Each clip should have a clear "hook" in the first 3 seconds
- Ensure clips end on a strong note (payoff, punchline, or call-to-action)

## Important Notes

1. Return ONLY the JSON object - no markdown formatting, no code blocks, no explanatory text
2. Validate all timestamps are within the video duration
3. Ensure no clips overlap in time
4. Order clips chronologically by start_time
5. Only recommend clips with virality_score >= 7
6. Aim for 3-7 clips total (quality over quantity)

Now analyze the transcript above and generate your recommendations.
