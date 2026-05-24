---
name: data-viz-storytelling-healy
description: >
  Chọn đúng biểu đồ, kể chuyện với số liệu, và tránh误导 — dựa trên nguyên tắc
  từ Kieran Healy (Data Visualization, Princeton 2019) và taxonomy từ AntV
  chart-visualization-skills. Dùng khi cần quyết định loại chart, trình bày insight
  cho stakeholder, hoặc kiểm tra xem figure có gây hiểu lầm không. Để vẽ Python
  thực tế, chuyển sang matplotlib / seaborn / scientific-visualization.
metadata:
  skill-author: Cake DS team
  sources:
    - name: "Kieran Healy, Data Visualization: A Practical Introduction (Princeton, 2019)"
      url: https://press.princeton.edu/books/ebook/9780691185064/data-visualization-pdf
    - name: "AntV chart-visualization-skills (MIT)"
      url: https://github.com/antvis/chart-visualization-skills
---

# Data Visualization & Storytelling (Healy + AntV)

> "The tools you use can help you live up to the right standards.
> But they cannot make you do the right thing."
> — Kieran Healy, *Data Visualization*, Ch. 1

## When to Use This Skill

- Deciding **which chart type** fits the analytical question
- Writing a report or slide deck where **numbers need a narrative**
- Reviewing a figure for **honesty / misleading patterns**
- Drafting an insight summary with **claim → evidence → caveat** structure
- Choosing between infographic (visual design) and statistical figure (accuracy)

**For actual plotting code** → use `matplotlib`, `seaborn`, or `scientific-visualization`.

---

## Section 1 — Honesty & Judgment (Healy Ch. 1)

Before choosing colors or chart types, verify the figure does not mislead.

### 1.1 Pre-plot Honesty Checklist

| Check | Why it matters |
|-------|----------------|
| Baseline / zero start | Bar charts starting above zero exaggerate differences. Line charts may omit zero legitimately if the focus is trend, not level. |
| Dual axes | Two Y-axes on one plot invite false correlation. Prefer faceted panels or indexed series. |
| Cherry-picked window | Short time windows can hide long-term patterns. Always show context. |
| Aggregation level | Averages can hide distribution shape. Consider showing raw data, box plots, or density. |
| Proportional vs absolute | Normalize when comparing groups of different size; keep raw counts available. |
| Color encoding | Do not use rainbow/palette that implies order for categorical data. Use colorblind-safe palettes. |
| Uncertainty | Show CI, prediction bands, or error bars when presenting estimates. |
| Axis labels & units | Every axis must state what it measures and in what unit. |

**Rule of thumb:** If removing context (time range, N, CI) changes the takeaway, the figure is misleading as-is.

### 1.2 Perception Principles (Healy Ch. 1 + Cleveland)

Humans perceive some encodings more accurately than others:

1. **Position on common scale** — most accurate (scatter, line)
2. **Position on different scale** — good (grouped bar, faceted)
3. **Length / direction** — moderate
4. **Angle / area** — poor (avoid pie charts for comparison)
5. **Color intensity / shape** — worst for magnitude; OK for categories

**Implication:** Prefer dot plots or bar charts over pie/bubble for quantitative comparison.

---

## Section 2 — Chart Selection Rubric (AntV taxonomy → Python)

Ask: **"What is the analytical question?"** then pick the chart family.

| Question family | Chart types | Python (seaborn/matplotlib) |
|-----------------|-------------|-----------------------------|
| **Trend over time** | Line, area, step | `sns.lineplot`, `ax.plot`, `ax.fill_between` |
| **Comparison (categories)** | Bar (grouped/stacked), lollipop | `sns.barplot`, `ax.barh` |
| **Part-to-whole** | Stacked bar, waffle, pie (sparingly) | `ax.bar(stacked)`, avoid pie for >3 slices |
| **Distribution** | Histogram, KDE, box, violin, ridgeline | `sns.histplot`, `sns.kdeplot`, `sns.boxplot`, `sns.violinplot` |
| **Relationship (2+ vars)** | Scatter, bubble, hexbin, 2D density | `sns.scatterplot`, `ax.hexbin`, `sns.jointplot` |
| **Ranking** | Lollipop, horizontal bar (sorted) | `ax.barh` (sorted) |
| **Deviation / contrast** | Diverging bar, slope chart, dumbbell | Custom `ax.barh` with center baseline |
| **Geography** | Choropleth, bubble map | `geopandas` + matplotlib; or Folium |
| **Hierarchy / flow** | Treemap, sankey, dendrogram | `squarify`, `matplotlib-sankey` |
| **Multi-variate summary** | Parallel coordinates, radar, heatmap | `pd.plotting.parallel_coordinates`, `sns.heatmap` |
| **Model diagnostics** | Residual plot, calibration curve, lift/gains | `sns.residplot`, custom calibration, KS plot |

### Decision Flow

```
1. How many variables?  → 1 (distribution) | 2 (relationship) | 3+ (multivariate)
2. Is there a time component?  → Yes: line/area trend
3. Am I comparing groups?  → Yes: bar/lollipop
4. Am I showing composition?  → Yes: stacked bar > pie
5. Am I showing uncertainty?  → Always add CI/bands
6. Audience?  → Expert: detail plot | Executive: annotated summary + callout
```

---

## Section 3 — Building Plots Layer by Layer (Healy Ch. 3)

Healy teaches the **grammar of graphics**: data → mapping → geom → stat → coord → facet → theme.

Mapped to matplotlib/seaborn:

| Grammar layer | ggplot concept | matplotlib / seaborn equivalent |
|---------------|----------------|--------------------------------|
| Data | `ggplot(df)` | Pass DataFrame to seaborn or plot columns |
| Aesthetic mapping | `aes(x=, y=, color=)` | `x=`, `y=`, `hue=` params in seaborn; manual in matplotlib |
| Geometry | `geom_point`, `geom_line` | `ax.scatter`, `ax.plot`, `sns.scatterplot` |
| Statistical transform | `stat_summary`, `geom_smooth` | `sns.regplot`, `sns.aggplot`-like via groupby + plot |
| Coordinate system | `coord_flip`, `coord_polar` | `ax.invert_yaxis()`, projection='polar' |
| Facet | `facet_wrap(~var)` | `sns.FacetGrid` / `sns.relplot(col=)` |
| Theme / labels | `labs()`, `theme_minimal()` | `ax.set_title/labels`, spine removal, style sheets |

**Workflow in Python:**

```python
import seaborn as sns
import matplotlib.pyplot as plt

# Layer 1: data + mapping + geom
g = sns.relplot(
    data=df,
    x="feature_date", y="default_rate",
    hue="segment", col="product",
    kind="line", facet_kws={"sharey": False}
)

# Layer 2: annotation
g.fig.suptitle("Default Rate Trend by Segment & Product", y=1.02)
g.set_axis_labels("Month", "Default Rate (%)")

# Layer 3: refine
g.tick_params(axis="x", rotation=45)
sns.despine()
plt.tight_layout()
```

---

## Section 4 — Narrative with Numbers (AntV T8 + Report Pattern)

When writing a data-driven section (report, slide, notebook conclusion), follow:

### 4.1 Claim-Evidence-Caveat Pattern

```
**Claim:** "Approval rate for Segment A dropped 15 pp in Q3."

**Evidence:**
  - Figure: Line chart of monthly approval rate, Segments A/B/C, Jan–Sep
  - Table: N, mean, CI per segment per quarter

**Caveat:**
  - "Data window excludes Jan policy change; Segment C sample < 500."
```

### 4.2 Entity Annotation (T8-inspired)

In markdown, annotate key entities so readers (and agents) can parse them:

```markdown
The [metric:approval_rate] for [dimension:Segment_A] was [value:72%] ([trend:down_15pp])
in [dimension:Q3_2026], compared to [value:87%] in [dimension:Q2_2026].
```

This mirrors AntV T8's entity-based narrative but works in plain markdown.

### 4.3 Figure Caption Template (Healy Ch. 5)

A good caption has:

1. **What** is being shown (chart type + variables)
2. **Who/when** (cohort, time window, N)
3. **Key takeaway** (one sentence)
4. **Caveat** (if any)

Example:
> Figure 3. Monthly default rate (%) by risk tier, Jan 2025 – Sep 2026 (N = 142,000). Tier D shows the steepest increase after the Q2 policy change. 95% CI shown in shading.

---

## Section 5 — Model → Visualization (Healy Ch. 6, Credit Scoring context)

Common model diagnostic plots for credit scoring:

| Diagnostic | Chart | Purpose |
|------------|-------|---------|
| Residual analysis | Residual vs predicted, Q-Q plot | Check model assumptions |
| Feature effect | Partial dependence / ICE | Direction & magnitude of top features |
| Discrimination | KS plot, ROC curve, PR curve | Rank-ordering ability |
| Calibration | Calibration curve (predicted vs actual) | Score reliability |
| Stability | PSI over time, population distribution shift | Feature / score drift |
| Segmentation | Slice metrics (Gini by segment, approval rate by tier) | Fairness & performance parity |
| SHAP | Beeswarm, waterfall, scatter | Explainability (see `shap` skill) |

---

## Section 6 — Refinement Quick Reference

For detailed publication styling → `scientific-visualization`.

| Aspect | Guideline |
|--------|-----------|
| Color palette | Use colorblind-safe (viridis, Okabe-Ito). Avoid rainbow for sequential data. |
| Grayscale test | Figure should still be readable in black & white. |
| Font size | Minimum 6 pt at final print size; larger for presentations. |
| Spines | Remove top & right spines for cleaner look. |
| Grid lines | Use light, sparse gridlines; avoid heavy grid. |
| Legends | Place near data; consider direct labels instead. |
| Aspect ratio | Choose so perception is not distorted (banking to 45° for trends). |
| File format | PDF/SVG for vector; PNG at 300+ DPI for raster. |

---

## Section 7 — Infographic vs Statistical Figure

| Dimension | Infographic (`infographics` skill) | Statistical Figure (this + `scientific-visualization`) |
|-----------|------------------------------------|--------------------------------------------------------|
| Primary goal | Communicate key message visually | Show data accurately & completely |
| Audience | General / executive / marketing | Analysts, reviewers, risk committee |
| Data density | Low-moderate (curated highlights) | High (full distribution, uncertainty) |
| Aesthetics | Template-driven, branded | Clean, minimal chart junk |
| Tool | Nano Banana Pro / design tools | matplotlib / seaborn / plotly |

**Choose infographic when:** one key message, non-technical audience, visual impact matters.
**Choose statistical figure when:** accuracy, reproducibility, peer review required.

---

## References

- Healy, K. (2019). *Data Visualization: A Practical Introduction*. Princeton University Press.
- AntV chart-visualization-skills: https://github.com/antvis/chart-visualization-skills (MIT)
- Cleveland, W. S. & McGill, R. (1984). "Graphical Perception: Theory, Experimentation, and Application to the Development of Graphical Methods." *JASA*.
- Tufte, E. R. (2001). *The Visual Display of Quantitative Information*. Graphics Press.
