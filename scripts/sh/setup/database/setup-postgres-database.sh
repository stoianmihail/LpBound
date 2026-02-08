#!/bin/bash

# ===========================================
# Script: setup-postgres-database.sh
# Purpose: Drop & recreate a PostgreSQL database, then load schema + data
# Usage: ./setup-postgres-database.sh <database_name>
# Example: ./setup-postgres-database.sh stackoverflow_dba
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
  echo "Example: $0 stackoverflow_dba"
  exit 1
fi

DATABASE_NAME="$1"

# --- Drop existing DB ---
log_info "Dropping old database (if it exists)..."
dropdb --if-exists "$DATABASE_NAME"

# --- Create fresh DB ---
log_info "Creating fresh database..."
createdb "$DATABASE_NAME"

# --- Run schema ---
log_info "Running schema..."
psql "$DATABASE_NAME" \
  -f metadata/$DATABASE_NAME/postgres/postgres-$DATABASE_NAME-schema.sql

# --- Load data ---
log_info "Loading data..."
psql "$DATABASE_NAME" \
  -f  metadata/$DATABASE_NAME/postgres/postgres-$DATABASE_NAME-load.sql

# --- Done ---
log_info "Done. Database '$DATABASE_NAME' is ready."