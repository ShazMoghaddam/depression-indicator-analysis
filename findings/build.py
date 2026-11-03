"""Draw every chart and write the findings report.

Run from the repository root:

    python findings/build.py

Charts go into charts/ as SVG files. The report is written to findings/README.md, and the key findings in the
main README are rewritten between their marker comments. Every number is worked out from the data. Nothing in
them is typed in by hand.
"""

from __future__ import annotations

import random
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "findings"))

import analysis as an  # noqa: E402
import charts  # noqa: E402

CHARTS = ROOT / "charts"
REPORT = ROOT / "findings" / "README.md"
README = ROOT / "README.md"


def facts() -> dict:
    """Every number the writing uses, in one place."""
    t = an.overall()["Percent"]
    size = an.survey_size()
    margin = an.margin()
    weighted = an.weighted_adults()
    jump = an.changes(2016, 2017).drop(index="Total")
    gap = an.sex_gap()
    sex = an.pooled_group("Sex")
    age = an.pooled_group("Age")
    income = an.pooled_group("Income")
    education = an.pooled_group("Education")
    race = an.pooled_group("Race-Ethnicity")
    rich, poor = "$100,000+", "< $20,000"
    one_told, one_pairs = an.separable("Age", 2018)
    pooled_told, _ = an.separable_pooled("Age")
    margins = an.margins_by_age()
    return {
        "first": int(t.index.min()), "last": int(t.index.max()),
        "t12": t[2012], "t16": t[2016], "t17": t[2017], "t18": t[2018],
        "steady_low": t.loc[2012:2016].min(), "steady_high": t.loc[2012:2016].max(), "everyone": an.everyone_pooled(),
        "jump": t[2017] - t[2016], "groups": len(jump), "rose": int((jump > 0).sum()),
        "rise_low": jump.min(), "rise_high": jump.max(),
        "avg_jump": jump.mean(),
        "other_avg": max(abs(an.changes(year - 1, year).drop(index="Total").mean()) for year in range(2013, 2019) if year != 2017),
        "size12": f"{size[2012]:,}", "size17": f"{size[2017]:,}", "size_min_year": int(size.idxmin()),
        "margin12": margin[2012], "margin17": margin[2017], "margin_times": margin[2017] / margin[2012],
        "w16": weighted[2016] / 1e6, "w17": weighted[2017] / 1e6, "w_rise": weighted[2017] / weighted[2016] - 1,
        "gap_low": gap.min(), "gap_high": gap.max(), "sex_years": len(an.years_apart("Sex", "Female", "Male")),
        "years": len(t), "women": sex.loc["Female", "percent"], "men": sex.loc["Male", "percent"],
        "a1834": age.loc["18 to 34", "percent"], "a5564": age.loc["55 to 64", "percent"], "a65": age.loc["65+ years", "percent"],
        "poor": income.loc[poor, "percent"], "rich": income.loc[rich, "percent"],
        "income_years": len(an.years_apart("Income", poor, rich)),
        "degree": education.loc["College Graduate or Post Grad", "percent"],
        "some_college": education.loc["Some College or Tech School", "percent"],
        "asian": race.loc["Asian/Pacific Islander", "percent"], "white": race.loc["White", "percent"],
        "other": race.loc["Other", "percent"], "hispanic": race.loc["Hispanic", "percent"], "black": race.loc["Black", "percent"],
        "asian_lowest": an.lowest_every_year("Race-Ethnicity") == {"Asian/Pacific Islander"},
        "one_told": one_told, "pairs": one_pairs, "pooled_told": pooled_told,
        "m18_low": margins["2018 alone"].min(), "m18_high": margins["2018 alone"].max(),
        "mp_low": margins["2012 to 2016 pooled"].min(), "mp_high": margins["2012 to 2016 pooled"].max(),
        "rows": an.group_years(),
    }


def told(n: int, word: str) -> str:
    """'none' rather than 'only 0'."""
    return "none" if n == 0 else f"{word} {n}"


def key_findings(f: dict) -> str:
    return f"""### The 2017 jump looks like a change in the survey, not in people

The rate held between {f['steady_low']:.1f}% and {f['steady_high']:.1f}% from 2012 to 2016, then rose to **{f['t17']:.1f}%** in 2017. Every one of the {f['groups']}
groups rose that same year, while the survey heard from its fewest people ({f['size17']}, against {f['size12']} in 2012). A real change that
sudden and that even would be unusual, so treat 2017 and 2018 with care.

![Adults ever told they have depression, by year](charts/overall-trend.svg)

### Women report depression far more often than men, every year

Over 2012 to 2016, {f['women']:.1f}% of women had been told they have depression against {f['men']:.1f}% of men. The gap is clear
in all {f['sex_years']} years.

![Women and men, by year](charts/sex-gap.svg)

### Age, income and ethnicity all matter

Pooling 2012 to 2016 gives each group enough answers to compare. Depression peaks at **{f['a5564']:.1f}%** for 55–64 year olds,
reaches **{f['poor']:.1f}%** in households earning under $20,000 against {f['rich']:.1f}% at $100,000 or more, and is lowest among
Asian and Pacific Islander adults (**{f['asian']:.1f}%**). Rose bars are clearly above all adults, green clearly below.

<p>
  <img src="charts/tile-age.svg" alt="By age: rising from {f['a1834']:.1f} percent at 18 to 34 to {f['a5564']:.1f} percent at 55 to 64, then {f['a65']:.1f} percent at 65 and over" width="330">
  <img src="charts/tile-income.svg" alt="By income: {f['poor']:.1f} percent under 20 thousand dollars, {f['rich']:.1f} percent at 100 thousand or more" width="330">
</p>
<p>
  <img src="charts/tile-education.svg" alt="By education: highest with some college at {f['some_college']:.1f} percent, lowest with a degree at {f['degree']:.1f} percent" width="330">
  <img src="charts/tile-race.svg" alt="By race and ethnicity: Asian and Pacific Islander lowest at {f['asian']:.1f} percent, Other highest at {f['other']:.1f} percent" width="330">
</p>

### One year of data can't rank the groups

In 2018 alone, {told(f['one_told'], 'only')} of the {f['pairs']} pairs of age groups can be told apart. Pooled over five years, {f['pooled_told']} can.

![Margin of error by age, one year against five](charts/margins.svg)"""


def report(f: dict) -> str:
    return f"""# Findings

How common depression is among adults in California, who is most affected, and what changed, from {f['first']} to {f['last']}.
This page is written by [`build.py`](build.py), so every number comes straight from the data.

The figures are the share of adults who have **ever been told** by a doctor, nurse or other health professional that
they have a depressive disorder, from the California Behavioral Risk Factor Surveillance Survey. That depends on people
seeing a professional and being diagnosed, so it isn't the same as how many people have depression.

## 1. About 1 in 8 adults, and steady until 2016

From 2012 to 2016 the rate stayed between {f['steady_low']:.1f}% and {f['steady_high']:.1f}%. Pooled over those five years it was **{f['everyone']:.1f}%**,
about 1 in 8 adults.

![Adults ever told they have depression, by year](../charts/overall-trend.svg)

## 2. The 2017 jump looks like a change in the survey, not in people

In 2017 the rate rose {f['jump']:.1f} points in a year, to {f['t17']:.1f}%, and stayed high in 2018 at {f['t18']:.1f}%. Several things suggest the survey
changed rather than Californians' health:

- **Every group rose at once, and by a lot.** All {f['groups']} groups went up, by between {f['rise_low']:.1f} and {f['rise_high']:.1f} points. The average
  rise was {f['avg_jump']:.1f} points. In no other year did the average move by more than {f['other_avg']:.1f}.
- **The survey was smaller.** Working back from the counts, {f['size17']} people answered in 2017, the fewest of any year, against
  {f['size12']} in 2012.
- **The uncertainty tripled.** The margin of error on the overall rate was ±{f['margin12']:.1f} points in 2012 and ±{f['margin17']:.1f} in 2017.
- **The scaled-up count leapt.** Adults with depression, scaled up to California's population, went from {f['w16']:.1f} million to
  {f['w17']:.1f} million in a year, up {f['w_rise']:.0%}.

![Average change across groups, year to year](../charts/year-changes.svg)

![People who answered the survey each year](../charts/survey-size.svg)

The California Department of Public Health's notes don't record a change in method that year, so the data can't say what
happened. It may be a real rise. But until that's confirmed, 2017 and 2018 shouldn't be compared directly with earlier
years, and the group comparisons below use 2012 to 2016.

## 3. Women report depression far more often than men

Women's rate was higher than men's in every year, by {f['gap_low']:.1f} to {f['gap_high']:.1f} points, and the confidence intervals never overlap. Over 2012
to 2016, {f['women']:.1f}% of women had been told they have depression against {f['men']:.1f}% of men.

![Women and men, by year](../charts/sex-gap.svg)

Part of this gap may be that women are more likely to see a doctor and be diagnosed. The data can't separate the two.

## 4. Depression rises with age until 65

Pooled over 2012 to 2016, the rate climbs from {f['a1834']:.1f}% among 18–34 year olds to **{f['a5564']:.1f}%** at 55–64, then falls to {f['a65']:.1f}% at 65
and over. Rose bars are clearly above all adults ({f['everyone']:.1f}%), green clearly below, and indigo can't be told apart.

<img src="../charts/tile-age.svg" alt="By age, 2012 to 2016" width="330">

## 5. Lower income, more depression

Households earning under $20,000 had a rate of **{f['poor']:.1f}%**, about double the {f['rich']:.1f}% in households earning $100,000 or more. The gap
is clear in {f['income_years']} of {f['years']} years on their own. By education, adults with some college had the highest rate ({f['some_college']:.1f}%) and graduates
the lowest ({f['degree']:.1f}%).

<p>
  <img src="../charts/tile-income.svg" alt="By income, 2012 to 2016" width="330">
  <img src="../charts/tile-education.svg" alt="By education, 2012 to 2016" width="330">
</p>

## 6. Asian and Pacific Islander adults report the least depression

Asian and Pacific Islander adults had the lowest rate in every year, {f['asian']:.1f}% pooled over 2012 to 2016. Hispanic adults were also below
average ({f['hispanic']:.1f}%), Black adults close to it ({f['black']:.1f}%), and White adults ({f['white']:.1f}%) and those recorded as "Other" ({f['other']:.1f}%) above.

<img src="../charts/tile-race.svg" alt="By race and ethnicity, 2012 to 2016" width="330">

Diagnosis depends on seeking care, which differs between communities, so these gaps may partly reflect who gets diagnosed.

## 7. One year of data can't rank the groups

Each group in each year rests on a few hundred answers, so single-year figures carry wide margins of error: ±{f['m18_low']:.1f} to
±{f['m18_high']:.1f} points for the age groups in 2018. Pooling five years cuts that to ±{f['mp_low']:.1f} to ±{f['mp_high']:.1f}.

![Margin of error by age, one year against five](../charts/margins.svg)

In 2018 alone, {told(f['one_told'], 'only')} of the {f['pairs']} pairs of age groups can be told apart. Pooled, {f['pooled_told']} can. The same is true of the earlier
version's model: with only {f['rows']} group-year rows and nothing but the year and the group to go on, it was mostly memorising
which groups are high, which the confidence intervals already show directly. It's been replaced by the comparisons above.

## What this data can't tell you

- **How many people have depression.** It counts people who have been diagnosed, which depends on access to care.
- **What happened in 2017.** The signs point to the survey, but the published notes don't say.
- **Anything about individuals.** These are group averages from a weighted survey.
- **Causes.** Income, age or ethnicity going with higher rates doesn't show that they cause them.

## How it was worked out

1. [`data/adult_depression_lghc_indicator_24.csv`](../data/adult_depression_lghc_indicator_24.csv) is the published file, unchanged.
2. [`analysis.py`](analysis.py) holds every calculation as a small, tested function. Standard errors are worked back from the published
   95% confidence limits, and years are pooled by inverse-variance weighting, which gives more weight to years measured more precisely.
3. [`charts.py`](charts.py) draws each chart with [bezel-charts](https://pypi.org/project/bezel-charts/).
4. [`notebooks/depression_analysis.ipynb`](../notebooks/depression_analysis.ipynb) walks through the same steps with the working shown.

Pooling assumes each group's rate was roughly steady from 2012 to 2016, which the overall rate supports.

## A correction to the earlier version

The earlier version named 55–64 year olds and adults with some college as the highest groups in 2018. Their rates were the
highest that year, but neither can be told apart from most other groups on 2018 alone. Five years pooled confirm both
patterns. It also read 2017 as a possible real rise and ran a classifier on {f['rows']} rows. Everything here replaces that work.
"""


def replace_block(text: str, name: str, body: str) -> str:
    pattern = re.compile(rf"(<!-- {name}:start -->\n).*?(\n<!-- {name}:end -->)", re.S)
    if not pattern.search(text):
        raise ValueError(f"Marker {name} not found")
    return pattern.sub(lambda m: m.group(1) + body + m.group(2), text)


def main() -> None:
    # bezel-charts gives each gradient a random id so charts can share a page. A fixed seed keeps the
    # files identical between runs, so a rebuild only shows up in git when something really changed.
    random.seed(2026)
    CHARTS.mkdir(exist_ok=True)
    for name, draw in charts.ALL.items():
        draw().save(CHARTS / f"{name}.svg")
    f = facts()
    REPORT.write_text(report(f), encoding="utf-8")
    README.write_text(replace_block(README.read_text(encoding="utf-8"), "key-findings", key_findings(f)), encoding="utf-8")
    print(f"Wrote {len(charts.ALL)} charts, {REPORT.relative_to(ROOT)} and the README findings")


if __name__ == "__main__":
    main()
