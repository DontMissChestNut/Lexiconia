#!/bin/bash

current_branch=$(git rev-parse --abbrev-ref HEAD)

upstream=$(git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null)

echo "========================================"
echo "当前分支: $current_branch"
echo "上游分支: $upstream"
echo "========================================"
