/**
 * Converts vid-clipper Whisper JSON format to Remotion Caption objects.
 * Supports both segment-level and word-level timestamps.
 */

export interface WhisperWord {
  word: string;
  start: number;
  end: number;
  probability?: number;
}

export interface WhisperSegment {
  id: number;
  seek: number;
  start: number;
  end: number;
  text: string;
  tokens: number[];
  temperature: number;
  avg_logprob: number;
  compression_ratio: number;
  no_speech_prob: number;
  words?: WhisperWord[];
}

export interface WhisperTranscript {
  text: string;
  segments: WhisperSegment[];
  language: string;
}

export interface RemotionCaption {
  text: string;
  startMs: number;
  endMs: number;
  timestampMs: number;
  confidence: number | null;
}

/**
 * Convert Whisper JSON transcript to Remotion Caption array.
 * Uses word-level timestamps when available for precise caption timing.
 */
export function convertWhisperToRemotionCaptions(
  whisperJson: WhisperTranscript,
  clipStartTime?: number,
  clipEndTime?: number
): RemotionCaption[] {
  const captions: RemotionCaption[] = [];
  const offsetMs = (clipStartTime || 0) * 1000;

  for (const segment of whisperJson.segments) {
    // Skip segments outside clip range if specified
    if (clipStartTime !== undefined && segment.end < clipStartTime) continue;
    if (clipEndTime !== undefined && segment.start > clipEndTime) continue;

    // Use word-level timestamps if available
    if (segment.words && segment.words.length > 0) {
      for (const word of segment.words) {
        // Skip words outside clip range
        if (clipStartTime !== undefined && word.end < clipStartTime) continue;
        if (clipEndTime !== undefined && word.start > clipEndTime) continue;

        const startMs = Math.max(0, word.start * 1000 - offsetMs);
        const endMs = word.end * 1000 - offsetMs;

        // Clamp to clip duration if specified
        if (clipEndTime !== undefined) {
          const clipDurationMs = (clipEndTime - (clipStartTime || 0)) * 1000;
          if (startMs >= clipDurationMs) continue;
        }

        captions.push({
          text: word.word.trim(),
          startMs,
          endMs,
          timestampMs: startMs,
          confidence: word.probability ?? null,
        });
      }
    } else {
      // Fall back to segment-level timestamps
      // Split segment text into words and distribute time evenly
      const words = segment.text.trim().split(/\s+/);
      const segmentDuration = (segment.end - segment.start) * 1000;
      const wordDuration = segmentDuration / words.length;

      for (let i = 0; i < words.length; i++) {
        const wordStart = segment.start * 1000 + i * wordDuration - offsetMs;
        const wordEnd = wordStart + wordDuration;

        if (wordStart < 0) continue;

        captions.push({
          text: words[i],
          startMs: Math.max(0, wordStart),
          endMs: wordEnd,
          timestampMs: Math.max(0, wordStart),
          confidence: null,
        });
      }
    }
  }

  return captions;
}

/**
 * Extract captions for a specific clip timerange from the full transcript.
 */
export function extractClipCaptions(
  whisperJson: WhisperTranscript,
  startTime: number,
  endTime: number
): RemotionCaption[] {
  return convertWhisperToRemotionCaptions(whisperJson, startTime, endTime);
}

/**
 * Read and parse Whisper JSON file.
 */
export async function loadWhisperTranscript(
  jsonPath: string
): Promise<WhisperTranscript> {
  const response = await fetch(jsonPath);
  if (!response.ok) {
    throw new Error(`Failed to load Whisper transcript: ${jsonPath}`);
  }
  return response.json();
}
