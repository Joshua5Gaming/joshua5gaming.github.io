#!/bin/bash
# Go to your repo folder
cd "E:/Documents/A1 - My Stuff/joshua5gaming.github.io" || exit

# Make sure we have the latest info from GitHub
git fetch origin

# Force reset local branch to GitHub (main branch)
git reset --hard origin/main

# Remove untracked files (optional, uncomment if you want a clean slate)
# git clean -fd

echo "✅ Local files are now identical to GitHub (origin/main)."
