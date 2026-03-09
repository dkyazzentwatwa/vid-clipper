import React from "react";
import { interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { CaptionStyleProps, getActiveWords } from "./types";

/**
 * ColoredWords Style
 *
 * Clean, readable captions where the active word is highlighted
 * in an accent color. Simple and professional.
 */
export const ColoredWords: React.FC<CaptionStyleProps> = ({
  captions,
  currentFrame,
  fps,
  accentColor,
  fontFamily,
}) => {
  const words = getActiveWords(captions, currentFrame, fps);

  if (words.length === 0) return null;

  return (
    <div
      style={{
        display: "flex",
        flexWrap: "wrap",
        justifyContent: "center",
        alignItems: "center",
        gap: "6px 10px",
        padding: "16px 40px",
        maxWidth: "85%",
      }}
    >
      {words.map((word, index) => {
        const isActive = word.isActive;

        // Smooth opacity transition
        const progress = interpolate(
          currentFrame,
          [word.startFrame - 3, word.startFrame, word.endFrame, word.endFrame + 3],
          [0.6, 1, 1, 0.6],
          { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
        );

        return (
          <span
            key={`${word.word}-${index}`}
            style={{
              fontFamily,
              fontSize: "36px",
              fontWeight: 700,
              color: isActive ? accentColor : "#FFFFFF",
              textShadow: isActive
                ? `0 0 12px ${accentColor}80, 1px 1px 3px rgba(0,0,0,0.9)`
                : "1px 1px 3px rgba(0,0,0,0.9)",
              opacity: progress,
              transition: "color 0.1s ease-out",
              textTransform: "uppercase",
              letterSpacing: "0.01em",
            }}
          >
            {word.word}
          </span>
        );
      })}
    </div>
  );
};
