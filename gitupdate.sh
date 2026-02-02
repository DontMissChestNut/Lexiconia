#!/bin/bash

current_branch=dev/mac
current_upstream=origin/dev/mac
target_upstream="$current_upstream"

current_branch=$(git rev-parse --abbrev-ref HEAD)
current_upstream=$(git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null)

update_repo() {
    echo "更新当前上游仓库 $current_upstream"
    git pull
    git add .
    git commit -m "update $current_branch"
    git push
    echo "更新完成"

    if [ "$target_upstream" != "$current_upstream" ]; then
        echo "更新目标上游分支 $target_upstream"
        git branch --set-upstream-to=$target_upstream
        git pull
        git add .
        git commit -m "update $target_upstream"
        git push origin HEAD:develop
        echo "推送完成"

        echo "设置上游分支为 dev/mac"
        git branch --set-upstream-to=origin/dev/mac
        
    fi

}


if [ "$current_branch" = "develop" ]; then
    echo "当前分支是保护分支 $current_branch ，切换到 dev/mac 分支"
    git checkout dev/mac
elif [ "$current_branch" != "dev/mac" ]; then
    echo "当前分支不是 dev/mac, 切换到 dev/mac 分支"
    git checkout dev/mac
fi

while [[ $# -gt 0 ]]; do
    case $1 in
        -m|--mac)
            target_upstream=origin/dev/mac
            shift
            ;;
        -d|--dev)
            target_upstream=origin/develop
            shift
            ;;
    esac
done

echo "========================================"
echo "当前分支: $current_branch"
echo "当前上游分支: $current_upstream"
echo "推送目标分支: $target_upstream"
echo "========================================"

update_repo