import { RemotionCaption } from "../convert-whisper";

export type CaptionStyle = "colored" | "scaling" | "background";

export interface CaptionStyleProps {
  captions: RemotionCaption[];
  currentFrame: number;
  fps: number;
  accentColor: string;
  fontFamily: string;
}

export interface WordTiming {
  word: string;
  startFrame: number;
  endFrame: number;
  isActive: boolean;
}

/**
 * Get words visible at the current frame with their timing info.
 * Groups words into "pages" - sentences or groups that appear together.
 */
export function getActiveWords(
  captions: RemotionCaption[],
  currentFrame: number,
  fps: number,
  windowMs: number = 3000 // Show 3 seconds of context
): WordTiming[] {
  const currentTimeMs = (currentFrame / fps) * 1000;
  const windowStart = currentTimeMs - windowMs / 2;
  const windowEnd = currentTimeMs + windowMs / 2;

  return captions
    .filter((cap) => cap.startMs <= windowEnd && cap.endMs >= windowStart)
    .map((cap) => ({
      word: cap.text,
      startFrame: Math.round((cap.startMs / 1000) * fps),
      endFrame: Math.round((cap.endMs / 1000) * fps),
      isActive: currentTimeMs >= cap.startMs && currentTimeMs < cap.endMs,
    }));
}

/**
 * Find the currently active word index.
 */
export function getActiveWordIndex(
  captions: RemotionCaption[],
  currentFrame: number,
  fps: number
): number {
  const currentTimeMs = (currentFrame / fps) * 1000;
  return captions.findIndex(
    (cap) => currentTimeMs >= cap.startMs && currentTimeMs < cap.endMs
  );
}
