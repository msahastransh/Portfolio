"""
build_dashboard.py
Builds a standalone interactive HTML dashboard (Plotly) summarizing the key
Olist business analytics findings. Run from the project root:
    python3 scripts/build_dashboard.py
Output: dashboard/olist_dashboard.html
"""
import sqlite3
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

BASE = os.path.join(os.path.dirname(__file__), '..')
DB_PATH = os.path.join(BASE, 'data', 'olist.db')
SQL_DIR = os.path.join(BASE, 'sql')
OUT_PATH = os.path.join(BASE, 'dashboard', 'olist_dashboard.html')

conn = sqlite3.connect(DB_PATH)

def run_sql(filename):
    with open(os.path.join(SQL_DIR, filename)) as f:
        query = f.read()
    return pd.read_sql(query, conn)

COLORS = ['#2E5EAA','#E8743B','#19A979','#ED4A7B','#945ECF','#13A4B4','#F2B134','#7A7A7A']

# ---------- Pull data ----------
rev = run_sql('01_monthly_revenue_trend.sql')
rev['year_month'] = pd.to_datetime(rev['year_month'])

cat = run_sql('02_category_performance.sql')
cat = cat[cat['order_count'] >= 20].nlargest(12, 'product_revenue')

state = run_sql('03_state_analysis.sql').nlargest(10, 'gmv')

pay = run_sql('04_payment_behavior.sql')

repeat = run_sql('06_repeat_purchase_rate.sql')

delivery = run_sql('07_delivery_vs_satisfaction.sql')

funnel_conv = run_sql('09_marketing_funnel_conversion.sql')
funnel_conv = funnel_conv[funnel_conv['total_leads'] >= 50].sort_values('conversion_rate_pct')

# ---------- Build figure: 3x2 grid ----------
fig = make_subplots(
    rows=3, cols=2,
    subplot_titles=(
        "Monthly GMV Trend", "Top Categories by Revenue",
        "GMV by State (Top 10)", "Payment Method Share",
        "Delivery Timeliness vs Avg Review Score", "Repeat vs One-Time Customers"
    ),
    specs=[[{"type":"scatter"}, {"type":"bar"}],
           [{"type":"bar"}, {"type":"pie"}],
           [{"type":"bar"}, {"type":"pie"}]],
    vertical_spacing=0.1, horizontal_spacing=0.12
)

# 1. GMV trend
fig.add_trace(go.Scatter(x=rev['year_month'], y=rev['gmv'], mode='lines+markers',
                          line=dict(color=COLORS[0], width=3), name='GMV',
                          hovertemplate='%{x|%Y-%m}<br>GMV: R$%{y:,.0f}<extra></extra>'),
              row=1, col=1)

# 2. Category revenue
fig.add_trace(go.Bar(y=cat['category'], x=cat['product_revenue'], orientation='h',
                      marker_color=COLORS[0], name='Revenue',
                      hovertemplate='%{y}<br>Revenue: R$%{x:,.0f}<extra></extra>'),
              row=1, col=2)

# 3. State GMV
fig.add_trace(go.Bar(x=state['state'], y=state['gmv'], marker_color=COLORS[2], name='GMV by state',
                      hovertemplate='%{x}<br>GMV: R$%{y:,.0f}<extra></extra>'),
              row=2, col=1)

# 4. Payment share
fig.add_trace(go.Pie(labels=pay['payment_type'], values=pay['total_payment_value'],
                      marker_colors=COLORS, name='Payment share', hole=0.35),
              row=2, col=2)

# 5. Delivery vs satisfaction
delivery_colors = [COLORS[2], COLORS[0], COLORS[6], COLORS[1]]
fig.add_trace(go.Bar(x=delivery['delivery_bucket'], y=delivery['avg_review_score'],
                      marker_color=delivery_colors, name='Avg review score',
                      hovertemplate='%{x}<br>Avg score: %{y:.2f}<extra></extra>'),
              row=3, col=1)

# 6. Repeat vs one-time
fig.add_trace(go.Pie(labels=['One-time buyers','Repeat buyers'],
                      values=[repeat['one_time_customers'][0], repeat['repeat_customers'][0]],
                      marker_colors=[COLORS[7], COLORS[2]], name='Customer type', hole=0.35),
              row=3, col=2)

fig.update_layout(
    height=1400, width=1250,
    title_text="<b>Olist E-Commerce — Business Analytics Dashboard</b><br><sup>Jan 2017 – Aug 2018 | Real transactional data, 96,478 delivered orders</sup>",
    title_x=0.5,
    showlegend=False,
    font=dict(family="Arial, sans-serif", size=11),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(t=120)
)
fig.update_xaxes(tickangle=45, row=2, col=1)
fig.update_xaxes(tickangle=15, row=3, col=1)
fig.update_yaxes(title_text="R$", row=1, col=1)
fig.update_yaxes(title_text="R$", row=2, col=1)
fig.update_yaxes(title_text="Avg score (1-5)", row=3, col=1)

# Add annotation banner with headline KPIs
total_gmv = rev['gmv'].sum()
total_orders = rev['order_count'].sum()
repeat_rate = repeat['repeat_rate_pct'][0]

kpi_html = f"""
<div style="font-family: Arial, sans-serif; max-width: 1250px; margin: 20px auto; padding: 20px;
            background: #f7f9fc; border-radius: 10px; display: flex; justify-content: space-around; text-align:center;">
  <div><div style="font-size:26px; font-weight:bold; color:{COLORS[0]}">R$ {total_gmv:,.0f}</div><div style="color:#555">Total GMV</div></div>
  <div><div style="font-size:26px; font-weight:bold; color:{COLORS[2]}">{total_orders:,.0f}</div><div style="color:#555">Delivered Orders</div></div>
  <div><div style="font-size:26px; font-weight:bold; color:{COLORS[1]}">{repeat_rate:.1f}%</div><div style="color:#555">Repeat Purchase Rate</div></div>
  <div><div style="font-size:26px; font-weight:bold; color:{COLORS[3]}">{delivery['avg_review_score'].iloc[0]:.2f} → {delivery['avg_review_score'].iloc[-1]:.2f}</div><div style="color:#555">Review Score: Early vs Very Late Delivery</div></div>
</div>
"""

os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
fig_html = fig.to_html(include_plotlyjs='cdn', full_html=False)

full_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Olist Business Analytics Dashboard</title>
</head>
<body style="margin:0; background:#ffffff;">
{kpi_html}
{fig_html}
<div style="font-family: Arial, sans-serif; max-width:1250px; margin: 10px auto 40px; padding: 15px 20px;
            color:#777; font-size:12px; text-align:center;">
  Built from the Olist Brazilian E-Commerce Public Dataset (real, anonymized data, 2016-2018). Hover over charts for details.
</div>
</body>
</html>
"""

with open(OUT_PATH, 'w') as f:
    f.write(full_html)

print(f"Dashboard written to {OUT_PATH}")
print(f"Total GMV: R$ {total_gmv:,.2f}  |  Orders: {total_orders:,}  |  Repeat rate: {repeat_rate:.1f}%")
