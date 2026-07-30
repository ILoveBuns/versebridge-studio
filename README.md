# VerseBridge Studio

Creator-ready Scripture content packs grounded in licensed YouVersion text and generated with Gloo AI.

## Run

```bash
python3 app.py
```

Without credentials the app runs in a clearly labelled demo mode. For live integration, set `YVP_APP_KEY` and either `GLOO_ACCESS_TOKEN` or the three Gloo client-credential variables shown in `.env.example`.

## Design safeguards

- Scripture and generated commentary are visually separated.
- Every pack retains a visible reference and source link.
- The model receives only text retrieved from YouVersion and is instructed not to invent quotations.
- Generated reflections include a review note rather than presenting themselves as Scripture.
