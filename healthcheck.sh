#!/usr/bin/env bash

set -euo

result=$(sqlplus -S -L target/'ACMflorin1975!'@//source_db:1521/XEPDB1 <<'EOF'
WHENEVER SQLERROR EXIT 1
SET PAGES 0 FEEDBACK OFF HEADING OFF
SELECT COUNT(*) FROM target.fact_activity;
EXIT
EOF
)

count=$(echo "$result" | tr -dc '0-9')

if [ "$count" -gt 0 ]; then
  exit 0
else
  exit 1
fi