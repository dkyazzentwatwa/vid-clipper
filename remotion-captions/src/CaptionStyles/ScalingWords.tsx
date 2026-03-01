import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { CaptionStyleProps, getActiveWords } from "./types";

/**
 * ScalingWords Style
 *
 * Punchy, dynamic captions where each word scales up with a spring
 * animation when it becomes active. Great for energetic content.
 */
export const ScalingWords: React.FC<CaptionStyleProps> = ({
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

        // Spring animation for scale
        const scaleProgress = spring({
          frame: currentFrame - word.startFrame,
          fps,
          config: {
            damping: 12,
            stiffness: 200,
            mass: 0.5,
          },
        });

        // Scale up when active, return to normal after
        const scale = isActive
          ? interpolate(scaleProgress, [0, 1], [1, 1.2])
          : interpolate(
              currentFrame,
              [word.endFrame, word.endFrame + 5],
              [1.2, 1],
              { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
            );

        // Opacity based on timing
        const opacity = interpolate(
          currentFrame,
          [word.startFrame - 5, word.startFrame, word.endFrame + 10, word.endFrame + 15],
          [0.5, 1, 1, 0.5],
          { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
        );

        return (
          <span
            key={`${word.word}-${index}`}
            style={{
              fontFamily,
              fontSize: "36px",
              fontWeight: 700,
              color: "#FFFFFF",
              textShadow: isActive
                ? `0 0 16px ${accentColor}, 0 0 32px ${accentColor}80, 1px 1px 3px rgba(0,0,0,0.9)`
                : "1px 1px 3px rgba(0,0,0,0.9)",
              transform: `scale(${scale})`,
              opacity,
              display: "inline-block",
              textTransform: "uppercase",
              letterSpacing: "0.01em",
              WebkitTextStroke: isActive ? `1px ${accentColor}` : "none",
            }}
          >
            {word.word}
          </span>
        );
      })}
    </div>
  );
};
