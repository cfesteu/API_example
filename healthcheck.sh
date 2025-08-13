#!/bin/bash
set -euo pipefail



result=$(sqlplus -S -L $ORC_USERNAME/"$ORC_PASSWORD"@//source_db:1521/XEPDB1 <<'EOF'
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