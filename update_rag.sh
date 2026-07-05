#!/usr/bin/env bash
# update_rag.sh — updates your RAG project files
# Usage: bash update_rag.sh [path/to/your/rag_project]

set -e

PROJECT="${1:-$(pwd)}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$SCRIPT_DIR"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  RAG Project Updater"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Target: $PROJECT"
echo ""

# Verify source exists
if [ ! -d "$SRC" ]; then
  echo "❌ Could not find source files at: $SRC"
  echo "   Make sure update_rag.sh is in the same folder as the rag_project/ directory."
  exit 1
fi

# Backup existing project
BACKUP="$PROJECT/../rag_backup_$(date +%Y%m%d_%H%M%S)"
echo "📦 Backing up current project to:"
echo "   $BACKUP"
cp -r "$PROJECT" "$BACKUP"
echo "✅ Backup done"
echo ""

# Copy src files
echo "📂 Updating src/ files..."
cp "$SRC/src/db.py"           "$PROJECT/src/db.py"
cp "$SRC/src/embeddings.py"   "$PROJECT/src/embeddings.py"
cp "$SRC/src/chunking.py"     "$PROJECT/src/chunking.py"
cp "$SRC/src/pdf_loader.py"   "$PROJECT/src/pdf_loader.py"
cp "$SRC/src/ingestion.py"    "$PROJECT/src/ingestion.py"
cp "$SRC/src/search.py"       "$PROJECT/src/search.py"
cp "$SRC/src/rag_pipeline.py" "$PROJECT/src/rag_pipeline.py"
cp "$SRC/src/app.py"          "$PROJECT/src/app.py"
cp "$SRC/src/__init__.py"     "$PROJECT/src/__init__.py"
echo "✅ src/ updated"

# Copy root files
echo "📂 Updating root files..."
cp "$SRC/run.py"              "$PROJECT/run.py"
cp "$SRC/requirements.txt"    "$PROJECT/requirements.txt"
cp "$SRC/widget.html"         "$PROJECT/widget.html"

# Only copy .env.example if .env doesn't exist (don't overwrite credentials)
if [ ! -f "$PROJECT/.env" ]; then
  cp "$SRC/.env.example" "$PROJECT/.env"
  echo "⚠️  .env created from template — fill in your DB credentials"
else
  echo "ℹ️  .env already exists — skipping (your credentials are safe)"
fi
echo "✅ Root files updated"

# Install new dependencies
echo ""
echo "📦 Installing/updating dependencies..."
pip install -r "$PROJECT/requirements.txt" --quiet
echo "✅ Dependencies up to date"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  All done! Run your project with:"
echo "  cd $PROJECT && python run.py"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
