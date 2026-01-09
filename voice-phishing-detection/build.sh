#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install ffmpeg
apt-get update && apt-get install -y ffmpeg

# Install dependencies
pip install --upgrade pip
pip install -r backend/requirements.txt
