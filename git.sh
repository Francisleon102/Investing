#!/bin/bash

read -p "Enter your commit message: " text

git add .

if git diff --cached --quiet; then
    echo "Nothing to commit."
else
    git commit -m "$text"
    git push origin main
fi