#!/usr/bin/env bash
IFS=$'\t' read -r n posted title company loc url <<< "$1"
f="$2/$n.txt"
{ echo "URL: $url"; echo "TITLE: $title"; echo "COMPANY: $company"; echo "LOC: $loc"; echo "POSTED: $posted"; python3 scripts/fetch-jd.py "$url"; } > "$f" 2>/dev/null
