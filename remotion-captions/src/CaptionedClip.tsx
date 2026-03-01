import React from "react";
import {
  AbsoluteFill,
  OffthreadVideo,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { RemotionCaption } from "./convert-whisper";
import {
  ColoredWords,
  ScalingWords,
  AnimatedBackground,
  CaptionStyle,
} from "./CaptionStyles";

export interface CaptionedClipProps {
  videoSrc: string;
  captions: RemotionCaption[];
  style: CaptionStyle;
  accentColor: string;
  fontFamily: string;
  durationInFrames: number;
}

const CaptionRenderer: React.FC<{
  style: CaptionStyle;
  captions: RemotionCaption[];
  currentFrame: number;
  fps: number;
  accentColor: string;
  fontFamily: string;
}> = ({ style, ...props }) => {
  switch (style) {
    case "colored":
      return <ColoredWords {...props} />;
    case "scaling":
      return <ScalingWords {...props} />;
    case "background":
    default:
      return <AnimatedBackground {...props} />;
  }
};

export const CaptionedClip: React.FC<CaptionedClipProps> = ({
  videoSrc,
  captions,
  style,
  accentColor,
  fontFamily,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Use staticFile for videos in the public folder
  const resolvedVideoSrc = videoSrc.startsWith("/") || videoSrc.startsWith("http")
    ? videoSrc
    : staticFile(videoSrc);

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#000000",
      }}
    >
      {/* Video layer */}
      <AbsoluteFill>
        <OffthreadVideo
          src={resolvedVideoSrc}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "contain",
          }}
        />
      </AbsoluteFill>

      {/* Caption overlay layer - positioned at bottom of video content (not black bars) */}
      {/* For 16:9 video in 9:16 frame: video is ~608px tall, centered, so bottom of video is ~656px from frame bottom */}
      <div
        style={{
          position: "absolute",
          bottom: 700,
          left: 0,
          right: 0,
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        <CaptionRenderer
          style={style}
          captions={captions}
          currentFrame={frame}
          fps={fps}
          accentColor={accentColor}
          fontFamily={fontFamily}
        />
      </div>
    </AbsoluteFill>
  );
};
