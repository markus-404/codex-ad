# Security Policy

## Supported Use

This repository packages a local Codex plugin and Python helper scripts for
static ad prompt generation. It is not a hosted service and does not include
authentication, storage, or network listeners.

## Secrets

Do not commit API keys, `.env` files, client assets, campaign data, or private
brand briefs. Runtime image generation reads `OPENAI_API_KEY` from the local
environment.

## Image Inputs

The compositing helper opens local image files with Pillow. Only use image files
from trusted campaign folders.

## Reporting

Report issues to the repository owner.
