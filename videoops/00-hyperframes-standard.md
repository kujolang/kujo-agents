# VideoOps HyperFrames Standard

The editor must preflight the installed HyperFrames interface and record its version. The verified local reference for this package is HyperFrames `0.8.27`, invoked with `npx hyperframes`.

Use frame-accurate composition timing, explicit resolution/FPS/duration, supported image/video/GIF/audio media, deterministic animations, and effects only when justified. Build from the approved shot list and manifest under `production/hyperframes/`.

Run `hyperframes lint`, `check`, and `render`; use `inspect`, `snapshot`, or `keyframes` when needed. Use FFmpeg/ffprobe for output integrity, dimensions, FPS, duration, streams, loudness, and corruption checks. Never hide unresolved production assets behind placeholders in a declared final render.

When a fix list exists, report every item as `APPLIED`, `PARTIAL`, `REJECTED`, or `BLOCKED`. Material timing or substitution changes belong in production notes.
