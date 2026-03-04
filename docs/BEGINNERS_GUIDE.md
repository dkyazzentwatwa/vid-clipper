# How to Turn Any Video Into Viral Shorts (Using Claude Code)

literally just drop a youtube link or video file into claude and get instagram-ready clips in minutes

---

## what you need

- claude code (the desktop app)
- this skill file: `universal-video-clipper.skill`

that's it. claude handles the rest.

---

## setup (2 minutes)

**step 1:** download the skill file from the github repo

**step 2:** open claude code, paste this:
```
install this skill: universal-video-clipper.skill
```

claude will load it up. done.

---

## how to use it

just paste a link or file path and ask for clips:

> "make viral clips from this: https://youtube.com/watch?v=..."

> "turn this into reels: ~/downloads/my-video.mp4"

> "extract highlights from this tutorial for tiktok: [url]"

that's literally it. claude will:
- download the video
- transcribe it
- find the best moments
- cut 3-7 clips (15-60 seconds each)
- make instagram 9:16 versions
- write captions and hashtags for you

---

## pro tip: animated captions

want that capcut-style word-by-word caption effect? just say:

> "make clips with animated captions from: [url]"

you'll get clips with text that bounces along with the audio.

---

## what you get

claude creates a folder with everything:

```
downloads/video-id/
├── clips/
│   ├── clip_001_hook.mp4           # original format
│   ├── clip_001_hook_instagram.mp4 # 9:16 vertical
│   └── clip_001_hook_captioned.mp4 # with animated text
└── SUMMARY.md                       # captions & hashtags ready to copy
```

open `SUMMARY.md` - it has suggested captions with emojis, hashtags, and virality scores for each clip. just copy and post.

---

## the one thing to know

at one point claude will pause and say "press enter to continue"

this is normal. claude is analyzing the transcript to pick the best clips. just hit enter and let it cook.

---

## example workflow

**you:** "create viral clips from this: https://youtu.be/dQw4w9WgXcQ"

**claude:** *downloads, transcribes, analyzes, cuts clips*

**claude:** "done! created 5 clips in downloads/dQw4w9WgXcQ/clips/"

**you:** copy captions from SUMMARY.md → paste into instagram → post

---

try it on any video. works with youtube links or files on your computer.
