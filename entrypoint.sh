#!/bin/sh

# Run npm build
npm run build

# Check exit code of npm run build
if [ $? -ne 0 ]; then
  echo "Error: npm run build failed. Aborting..."
  exit 1
fi

# Start the Python backend server
python backend/server.py