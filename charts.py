"""Charts for the Adult Depression Indicator Analysis, drawn with Bezel Charts.

Every chart shares one look: light, frameless, warm off-white background and
Paul Tol's colour-blind-safe "muted" palette.
"""

from pathlib import Path

import bezel_charts as bz
import pandas as pd

INDIGO = "#332288"  # main series
ROSE = "#CC6677"    # comparison group
GREEN = "#117733"   # second model / extra series
CYAN = "#88CCEE"    # confidence limits only, never text

STYLE = dict(theme="light", frame="none", corners=12, background="#F7F6F2")
WIDE = 680
TILE = 330

OUT = Path("charts")

# Short labels so the tiles stay readable.
SHORT = {
    "< $20,000": "Under $20k",
    "$20,000 - $34,999": "$20k–35k",
    "$35,000 - $49,999": "$35k–50k",
    "$50,000 - $74,999": "$50k–75k",
    "$75,000 - $99,999": "$75k–100k",
    "$100,000+": "$100k+",
    "No High School Diploma": "No diploma",
    "High School Graduate or GED Certificate": "High school / GED",
    "Some College or Tech School": "Some college",
    "College Graduate or Post Grad": "Degree or higher",
    "Asian/Pacific Islander": "Asian / Pac. Isl.",
    "65+ years": "65+",
}


def _save(chart, name):
    OUT.mkdir(exist_ok=True)
    chart.save(OUT / f"{name}.svg")
    return chart


def overall_trend(df):
    """Share of adults with depression each year, with its 95% confidence limits."""
    t = df[df["Strata"] == "Total"].sort_values("Year")
    chart = bz.line(
        values=[t["Percent"].tolist(), t["Upper 95% CL"].tolist(), t["Lower 95% CL"].tolist()],
        series=["Adults with depression", "Upper 95% limit", "Lower 95% limit"],
        labels=t["Year"].astype(str).tolist(),
        color=[INDIGO, CYAN, CYAN],
        heading="Adults with depression, % by year",
        suffix="%", decimals=1, stat="last", delta="inverse", delta_label="pts since 2012", width=WIDE, height=220, **STYLE,
    )
    return _save(chart, "overall_trend")


def sex_gap(df):
    """Women and men side by side over time."""
    s = df[df["Strata"] == "Sex"].pivot(index="Year", columns="Strata Name", values="Percent")
    chart = bz.line(
        values=[s["Female"].tolist(), s["Male"].tolist()],
        series=["Women", "Men"],
        labels=s.index.astype(str).tolist(),
        color=[ROSE, INDIGO],
        heading="Women vs men, % with depression",
        suffix="%", decimals=1, width=WIDE, height=220, **STYLE,
    )
    return _save(chart, "sex_gap")


def group_tile(df, strata, heading, order=None, year=2018):
    """Horizontal bars for one breakdown in one year; the highest group is shown at full strength."""
    g = df[(df["Strata"] == strata) & (df["Year"] == year)].set_index("Strata Name")["Percent"]
    g = g.reindex(order) if order else g.sort_values(ascending=False)
    chart = bz.bars(
        values=g.round(1).tolist(),
        labels=[SHORT.get(n, n) for n in g.index],
        color=INDIGO, horizontal=True, show_values=True,
        heading=f"{heading}, {year}",
        suffix="%", decimals=1, width=TILE, **STYLE,
    )
    return _save(chart, f"tile_{strata.lower().replace('-', '_')}")


def model_comparison(scores):
    """Test-set scores for each model, side by side. `scores` is a DataFrame: rows = models, columns = metrics."""
    chart = bz.bars(
        values=[scores.loc[m].round(2).tolist() for m in scores.index],
        series=scores.index.tolist(),
        labels=scores.columns.tolist(),
        color=[INDIGO, GREEN],
        heading="Model scores on the test set (1 = perfect)",
        decimals=2, show_values=True, width=WIDE, height=200, **STYLE,
    )
    return _save(chart, "model_comparison")


def all_tiles(df):
    return [
        group_tile(df, "Age", "By age", ["18 to 34", "35 to 44", "45 to 54", "55 to 64", "65+ years"]),
        group_tile(df, "Income", "By household income", [
            "< $20,000", "$20,000 - $34,999", "$35,000 - $49,999",
            "$50,000 - $74,999", "$75,000 - $99,999", "$100,000+",
        ]),
        group_tile(df, "Education", "By education", [
            "No High School Diploma", "High School Graduate or GED Certificate",
            "Some College or Tech School", "College Graduate or Post Grad",
        ]),
        group_tile(df, "Race-Ethnicity", "By race / ethnicity"),
    ]


if __name__ == "__main__":
    data = pd.read_csv("adult-depression-lghc-indicator-24.csv")
    overall_trend(data)
    sex_gap(data)
    all_tiles(data)
