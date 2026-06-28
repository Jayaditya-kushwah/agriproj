#!/usr/bin/env bash
# .specify/scripts/bash/speckit.sh
# AgriDoc Spec-Kit Lifecycle Automation

set -euo pipefail

SPECS_DIR="specs"
TEMPLATES_DIR=".specify/templates"

usage() {
  echo "AgriDoc Spec-Kit CLI"
  echo ""
  echo "Usage: bash .specify/scripts/bash/speckit.sh <command> [args]"
  echo ""
  echo "Commands:"
  echo "  init <NNN-feature-name>   Bootstrap a new feature spec"
  echo "  list                      List all feature specs"
  echo "  status                    Show completion status of all specs"
  echo "  help                      Show this help"
}

cmd_init() {
  local name="${1:-}"
  if [[ -z "$name" ]]; then
    echo "Error: feature name required (e.g. 002-farmer-registration)"
    exit 1
  fi
  local dir="$SPECS_DIR/$name"
  if [[ -d "$dir" ]]; then
    echo "Spec '$name' already exists at $dir"
    exit 1
  fi
  mkdir -p "$dir"
  cp "$TEMPLATES_DIR/spec.md"  "$dir/spec.md"
  cp "$TEMPLATES_DIR/plan.md"  "$dir/plan.md"
  cp "$TEMPLATES_DIR/tasks.md" "$dir/tasks.md"
  touch "$dir/data-model.md" "$dir/research.md"
  echo "✅ Spec bootstrapped at $dir"
  echo "   Next: Edit $dir/spec.md"
}

cmd_list() {
  echo "📁 Feature Specs:"
  if [[ -d "$SPECS_DIR" ]]; then
    ls -1 "$SPECS_DIR/" 2>/dev/null | while read -r d; do
      echo "  - $d"
    done
  else
    echo "  No specs found. Run: speckit init <name>"
  fi
}

cmd_status() {
  echo "📊 Spec-Kit Status:"
  if [[ -d "$SPECS_DIR" ]]; then
    for dir in "$SPECS_DIR"/*/; do
      local name; name=$(basename "$dir")
      local spec_done=0 plan_done=0 tasks_done=0
      [[ -s "$dir/spec.md" ]] && spec_done=1
      [[ -s "$dir/plan.md" ]] && plan_done=1
      [[ -s "$dir/tasks.md" ]] && tasks_done=1
      local total=$((spec_done + plan_done + tasks_done))
      echo "  $name — spec:$spec_done plan:$plan_done tasks:$tasks_done ($total/3)"
    done
  fi
}

case "${1:-help}" in
  init)   cmd_init "${2:-}" ;;
  list)   cmd_list ;;
  status) cmd_status ;;
  help|*) usage ;;
esac
