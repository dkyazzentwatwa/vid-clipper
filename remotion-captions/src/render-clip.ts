#!/usr/bin/env npx ts-node
/**
 * CLI script to render a captioned clip.
 *
 * Usage:
 *   npx ts-node src/render-clip.ts \
 *     --video /path/to/clip.mp4 \
 *     --whisper /path/to/original.json \
 *     --output /path/to/output.mp4 \
 *     --start 10.5 \
 *     --end 40.2 \
 *     --style background \
 *     --color "#FFFF00"
 */

import { bundle } from "@remotion/bundler";
import { renderMedia, selectComposition } from "@remotion/renderer";
import { convertWhisperToRemotionCaptions, WhisperTranscript } from "./convert-whisper";
import * as fs from "fs";
import * as path from "path";

interface RenderOptions {
  videoPath: string;
  whisperPath: string;
  outputPath: string;
  startTime: number;
  endTime: number;
  style: "colored" | "scaling" | "background";
  accentColor: string;
  fontFamily: string;
}

function parseArgs(): RenderOptions {
  const args = process.argv.slice(2);
  const options: Partial<RenderOptions> = {
    style: "background",
    accentColor: "#FFFF00",
    fontFamily: "Inter, system-ui, sans-serif",
  };

  for (let i = 0; i < args.length; i += 2) {
    const key = args[i];
    const value = args[i + 1];

    switch (key) {
      case "--video":
        options.videoPath = value;
        break;
      case "--whisper":
        options.whisperPath = value;
        break;
      case "--output":
        options.outputPath = value;
        break;
      case "--start":
        options.startTime = parseFloat(value);
        break;
      case "--end":
        options.endTime = parseFloat(value);
        break;
      case "--style":
        options.style = value as RenderOptions["style"];
        break;
      case "--color":
        options.accentColor = value;
        break;
      case "--font":
        options.fontFamily = value;
        break;
    }
  }

  if (!options.videoPath || !options.whisperPath || !options.outputPath) {
    console.error("Required: --video, --whisper, --output");
    process.exit(1);
  }

  if (options.startTime === undefined || options.endTime === undefined) {
    console.error("Required: --start, --end");
    process.exit(1);
  }

  return options as RenderOptions;
}

async function main() {
  const options = parseArgs();

  console.log("Loading Whisper transcript...");
  const whisperJson: WhisperTranscript = JSON.parse(
    fs.readFileSync(options.whisperPath, "utf-8")
  );

  console.log("Converting captions for clip range...");
  const captions = convertWhisperToRemotionCaptions(
    whisperJson,
    options.startTime,
    options.endTime
  );

  console.log(`Found ${captions.length} caption words for clip`);

  const fps = 30;
  const durationInFrames = Math.ceil((options.endTime - options.startTime) * fps);

  console.log("Bundling Remotion project...");
  const bundleLocation = await bundle({
    entryPoint: path.join(__dirname, "index.ts"),
    onProgress: (progress) => {
      if (progress % 20 === 0) {
        console.log(`Bundle progress: ${progress}%`);
      }
    },
  });

  console.log("Selecting composition...");
  const composition = await selectComposition({
    serveUrl: bundleLocation,
    id: "CaptionedClip",
    inputProps: {
      videoSrc: options.videoPath,
      captions,
      style: options.style,
      accentColor: options.accentColor,
      fontFamily: options.fontFamily,
      durationInFrames,
    },
  });

  console.log("Rendering video with captions...");
  await renderMedia({
    composition: {
      ...composition,
      durationInFrames,
    },
    serveUrl: bundleLocation,
    codec: "h264",
    outputLocation: options.outputPath,
    inputProps: {
      videoSrc: options.videoPath,
      captions,
      style: options.style,
      accentColor: options.accentColor,
      fontFamily: options.fontFamily,
      durationInFrames,
    },
    onProgress: ({ progress }) => {
      const percent = Math.round(progress * 100);
      if (percent % 10 === 0) {
        process.stdout.write(`\rRendering: ${percent}%`);
      }
    },
  });

  console.log(`\nDone! Output saved to: ${options.outputPath}`);
}

main().catch((err) => {
  console.error("Render failed:", err);
  process.exit(1);
});
