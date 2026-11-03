"""Checks that the data is sound and the findings hold up. Run from the repository root with `pytest`."""

import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "findings"))

import analysis as an  # noqa: E402
import build  # noqa: E402
import charts  # noqa: E402


def test_file_has_every_group_and_year():
    rows = an.rows()
    assert len(rows) == 161
    assert sorted(rows["Year"].unique()) == list(range(2012, 2019))
    assert (rows.groupby("Year").size() == 23).all()


def test_confidence_limits_are_symmetric_and_contain_the_rate():
    rows = an.rows()
    assert ((rows["Lower 95% CL"] <= rows["Percent"]) & (rows["Percent"] <= rows["Upper 95% CL"])).all()
    centre = (rows["Lower 95% CL"] + rows["Upper 95% CL"]) / 2
    assert (centre - rows["Percent"]).abs().max() < 0.01


def test_every_breakdown_covers_the_same_adults_each_year():
    # Sex and age each split everyone, so their scaled-up counts agree to within rounding
    totals = an.rows()[an.rows()["Strata"].isin(["Sex", "Age"])].groupby(["Year", "Strata"])["Weighted Frequency"].sum().unstack()
    assert ((totals["Sex"] - totals["Age"]).abs() <= 1).all()


def test_pooling_a_single_year_returns_it_unchanged():
    one = an.rows()[(an.rows()["Strata"] == "Total") & (an.rows()["Year"] == 2012)]
    pooled = an.pool(one)
    assert pooled["percent"] == pytest.approx(one["Percent"].iloc[0])
    assert pooled["low"] == pytest.approx(one["Lower 95% CL"].iloc[0], abs=0.01)


def test_pooling_narrows_the_interval():
    pooled = an.pooled().loc[("Total", "Total")]
    assert pooled["high"] - pooled["low"] < an.margin().loc[2012:2016].min() * 2


def test_2017_stands_out():
    assert (an.changes(2016, 2017).drop(index="Total") > 0).all()
    assert an.survey_size().idxmin() == 2017
    assert an.margin()[2017] > 2.5 * an.margin()[2012]


def test_women_above_men_every_year():
    assert an.years_apart("Sex", "Female", "Male") == list(range(2012, 2019))


def test_age_peaks_at_55_to_64():
    assert an.pooled_group("Age")["percent"].idxmax() == "55 to 64"


def test_lowest_income_is_about_double_the_highest():
    income = an.pooled_group("Income")["percent"]
    assert 1.7 < income["< $20,000"] / income["$100,000+"] < 2.3


def test_asian_and_pacific_islander_adults_lowest_every_year():
    assert an.lowest_every_year("Race-Ethnicity") == {"Asian/Pacific Islander"}


def test_one_year_cannot_rank_age_groups_but_five_can():
    assert an.separable("Age", 2018)[0] < an.separable_pooled("Age")[0]


def test_every_chart_draws_in_the_house_style():
    for name, draw in charts.ALL.items():
        svg = draw()._repr_svg_()
        assert "#F7F6F2" in svg, name
        width = 330 if name.startswith("tile-") else 680
        assert f'width="{width}"' in svg, name


def test_tiles_match_and_show_every_label():
    heights = set()
    for name, draw in charts.ALL.items():
        if not name.startswith("tile-"):
            continue
        svg = draw()._repr_svg_()
        heights.add(re.search(r'height="(\d+)"', svg).group(1))
        strata = {"tile-age": "Age", "tile-income": "Income", "tile-education": "Education", "tile-race": "Race-Ethnicity"}[name]
        for label in an.ORDER[strata]:
            shown = charts.SHORT.get(label, label).replace("<", "&lt;")
            assert f">{shown}<" in svg, (name, label)
    assert len(heights) == 1


def test_report_has_no_unfilled_placeholders():
    f = build.facts()
    text = build.report(f) + build.key_findings(f)
    assert not re.search(r"\{[a-z_]+\}|\bnan\b|only 0", text)


def test_readme_links_to_charts_that_exist():
    readme = (ROOT / "README.md").read_text(encoding="utf-8") + (ROOT / "findings" / "README.md").read_text(encoding="utf-8")
    for path in re.findall(r"charts/([a-z-]+\.svg)", readme):
        assert (ROOT / "charts" / path).exists(), path
