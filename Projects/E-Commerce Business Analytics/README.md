# Olist E-Commerce — Business Analytics Project

A business-analyst engagement analyzing real Brazilian e-commerce transactional data: relational database design, SQL-driven KPI analysis, customer segmentation, and operational diagnostics — structured as a 4-week engagement and delivered with reproducible code.

## Dataset

**Brazilian E-Commerce Public Dataset by Olist** — real, anonymized transactional data, 2016–2018.
- Official source: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
- 99,441 orders · 99,441 customer records · 3,095 sellers · 32,951 products · 8,000 marketing leads
- 11 raw CSVs (place them in `data/raw/` before running — see **Reproducing this project** below)

## Project structure

```
.
├── data/
│   ├── raw/                     # place the 11 source CSVs here
│   └── olist.db                 # built SQLite database (generated)
├── sql/                         # 10 standalone, documented KPI queries
├── notebook/
│   └── Olist_Business_Analytics.ipynb   # the full, executed 4-week analysis
├── dashboard/
│   └── olist_dashboard.html     # standalone interactive Plotly dashboard
├── reports/
│   └── Executive_Summary.docx   # 3-page non-technical summary + recommendations
├── scripts/
│   ├── build_database.py        # CSVs -> normalized SQLite DB (with indices)
│   ├── build_dashboard.py       # DB -> interactive HTML dashboard
│   └── build_exec_summary.js    # charts + findings -> Word doc
├── requirements.txt             # pinned Python dependency versions
└── run_pipeline.sh              # one-command full reproduction
```

## Engagement structure (notebook sections)

- **Week 1 — Data Foundation:** build the relational database, audit data quality (including the decision to exclude the near-empty Sep–Dec 2016 pilot period and the Sep–Oct 2018 trailing tail), define KPIs
- **Week 2 — Sales & Business Performance:** revenue trend, category mix, state-level geography, payment behavior, order fulfillment funnel
- **Week 3 — Customer Analytics:** RFM segmentation, repeat-purchase rate, monthly cohort retention analysis, high-value customer profiling
- **Week 4 — Operations & Satisfaction:** delivery timeliness vs. review score, seller scorecards, marketing funnel conversion by channel, final ranked recommendations

## Headline findings

| Finding | Detail |
|---|---|
| **Revenue plateau** | GMV grew steadily through 2017 (with a Nov 2017 Black Friday spike) but has flattened since March 2018 |
| **Retention is effectively absent** | Only **3.0%** of customers place a second order; every monthly cohort (20 in a row) drops to <1% retention by month 1 |
| **Delivery drives satisfaction** | Avg review score falls from **4.32** (early delivery) to **1.73** (very late) — the strongest single driver of dissatisfaction in the data |
| **Payment behavior** | Credit card = 78% of payment value, avg 3.5 installments — core to how customers afford larger baskets |

Full detail, charts, and the ranked recommendation list are in `reports/Executive_Summary.docx` and `notebook/Olist_Business_Analytics.ipynb`.

## Reproducing this project (after a week, or anytime)

**1. Get the raw data.** Download the 11 CSVs from the Kaggle link above (or wherever you originally sourced them) and place them in `data/raw/`. Expected filenames:
```
customers.csv, geolocation.csv, leads_closed.csv, leads_qualified.csv,
orders.csv, order_items.csv, order_payments.csv, order_reviews.csv,
products.csv, product_category_name_translation.csv, sellers.csv
```

**2. Install prerequisites.**
- Python 3.10+
- Node.js (only needed if you want to regenerate `reports/Executive_Summary.docx`; the `docx` npm package must be available — `npm install docx` if not already present)

**3. Run the pipeline.**
```bash
bash run_pipeline.sh
```
This single command: installs pinned Python packages → rebuilds the SQLite database from the raw CSVs → copies the DB and SQL files into `notebook/` → executes the full notebook end-to-end (regenerating all 12 chart images) → rebuilds the interactive dashboard. Takes about 1-2 minutes.

**4. (Optional) Rebuild the executive summary.** Only needed if you've changed the underlying charts/findings:
```bash
node scripts/build_exec_summary.js
```

**5. Open the outputs.**
- `notebook/Olist_Business_Analytics.ipynb` — open in Jupyter to read the full analysis
- `dashboard/olist_dashboard.html` — open directly in any browser, no server needed
- `reports/Executive_Summary.docx` — open in Word/Google Docs

## Why this is structured the way it is (notes for interviews)

- **SQL lives in standalone `.sql` files**, not inline strings — this is how a BA would work against a real analytics warehouse, and it makes every query independently reviewable and reusable.
- **`customer_unique_id` vs `customer_id`** — Olist assigns a new `customer_id` per order, so identifying true repeat customers requires joining on `customer_unique_id`. Getting this wrong is a common mistake that silently makes the repeat-purchase rate look like ~0% (every "customer" looks one-time); the SQL queries here handle it correctly and it's called out explicitly in `sql/05_rfm_base.sql`.
- **The Jan 2017 – Aug 2018 window is a documented, justified decision**, not an arbitrary cut — see notebook Section 1.3.
- **A real bug and fix are part of the build history**: the initial database was missing an index on `customers.customer_id`, which caused a join to silently hang (an effective ~9.9 billion-row nested-loop scan on two ~99K-row tables) rather than error out. `scripts/build_database.py` now creates a complete index set; this is a good, honest example to mention if asked about debugging experience.

## Possible extensions

- Layer in fulfillment cost and marketing spend data to convert findings into ROI-ranked recommendations
- A/B test a retention intervention against a holdout cohort
- Re-run monthly and track KPI trends over time rather than as a single snapshot
- Extend the seller scorecard into a full seller-tiering/incentive system
