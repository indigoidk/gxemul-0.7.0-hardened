#!/bin/bash
cat "$NULDIR/ans.txt"
case "$NULCASE" in
  wd)    printf 'OpenAI Codex v0.153.4\n--------\nworkdir: x\000y\nmodel: gpt-6-astra\nreasoning effort: ultra\n--------\n' 1>&2 ;;
  model) printf 'OpenAI Codex v0.153.4\n--------\nworkdir: x\nmodel: gpt-6-a\000stra\nreasoning effort: ultra\n--------\n' 1>&2 ;;
  other) printf 'OpenAI Codex v0.153.4\n--------\nworkdir: x\nmodel: gpt-6-other\000\nreasoning effort: ultra\n--------\n' 1>&2 ;;
esac
exit 0
