const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, ImageRun,
  Table, TableRow, TableCell, WidthType, ShadingType, BorderStyle,
  AlignmentType, Numbering, LevelFormat, convertInchesToTwip
} = require("docx");

const FIGS = "/home/claude/ba_proj/notebook/figs";
const BLUE = "2E5EAA";
const ORANGE = "E8743B";
const GREEN = "19A979";
const GREY = "666666";

function h1(text) {
  return new Paragraph({ text, heading: HeadingLevel.HEADING_1, spacing: { before: 300, after: 150 } });
}
function h2(text) {
  return new Paragraph({ text, heading: HeadingLevel.HEADING_2, spacing: { before: 250, after: 120 } });
}
function body(text, opts = {}) {
  return new Paragraph({
    children: [new TextRun({ text, ...opts })],
    spacing: { after: 160 },
  });
}
function bullet(text, bold) {
  return new Paragraph({
    text,
    bullet: { level: 0 },
    spacing: { after: 80 },
  });
}
function image(path, widthPx, heightPx, maxWidthIn = 6.3) {
  const scale = Math.min(1, (maxWidthIn * 96) / widthPx);
  return new Paragraph({
    children: [
      new ImageRun({
        type: "png",
        data: fs.readFileSync(path),
        transformation: { width: widthPx * scale, height: heightPx * scale },
      }),
    ],
    spacing: { after: 200 },
    alignment: AlignmentType.CENTER,
  });
}

function kpiTable(rows) {
  const colWidths = [3200, 3200, 3200];
  return new Table({
    width: { size: 9600, type: WidthType.DXA },
    columnWidths: colWidths,
    rows: rows.map((r, i) =>
      new TableRow({
        children: r.map((cellText, j) =>
          new TableCell({
            width: { size: colWidths[j], type: WidthType.DXA },
            shading: i === 0 ? { fill: BLUE, type: ShadingType.CLEAR } : undefined,
            margins: { top: 100, bottom: 100, left: 120, right: 120 },
            children: [
              new Paragraph({
                children: [
                  new TextRun({
                    text: cellText,
                    bold: i === 0,
                    color: i === 0 ? "FFFFFF" : "000000",
                  }),
                ],
              }),
            ],
          })
        ),
      })
    ),
  });
}

const doc = new Document({
  sections: [
    {
      properties: {
        page: { size: { width: 12240, height: 15840 }, margin: { top: 1000, bottom: 1000, left: 1100, right: 1100 } },
      },
      children: [
        new Paragraph({
          children: [new TextRun({ text: "Olist E-Commerce", bold: true, size: 48, color: BLUE })],
          spacing: { after: 60 },
        }),
        new Paragraph({
          children: [new TextRun({ text: "Business Analytics — Executive Summary", bold: true, size: 32, color: "333333" })],
          spacing: { after: 200 },
        }),
        body("Prepared as a business-analyst engagement summary covering sales performance, customer analytics, and operations. Dataset: Brazilian E-Commerce Public Dataset by Olist (real, anonymized transactional data). Analysis window: January 2017 – August 2018.", { italics: true, color: GREY, size: 20 }),

        h1("Headline Numbers"),
        kpiTable([
          ["Metric", "Value", "Context"],
          ["Total GMV", "R$ 15.37M", "Jan 2017 – Aug 2018, delivered orders"],
          ["Delivered orders", "96,478", "97% of all orders placed"],
          ["Repeat purchase rate", "3.0%", "Of 93,104 unique customers"],
          ["Review score, on-time vs very late delivery", "4.32 → 1.73", "On a 1–5 scale"],
        ]),

        h1("Purpose & Scope"),
        body("This engagement analyzed Olist's transactional marketplace data to answer four questions a business stakeholder would ask: (1) How is revenue trending, and why? (2) Who are our customers, and are we keeping them? (3) What operational factors drive customer satisfaction? (4) Which acquisition channels are working? The full technical analysis — SQL queries, code, and 12 supporting charts — lives in the accompanying Jupyter notebook and SQL query library; this document summarizes the findings and recommendations for a non-technical audience."),

        h1("Key Finding 1 — Revenue Growth Is Plateauing"),
        image(`${FIGS}/01_revenue_trend.png`, 1289, 690),
        body("GMV grew steadily through 2017, with a clear seasonal spike in November 2017 (Black Friday). Growth continued into early 2018 but has since plateaued — order count has flattened and even dipped slightly from March 2018 onward, while average order value stays roughly flat. Order cancellation rates remain low and stable throughout, ruling out a fulfillment or checkout problem as the cause. The explanation lies in Finding 2, below."),

        h1("Key Finding 2 — Retention Is Effectively Absent"),
        image(`${FIGS}/08_cohort_retention.png`, 1198, 690),
        body("Only 3.0% of customers ever place a second order. The cohort retention heatmap above is the clearest evidence: every single monthly cohort from January 2017 through August 2018 — 20 consecutive cohorts — collapses to under roughly 1% still active by the following month, with no exceptions and no improving trend over time. This means the business is almost entirely dependent on new-customer acquisition for growth; there is essentially no repeat-revenue base cushioning it. This directly explains the plateau in Finding 1: once acquisition growth slows, so does total GMV, because there is minimal repeat purchasing to fall back on."),

        h1("Key Finding 3 — Delivery Speed Is the Strongest Driver of Satisfaction"),
        image(`${FIGS}/09_delivery_satisfaction.png`, 1289, 490),
        body("Average review score falls from 4.32 (delivered 7+ days early) to 1.73 (delivered more than a week late) — a drop of over 2.5 points on a 5-point scale. The share of negative reviews (score ≤ 2) rises from about 9% when on time to about 78% when very late. This relationship is stronger and more consistent than any product-category or price effect found in the data, making delivery reliability the single highest-leverage lever for improving customer satisfaction — and, by extension, the retention problem in Finding 2."),

        h1("Recommendations, Ranked by Expected Impact"),
        bullet("1. Improve delivery-estimate accuracy and logistics reliability, prioritizing the slowest-delivery states and the lowest-scoring individual sellers identified in the seller scorecard analysis. This is the highest-confidence lever in the entire analysis."),
        bullet("2. Design and launch a post-purchase retention program (reminder email, second-order incentive, or loyalty points) targeted at recent first-time buyers — there is currently no visible retention mechanism in the data, and even a modest lift in repeat rate would materially change the revenue mix."),
        bullet("3. Review underperforming sellers individually rather than by category alone — satisfaction problems in this data are often seller-specific and controllable, not purely category- or logistics-driven."),
        bullet("4. Treat the current growth plateau as a structural risk, not a temporary dip — flag to leadership that GMV is currently a near-direct function of acquisition spend, with little retention cushion."),
        bullet("5. Reallocate a small amount of seller-acquisition marketing budget away from the weakest-converting channels (email, display) toward the strongest (paid search, organic search), pending a larger-sample validation."),

        h1("Suggested Next Steps"),
        body("Re-run this analysis on a rolling monthly basis so these trends can be tracked going forward rather than viewed as a single snapshot. Pair a retention intervention (Recommendation 2) with an A/B test against a holdout group to measure causal impact before a full rollout. Layer in cost data — fulfillment cost per order, marketing spend per channel — to convert these directional recommendations into an ROI-ranked action plan with dollar-value projections."),

        new Paragraph({
          children: [new TextRun({ text: "Full technical detail — all SQL queries, the executed analysis notebook, and an interactive dashboard — accompanies this summary.", italics: true, color: GREY, size: 18 })],
          spacing: { before: 300 },
        }),
      ],
    },
  ],
});

Packer.toBuffer(doc).then((buffer) => {
  fs.writeFileSync("/home/claude/ba_proj/reports/Executive_Summary.docx", buffer);
  console.log("Executive summary written.");
});
