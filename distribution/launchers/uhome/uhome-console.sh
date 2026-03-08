#!/bin/sh
set -eu

MODULE="home"
if [ "${1:-}" = "--module" ] && [ -n "${2:-}" ]; then
  MODULE="$2"
fi

run_command() {
  if [ "${SONIC_LAUNCHER_TEST_MODE:-0}" = "1" ]; then
    printf '%s\n' "$*"
    return 0
  fi
  exec "$@"
}

case "$MODULE" in
  home)
    run_command steam -bigpicture "steam://open/library"
    ;;
  library)
    run_command steam -bigpicture "steam://open/games"
    ;;
  settings)
    run_command /usr/bin/env sh -lc "printf 'uHOME settings placeholder\n'"
    ;;
  *)
    printf 'Unknown uHOME module: %s\n' "$MODULE" >&2
    exit 1
    ;;
esac
