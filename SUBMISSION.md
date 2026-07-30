# Kaggle submission draft

## Title

VerseBridge Studio — Scripture that meets you in the moment

## Elevator pitch

VerseBridge Studio turns live workout biometrics into timely, source-grounded
Scripture encouragement. VersePulse detects meaningful moments such as peak
effort, hitting the wall, a final rep, finishing strong, and recovery. It then
selects a compatible entry from the official verse-movement mapping and
delivers it through the appropriate wearable channel. The same application
also helps creators turn licensed Scripture into audience-ready content while
preserving a bright line between biblical text and AI commentary.

## The problem

Most fitness apps can tell people what their bodies are doing, but not meet
their spiritual needs at the instant encouragement matters. Meanwhile, generic
AI tools can misquote passages, lose attribution, or make generated
interpretation look like Scripture.

## The solution

1. Read heart rate, HR zone, effort, recovery, stress, activity and elapsed time.
2. Detect the current workout moment and rank the official mappings by activity
   compatibility and trigger proximity.
3. Retrieve licensed text and attribution from the YouVersion Platform.
4. Send a narrowly scoped, source-grounded prompt to Gloo AI.
5. Keep verified Scripture and generated commentary visually distinct.
6. Preserve the reference and source link in every output.
7. Add a human-review note rather than presenting generated reflection as
   biblical text.

## Built with

- YouVersion Platform REST API
- Gloo AI Completions V2
- Official Scripture-in-New-Frontiers biometric and verse-movement mapping data
- Python standard library
- Accessible responsive HTML and CSS

## Links

- Source: https://github.com/ILoveBuns/versebridge-studio
- Narrated demo:
  https://github.com/ILoveBuns/versebridge-studio/raw/main/artifacts/versebridge-demo.mp4

## Potential frontiers

The same content pack can drive an Instagram carousel, podcast opening,
newsletter reflection, wearable daily prompt, or an ambient display. The
interface deliberately focuses on a reusable content object rather than a
single channel.

## Current limitations

- A creator should review tone and denominational context before publishing.
- Demo mode uses a clearly labelled excerpt until live API credentials are
  configured.
- VerseBridge does not generate or alter Scripture text.
