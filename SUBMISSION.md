# Kaggle submission draft

## Title

VerseBridge Studio — source-grounded Scripture packs for creators

## Elevator pitch

VerseBridge Studio helps creators turn licensed Scripture into audience-ready
content while preserving a bright line between biblical text and AI-generated
commentary. It retrieves the requested passage from YouVersion, sends only that
grounded source and the creator brief to Gloo AI, and returns a compact pack:
headline, caption, reflection prompt, visual direction, and review note.

## The problem

Creators increasingly use AI to draft spiritual content, but generic models can
misquote passages, lose attribution, or make generated interpretation look like
Scripture. The resulting experience is fast but hard to trust.

## The solution

1. Retrieve licensed text and attribution from the YouVersion Platform.
2. Send a narrowly scoped, source-grounded prompt to Gloo AI.
3. Keep verified Scripture and generated commentary visually distinct.
4. Preserve the reference and source link in every output.
5. Add a human-review note rather than presenting generated reflection as
   biblical text.

## Built with

- YouVersion Platform REST API
- Gloo AI Completions V2
- Python standard library
- Accessible responsive HTML and CSS

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
