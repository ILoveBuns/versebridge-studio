# VerseBridge Studio

[![tests](https://github.com/ILoveBuns/versebridge-studio/actions/workflows/test.yml/badge.svg)](https://github.com/ILoveBuns/versebridge-studio/actions/workflows/test.yml)

Biometric Scripture moments for workouts plus creator-ready content packs,
grounded in licensed YouVersion text and generated with Gloo AI.

## Run

```bash
python3 app.py
```

## Demo

[Watch the 76-second narrated product demo](artifacts/versebridge-demo.mp4).

Without credentials the app runs in a clearly labelled demo mode. For live integration, set `YVP_APP_KEY` and either `GLOO_ACCESS_TOKEN` or the three Gloo client-credential variables shown in `.env.example`.

## Design safeguards

- Scripture and generated commentary are visually separated.
- Every pack retains a visible reference and source link.
- The model receives only text retrieved from YouVersion and is instructed not to invent quotations.
- Generated reflections include a review note rather than presenting themselves as Scripture.

## Official hackathon data

The VersePulse flow consumes the competition's biometric fields (heart rate,
HR zone, activity, effort, recovery, stress, and session minute), detects the
current workout moment, and selects the closest compatible entry from the
official verse-movement mapping. It degrades to a small built-in mapping when
the Kaggle files are not present.
