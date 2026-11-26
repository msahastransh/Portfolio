#!/usr/bin/env bash
# run_pipeline.sh
# One-command reproduction of the full Olist Business Analytics project.
# Usage: bash run_pipeline.sh
#
# Prerequisites: raw CSVs must already be in data/raw/ (see README.md for the
# download link/instructions). Requires Python 3.10+, Node.js (for the
# executive summary doc), and the packages in requirements.txt.

set -e  # stop on first error

echo "=================================================="
echo " Olist Business Analytics — Full Pipeline"
echo "=================================================="

echo ""
echo "[1/5] Installing Python dependencies..."
pip install -r requirements.txt --break-system-packages --quiet

echo ""
echo "[2/5] Building SQLite database from raw CSVs..."
python3 scripts/build_database.py

echo ""
echo "[3/5] Copying database + SQL files into notebook/ (self-contained execution)..."
cp data/olist.db notebook/olist.db
mkdir -p notebook/sql notebook/figs
cp sql/*.sql notebook/sql/
rm -f notebook/figs/*.png

echo ""
echo "[4/5] Executing the analysis notebook end-to-end..."
jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 \
    --output Olist_Business_Analytics.ipynb notebook/Olist_Business_Analytics.ipynb

echo ""
echo "[5/5] Building the interactive dashboard..."
python3 scripts/build_dashboard.py

echo ""
echo "=================================================="
echo " Done. Outputs:"
echo "   - data/olist.db                              (SQLite database)"
echo "   - notebook/Olist_Business_Analytics.ipynb     (executed notebook + charts)"
echo "   - notebook/figs/*.png                         (14 standalone chart images)"
echo "   - dashboard/olist_dashboard.html              (interactive dashboard)"
echo "   - reports/Executive_Summary.docx              (already built; re-run"
echo "       'node scripts/build_exec_summary.js' if you change the source charts)"
echo "=================================================="
