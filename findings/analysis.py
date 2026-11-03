"""Every calculation in the project, as small functions that read data/adult_depression_lghc_indicator_24.csv.

Each function returns plain pandas objects or numbers, so the charts, the report, the notebook and the tests all
share one version of every figure.
"""

from __future__ import annotations

from functools import cache
from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "data"

STEADY = range(2012, 2017)  # The five years before the 2017 jump, pooled for group comparisons
Z = 1.96  # 95% confidence

ORDER = {
    "Age": ["18 to 34", "35 to 44", "45 to 54", "55 to 64", "65+ years"],
    "Income": ["< $20,000", "$20,000 - $34,999", "$35,000 - $49,999", "$50,000 - $74,999", "$75,000 - $99,999", "$100,000+"],
    "Education": [
        "No High School Diploma", "High School Graduate or GED Certificate", "Some College or Tech School",
        "College Graduate or Post Grad",
    ],
    "Race-Ethnicity": ["Asian/Pacific Islander", "Hispanic", "Black", "White", "Other"],
    "Sex": ["Male", "Female"],
}


@cache
def rows() -> pd.DataFrame:
    """Every group in every year, with a standard error worked back from its 95% confidence limits."""
    df = pd.read_csv(DATA / "adult_depression_lghc_indicator_24.csv")
    df["se"] = (df["Upper 95% CL"] - df["Lower 95% CL"]) / (2 * Z)
    return df


def group(strata: str) -> pd.DataFrame:
    return rows()[rows()["Strata"] == strata]


def series(strata: str, name: str, column: str = "Percent") -> pd.Series:
    g = group(strata)
    return g[g["Strata Name"] == name].set_index("Year")[column]


# 1. The overall rate -----------------------------------------------------------------------------

def overall() -> pd.DataFrame:
    return group("Total").set_index("Year")[["Percent", "Lower 95% CL", "Upper 95% CL"]]


# 2. The 2017 jump --------------------------------------------------------------------------------

def survey_size() -> pd.Series:
    """People who answered each year, worked back from the depression count and the rate. Unweighted."""
    total = group("Total").set_index("Year")
    return (total["Frequency"] / (total["Percent"] / 100)).round().astype(int)


def margin() -> pd.Series:
    """Half the width of the all-adults 95% confidence interval, in percentage points."""
    t = overall()
    return (t["Upper 95% CL"] - t["Lower 95% CL"]) / 2


def weighted_adults() -> pd.Series:
    """Adults with depression, scaled up to California's population, from the sex rows (which cover everyone)."""
    return group("Sex").groupby("Year")["Weighted Frequency"].sum()


def changes(start: int, end: int) -> pd.Series:
    """Change in percentage points for every group, including the total, between two years."""
    table = rows().pivot_table(index=["Strata", "Strata Name"], columns="Year", values="Percent")
    return table[end] - table[start]


# 3 to 6. Group comparisons -----------------------------------------------------------------------

def pool(frame: pd.DataFrame) -> pd.Series:
    """Combine several years into one estimate, giving more weight to years measured more precisely."""
    weight = 1 / frame["se"] ** 2
    estimate = (frame["Percent"] * weight).sum() / weight.sum()
    se = np.sqrt(1 / weight.sum())
    return pd.Series({"percent": estimate, "low": estimate - Z * se, "high": estimate + Z * se})


@cache
def pooled() -> pd.DataFrame:
    """Every group's rate over 2012 to 2016, and whether it's clearly above or below all adults."""
    steady = rows()[rows()["Year"].isin(STEADY)]
    table = pd.DataFrame({key: pool(frame) for key, frame in steady.groupby(["Strata", "Strata Name"])}).T
    everyone = table.loc[("Total", "Total"), "percent"]
    table["compared"] = np.where(table["low"] > everyone, "higher", np.where(table["high"] < everyone, "lower", "similar"))
    return table


def pooled_group(strata: str) -> pd.DataFrame:
    return pooled().loc[strata].reindex(ORDER[strata])


def everyone_pooled() -> float:
    return float(pooled().loc[("Total", "Total"), "percent"])


def apart(strata: str, high: str, low: str, year: int) -> bool:
    """True when two groups' 95% confidence intervals don't overlap in a year."""
    g = group(strata)
    g = g[g["Year"] == year].set_index("Strata Name")
    return bool(g.loc[high, "Lower 95% CL"] > g.loc[low, "Upper 95% CL"])


def years_apart(strata: str, high: str, low: str) -> list[int]:
    return [year for year in sorted(rows()["Year"].unique()) if apart(strata, high, low, year)]


def sex_gap() -> pd.Series:
    return series("Sex", "Female") - series("Sex", "Male")


def lowest_every_year(strata: str) -> set[str]:
    """The groups that were lowest in at least one year."""
    g = group(strata).pivot(index="Year", columns="Strata Name", values="Percent")
    return set(g.idxmin(axis=1))


# 7. One year can't rank groups -------------------------------------------------------------------

def separable(strata: str, year: int) -> tuple[int, int]:
    """How many pairs of groups can be told apart in one year, out of all pairs."""
    names = ORDER[strata]
    pairs = [(a, b) for i, a in enumerate(names) for b in names[i + 1:]]
    g = group(strata)
    g = g[g["Year"] == year].set_index("Strata Name")
    told = sum(
        g.loc[a, "Lower 95% CL"] > g.loc[b, "Upper 95% CL"] or g.loc[b, "Lower 95% CL"] > g.loc[a, "Upper 95% CL"]
        for a, b in pairs
    )
    return int(told), len(pairs)


def separable_pooled(strata: str) -> tuple[int, int]:
    names = ORDER[strata]
    pairs = [(a, b) for i, a in enumerate(names) for b in names[i + 1:]]
    t = pooled_group(strata)
    told = sum(t.loc[a, "low"] > t.loc[b, "high"] or t.loc[b, "low"] > t.loc[a, "high"] for a, b in pairs)
    return int(told), len(pairs)


def margins_by_age(year: int = 2018) -> pd.DataFrame:
    """Margin of error (± points) for each age group: one year alone against 2012 to 2016 pooled."""
    g = group("Age")
    one = g[g["Year"] == year].set_index("Strata Name")
    pooled_age = pooled_group("Age")
    return pd.DataFrame(
        {
            f"{year} alone": ((one["Upper 95% CL"] - one["Lower 95% CL"]) / 2).reindex(ORDER["Age"]),
            "2012 to 2016 pooled": (pooled_age["high"] - pooled_age["low"]) / 2,
        }
    )


def group_years() -> int:
    """Rows that describe a group in a year, leaving out the all-adults total."""
    return int((rows()["Strata"] != "Total").sum())
