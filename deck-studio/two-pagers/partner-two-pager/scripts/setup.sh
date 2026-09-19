#!/bin/sh
# One-time runtime setup; rerun after an ephemeral sandbox restarts.
# Bun, poppler-utils and ImageMagick must be on PATH.
set -eu
command -v bun >/dev/null
command -v pdfinfo >/dev/null
command -v pdftotext >/dev/null
command -v pdftoppm >/dev/null
command -v pdffonts >/dev/null
command -v magick >/dev/null
# --with-deps installs Chromium's Linux libraries when permitted.
# If running without sudo/root, install system libraries with your administrator,
# then run: bunx playwright@1.58.2 install chromium
bunx playwright@1.58.2 install --with-deps chromium
