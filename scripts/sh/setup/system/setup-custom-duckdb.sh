#!/usr/bin/env bash
set -euo pipefail

# Configuration
REPO_URL="git@github.com:utndatasystems/duckdb.git"
BRANCH="card-injection-1.4.2"
DIR_NAME="duckdb"

# Optional: change this if the script lives elsewhere
THIRD_PARTY_DIR="$(pwd)/third-party"

# Create third-party directory if needed
mkdir -p "$THIRD_PARTY_DIR"
cd "$THIRD_PARTY_DIR"

# Clone if not already present
if [ ! -d "$DIR_NAME" ]; then
  echo "Cloning *custom* DuckDB repository.."
  git clone "$REPO_URL" "$DIR_NAME"
else
  echo "DuckDB repository already exists, skipping clone."
fi

cd "$DIR_NAME"

# Fetch and checkout the desired branch
echo "Checking out branch: $BRANCH"
git fetch origin
git checkout "$BRANCH"
git pull origin "$BRANCH"

# Build
echo "Building DuckDB.."
export OVERRIDE_GIT_DESCRIBE="v1.4.2"
export GEN="ninja"

make

echo "DuckDB build completed successfully."
