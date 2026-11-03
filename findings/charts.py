"""Every chart in the project, drawn with bezel-charts (https://pypi.org/project/bezel-charts/).

Each function returns a chart, which shows up in a notebook and saves as an SVG.
"""

from __future__ import annotations

import pandas as pd

import bezel_charts as bc

try:
    from . import analysis as an
except ImportError:
    import analysis as an

# One look for the whole repo: light, frameless, on a warm off-white background
LOOK = {"theme": "light", "frame": "none", "corners": 12, "background": "#F7F6F2"}
WIDE = {**LOOK, "width": 680}
TILE = {**LOOK, "width": 330, "height": 190}

# Paul Tol's muted palette, readable with every common kind of colour blindness
INDIGO = "#332288"  # Main series, and groups that can't be told apart from all adults
ROSE = "#CC6677"    # Comparison series, and groups clearly above all adults
GREEN = "#117733"   # Groups clearly below all adults
CYAN = "#88CCEE"    # Confidence limits only, never text

COMPARED = {"higher": ROSE, "lower": GREEN, "similar": INDIGO}

SHORT = {
    "18 to 34": "18–34", "35 to 44": "35–44", "45 to 54": "45–54", "55 to 64": "55–64", "65+ years": "65+",
    "< $20,000": "<20k", "$20,000 - $34,999": "20–35k", "$35,000 - $49,999": "35–50k",
    "$50,000 - $74,999": "50–75k", "$75,000 - $99,999": "75–100k", "$100,000+": "100k+",
    "No High School Diploma": "No HS", "High School Graduate or GED Certificate": "HS/GED",
    "Some College or Tech School": "Some col.", "College Graduate or Post Grad": "Degree",
    "Asian/Pacific Islander": "Asian/PI",
}


def years(index) -> list[str]:
    return [str(year) for year in index]


def overall_trend():
    t = an.overall()
    return bc.line(
        values=[t["Percent"].tolist(), t["Upper 95% CL"].tolist(), t["Lower 95% CL"].tolist()],
        series=["Adults with depression", "Upper 95% limit", "Lower 95% limit"], labels=years(t.index),
        color=[INDIGO, CYAN, CYAN], heading="Adults ever told they have depression, % by year",
        suffix="%", decimals=1, height=220, zero=True, **WIDE,
    )


def survey_size():
    size = an.survey_size()
    return bc.bars(
        values=(size / 1000).round(1).tolist(), labels=years(size.index), suffix="k", decimals=1,
        color=[ROSE if year == 2017 else INDIGO for year in size.index], highlight="none",
        heading="People who answered the survey each year", stat="none", show_values=True, height=210, **WIDE,
    )


def year_changes():
    table = an.rows().pivot_table(index=["Strata", "Strata Name"], columns="Year", values="Percent").drop(index="Total")
    steps = table.diff(axis=1).mean().dropna().round(1)
    labels = [f"{year - 1}–{str(year)[2:]}" for year in steps.index]
    return bc.bars(
        values=steps.tolist(), labels=labels, color=[ROSE if year == 2017 else INDIGO for year in steps.index],
        highlight="none", heading="Average change across all 22 groups, percentage points",
        stat="none", show_values=True, decimals=1, height=210, **WIDE,
    )


def sex_gap():
    women, men = an.series("Sex", "Female"), an.series("Sex", "Male")
    return bc.line(
        values=[women.tolist(), men.tolist()], series=["Women", "Men"], labels=years(women.index),
        color=[ROSE, INDIGO], heading="Women and men ever told they have depression, %",
        suffix="%", decimals=1, height=220, zero=True, **WIDE,
    )


def margins():
    table = an.margins_by_age().round(1)
    table.index = [SHORT[name] for name in table.index]
    return bc.bars(
        table, heading="Margin of error by age group, ± percentage points",
        stat="none", show_values=True, decimals=1, height=210, color=[ROSE, INDIGO], **WIDE,
    )


# The 2×2 grid of tiles -----------------------------------------------------------------------------

def tile(strata: str, heading: str):
    t = an.pooled_group(strata)
    return bc.bars(
        values=t["percent"].round(1).tolist(), labels=[SHORT.get(name, name) for name in t.index],
        color=[COMPARED[c] for c in t["compared"]], highlight="none",
        heading=f"{heading} · all adults {an.everyone_pooled():.1f}%", stat="none", show_values=True,
        suffix="%", decimals=1, **TILE,
    )


def tile_age():
    return tile("Age", "By age")


def tile_income():
    return tile("Income", "By income, $")


def tile_education():
    return tile("Education", "By education")


def tile_race():
    return tile("Race-Ethnicity", "By race/ethnicity")


ALL = {
    "overall-trend": overall_trend,
    "survey-size": survey_size,
    "year-changes": year_changes,
    "sex-gap": sex_gap,
    "margins": margins,
    "tile-age": tile_age,
    "tile-income": tile_income,
    "tile-education": tile_education,
    "tile-race": tile_race,
}
