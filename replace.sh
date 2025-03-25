#!/usr/bin/env bash
# Usage:
#  replace.sh <file>
sed -i '' \
    -e 's/“/"/g' \
    -e 's/”/"/g' \
    -e 's/–/ -- /g' \
    -e "s/’/'/g" \
    $1
