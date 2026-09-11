# KNR AEGIS AI ⚡

**AEGIS — Agentic Executive & General Intelligence System**

## Mobile no-API experiment

The `mobile/` application is a browser/PWA shell designed for phone experiments without requiring a hosted LLM API key. It requests camera and microphone access only after explicit user interaction and can attempt on-device WebGPU inference using WebLLM.

### Important

- This does **not** provide silent or unrestricted access to the phone.
- Camera/microphone access is controlled by Android/browser permissions.
- On-device model inference depends on compatible WebGPU support and available device memory.
- The first model load can download substantial model weights.
- The existing AEGIS agent backend, provider router, cybersecurity skills, device ACLs, and model-training pipeline remain separate from this browser experiment.

### Mobile deployment

`.github/workflows/pages-mobile.yml` deploys `mobile/` through GitHub Pages when the branch is pushed and Pages is enabled.

## Core AEGIS status

AEGIS is an agent platform for research, coding, content, automation, real-estate operations, and defensive cybersecurity. The custom foundation-model training pipeline exists in `training/`, but a new foundation model has not yet been trained.
