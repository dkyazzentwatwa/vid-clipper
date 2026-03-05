import React from "react";
import { Composition, staticFile } from "remotion";
import { CaptionedClip } from "./CaptionedClip";
import type { RemotionCaption } from "./convert-whisper";
import type { CaptionStyle } from "./CaptionStyles";

// Schema for input props - matches CaptionedClipProps
const defaultCaptions: RemotionCaption[] = [];

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="CaptionedClip"
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        component={CaptionedClip as any}
        durationInFrames={30 * 30}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          videoSrc: staticFile("sample.mp4"),
          captions: defaultCaptions,
          style: "background" as CaptionStyle,
          accentColor: "#FFFF00",
          fontFamily: "Inter, system-ui, sans-serif",
          durationInFrames: 30 * 30,
        }}
        calculateMetadata={async ({ props }) => {
          return {
            durationInFrames:
              (props as { durationInFrames?: number }).durationInFrames ??
              30 * 30,
          };
        }}
      />
    </>
  );
};
