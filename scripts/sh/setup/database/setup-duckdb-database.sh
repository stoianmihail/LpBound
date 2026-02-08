#!/usr/bin/env bash

# ===========================================
# Script: setup-duckdb-database.sh
# Purpose: Generate and load all norms SQL dumps into DuckDB with timing
# Usage: ./setup-duckdb-database.sh <database_name>
# Example: ./setup-duckdb-database.sh imdb
# ===========================================

set -euo pipefail

# --- Colors ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# --- Logging ---
log_info()  { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# --- Command existence helper ---
command_exists() {
  command -v "$1" >/dev/null 2>&1
}

# --- Check required argument ---
if [[ $# -lt 1 ]]; then
  log_error "Missing database file argument."
  echo "Usage: $0 <database_name>"
  echo "Example: $0 imdb"
  exit 1
fi

DATABASE_NAME="$1"
DATABASE_FILE="dbs/${DATABASE_NAME}::base.duckdb"

# Specify the timing file.
HOSTNAME=$(hostname)
TIMING_FILE="results/timing/${DATABASE_NAME}-${HOSTNAME}-timing.txt"

# Ensure timing directory exists
mkdir -p results/timing

# If file doesn't exist, write header
if [[ ! -f "$TIMING_FILE" ]]; then
  echo "load-time [ms]" > "$TIMING_FILE"
fi

# --- Ensure DB directory exists ---
mkdir -p dbs

if [[ -f "$DATABASE_FILE" ]]; then
  log_warn "Database already exists on disk as: $DATABASE_FILE."
  log_warn "Removing existing database..."
  rm -f "$DATABASE_FILE"
  log_info "Old database removed."
else
  log_info "No existing database found. Creating fresh DB."
fi

# --- Start timing ---
start=$(python3 -c 'import time; print(time.perf_counter())')

# --- Run schema creation and load ---
log_info "Creating schema..."
duckdb "$DATABASE_FILE" -f metadata/$DATABASE_NAME/duckdb/duckdb-$DATABASE_NAME-schema.sql

log_info "Loading data..."
duckdb "$DATABASE_FILE" -f metadata/$DATABASE_NAME/duckdb/duckdb-$DATABASE_NAME-load.sql

# --- End timing ---
end=$(python3 -c 'import time; print(time.perf_counter())')
duration_ms=$(python3 -c "print(round((${end} - ${start}) * 1000, 3))")

# --- Append timing ---
echo "${duration_ms}" >> "$TIMING_FILE"

log_info "Database setup complete: $DATABASE_FILE"
log_info "Total loading time: ${duration_ms} ms"
log_info "Timing written to: $TIMING_FILE"