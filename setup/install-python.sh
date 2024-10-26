#!/bin/bash
echo "Installing Python via Homebrew..."
if ! command -v python3 &> /dev/null; then
  brew install python
else
  echo "Python is already installed."
fi
