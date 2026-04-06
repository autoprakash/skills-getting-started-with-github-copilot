#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MAILHOG_BIN="$ROOT_DIR/.bin/mailhog"
LOGFILE="$ROOT_DIR/mailhog.log"

if [ ! -x "$MAILHOG_BIN" ]; then
  echo "MailHog binary not found at $MAILHOG_BIN"
  echo "Please install MailHog in .bin/mailhog and make it executable."
  exit 1
fi

echo "Stopping any existing MailHog processes on ports 1025/8025..."
PIDS="$(lsof -t -iTCP:1025 -sTCP:LISTEN -P 2>/dev/null || true) $(lsof -t -iTCP:8025 -sTCP:LISTEN -P 2>/dev/null || true)" || true
if [ -n "${PIDS// /}" ]; then
  kill -9 $PIDS 2>/dev/null || true
fi

echo "Starting MailHog..."
nohup "$MAILHOG_BIN" \
  -ui-bind-addr 0.0.0.0:8025 \
  -api-bind-addr 0.0.0.0:8025 \
  -smtp-bind-addr 0.0.0.0:1025 \
  > "$LOGFILE" 2>&1 &

sleep 1

echo "MailHog started."
echo "HTTP UI: http://localhost:8025"
echo "SMTP: localhost:1025"
echo "Logs: $LOGFILE"
