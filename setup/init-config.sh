#!/bin/bash
echo "Initializing bot configuration..."

VOICE_DIR="./voices"
if [ ! -d "$VOICE_DIR" ]; then
  mkdir -p "$VOICE_DIR"
  echo "Created voice directory: $VOICE_DIR"
else
  echo "Voice directory already exists: $VOICE_DIR"
fi

echo "Setup complete!"
