import React, { useMemo, useRef, useEffect, useState } from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { CaptionStyleProps } from "./types";
import { RemotionCaption } from "../convert-whisper";

/**
 * AnimatedBackground Style (CapCut Signature Style)
 *
 * Shows a short phrase at the bottom with the active word highlighted.
 * Words stay in one fixed position - only the highlight moves.
 */
export const AnimatedBackground: React.FC<CaptionStyleProps> = ({
  captions,
  currentFrame,
  fps,
  accentColor,
  fontFamily,
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const wordRefs = useRef<Map<number, HTMLSpanElement>>(new Map());
  const [wordPositions, setWordPositions] = useState<Map<number, DOMRect>>(new Map());

  const currentTimeMs = (currentFrame / fps) * 1000;

  // Find the currently active word index in the full captions array
  const activeWordIndex = useMemo(() => {
    return captions.findIndex(
      (cap) => currentTimeMs >= cap.startMs && currentTimeMs < cap.endMs
    );
  }, [captions, currentTimeMs]);

  // Get a window of words to display (current word + context)
  const visibleWords = useMemo(() => {
    if (activeWordIndex < 0) {
      // Show first few words if nothing active yet
      return captions.slice(0, 4).map((cap, i) => ({
        word: cap.text,
        index: i,
        isActive: false,
      }));
    }

    // Show 3-5 words centered around the active word
    const windowSize = 4;
    const halfWindow = Math.floor(windowSize / 2);
    const start = Math.max(0, activeWordIndex - halfWindow);
    const end = Math.min(captions.length, start + windowSize);
    const actualStart = Math.max(0, end - windowSize);

    return captions.slice(actualStart, end).map((cap, i) => ({
      word: cap.text,
      index: actualStart + i,
      isActive: actualStart + i === activeWordIndex,
    }));
  }, [captions, activeWordIndex]);

  // Update word positions for highlight box
  useEffect(() => {
    const positions = new Map<number, DOMRect>();
    wordRefs.current.forEach((element, index) => {
      if (element) {
        positions.set(index, element.getBoundingClientRect());
      }
    });
    setWordPositions(positions);
  }, [visibleWords, currentFrame]);

  if (visibleWords.length === 0) return null;

  const containerRect = containerRef.current?.getBoundingClientRect();
  const activeVisibleIndex = visibleWords.findIndex((w) => w.isActive);
  const activeWordRect = wordPositions.get(activeVisibleIndex);

  return (
    <div
      ref={containerRef}
      style={{
        position: "relative",
        display: "flex",
        flexDirection: "row",
        justifyContent: "center",
        alignItems: "center",
        gap: "8px",
        padding: "12px 24px",
        backgroundColor: "rgba(0, 0, 0, 0.6)",
        borderRadius: "8px",
      }}
    >
      {/* Animated highlight box */}
      {activeVisibleIndex >= 0 && activeWordRect && containerRect && (
        <div
          style={{
            position: "absolute",
            left: activeWordRect.left - containerRect.left - 6,
            top: activeWordRect.top - containerRect.top - 4,
            width: activeWordRect.width + 12,
            height: activeWordRect.height + 8,
            backgroundColor: accentColor,
            borderRadius: "6px",
            transition: "all 0.1s ease-out",
            zIndex: 0,
          }}
        />
      )}

      {/* Words in a single row */}
      {visibleWords.map((item, index) => (
        <span
          key={`${item.word}-${item.index}`}
          ref={(el) => {
            if (el) wordRefs.current.set(index, el);
          }}
          style={{
            fontFamily,
            fontSize: "32px",
            fontWeight: 700,
            color: item.isActive ? "#000000" : "#FFFFFF",
            position: "relative",
            zIndex: item.isActive ? 2 : 1,
            textTransform: "uppercase",
            letterSpacing: "0.02em",
            whiteSpace: "nowrap",
          }}
        >
          {item.word}
        </span>
      ))}
    </div>
  );
};
