# Who Gets Told They Have Depression?

**How common depression is among adults in California from 2012 to 2018, who is most affected, and why the 2017 jump
needs a second look.**

[![Checks](https://github.com/ShazMoghaddam/depression-indicator-analysis/actions/workflows/checks.yml/badge.svg)](https://github.com/ShazMoghaddam/depression-indicator-analysis/actions/workflows/checks.yml)
[![Charts: bezel-charts](https://img.shields.io/pypi/v/bezel-charts?label=charts%3A%20bezel-charts&color=332288)](https://pypi.org/project/bezel-charts/)
[![MIT licence](https://img.shields.io/badge/licence-MIT-CC6677)](LICENSE)

About 1 in 8 Californian adults had been told by a health professional that they have depression, until a sudden jump
in 2017. This project compares groups the careful way, using the survey's own margins of error, and asks whether that
jump is real.

> **Every chart here is drawn with [bezel-charts](https://pypi.org/project/bezel-charts/), an open-source Python library
> created by Shaz Moghaddam, the author of this project.** It turns pandas data into clean, self-contained SVG charts.

---

## Key findings

<!-- key-findings:start -->
### The 2017 jump looks like a change in the survey, not in people

The rate held between 11.7% and 13.8% from 2012 to 2016, then rose to **19.0%** in 2017. Every one of the 22
groups rose that same year, while the survey heard from its fewest people (8,141, against 16,354 in 2012). A real change that
sudden and that even would be unusual, so treat 2017 and 2018 with care.

![Adults ever told they have depression, by year](charts/overall-trend.svg)

### Women report depression far more often than men, every year

Over 2012 to 2016, 15.9% of women had been told they have depression against 9.3% of men. The gap is clear
in all 7 years.

![Women and men, by year](charts/sex-gap.svg)

### Age, income and ethnicity all matter

Pooling 2012 to 2016 gives each group enough answers to compare. Depression peaks at **18.0%** for 55–64 year olds,
reaches **18.1%** in households earning under $20,000 against 9.3% at $100,000 or more, and is lowest among
Asian and Pacific Islander adults (**5.1%**). Rose bars are clearly above all adults, green clearly below.

<p>
  <img src="charts/tile-age.svg" alt="By age: rising from 9.2 percent at 18 to 34 to 18.0 percent at 55 to 64, then 13.3 percent at 65 and over" width="330">
  <img src="charts/tile-income.svg" alt="By income: 18.1 percent under 20 thousand dollars, 9.3 percent at 100 thousand or more" width="330">
</p>
<p>
  <img src="charts/tile-education.svg" alt="By education: highest with some college at 14.6 percent, lowest with a degree at 11.0 percent" width="330">
  <img src="charts/tile-race.svg" alt="By race and ethnicity: Asian and Pacific Islander lowest at 5.1 percent, Other highest at 20.0 percent" width="330">
</p>

### One year of data can't rank the groups

In 2018 alone, none of the 10 pairs of age groups can be told apart. Pooled over five years, 9 can.

![Margin of error by age, one year against five](charts/margins.svg)
<!-- key-findings:end -->

**[Read all seven findings, and what the data can't tell you →](findings/README.md)**

| # | Finding | |
|---|---|---|
| 1 | About 1 in 8 adults | And steady until 2016 |
| 2 | The 2017 jump looks like a change in the survey | Four warning signs |
| 3 | Women report depression far more often | In every year |
| 4 | Depression rises with age until 65 | Then falls |
| 5 | Lower income, more depression | About double at the bottom |
| 6 | Asian and Pacific Islander adults report the least | In every year |
| 7 | One year of data can't rank the groups | And why the model was dropped |

---

## Run it yourself

You'll need Python 3.11 or newer. The data is in the repo, so there's nothing to download.

```sh
git clone https://github.com/ShazMoghaddam/depression-indicator-analysis.git
cd depression-indicator-analysis
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt

python findings/build.py    # charts and report
pytest                      # checks the data and the numbers
```

Or open [`notebooks/depression_analysis.ipynb`](notebooks/depression_analysis.ipynb) for the same analysis with the
working shown.

## What's in the repo

```
├── data/
│   ├── adult_depression_lghc_indicator_24.csv   The published file, unchanged
│   └── sources.json                             Where it came from
├── findings/
│   ├── analysis.py                              Every calculation, as small functions
│   ├── charts.py                                Every chart
│   ├── build.py                                 Writes the charts and the report
│   └── README.md                                The full report
├── notebooks/depression_analysis.ipynb
├── charts/                                      The SVG charts
├── assets/social-preview.png                    The image GitHub shows when the repo is shared
├── tests/                                       Checks on the data and the findings
└── .github/                                     Automatic checks and dependency updates
```

## Data source and credit

- **Dataset:** [Adult Depression (LGHC Indicator)](https://catalog.data.gov/dataset/adult-depression-lghc-indicator) on
  DATA.GOV, hosted on the [California Health and Human Services Open Data Portal](https://data.chhs.ca.gov/)
- **Publisher:** California Department of Public Health (CDPH)
- **Survey:** California Behavioral Risk Factor Surveillance Survey (BRFSS), an annual telephone survey run for CDPH by
  the Public Health Survey Research Program at California State University, Sacramento
- **What it measures:** the share of adults who have ever been told by a doctor, nurse or other health professional that
  they have a depressive disorder
- **Part of:** [Let's Get Healthy California](https://letsgethealthy.ca.gov/), where this is Indicator 24
- **Licence:** [Creative Commons Attribution (CC BY)](http://www.opendefinition.org/licenses/cc-by)

The data was collected and published by CDPH and the BRFSS team, and I'm grateful for their work in making it openly
available. CDPH notes that its weighting uses California Department of Finance population figures rather than the U.S.
Census, so the numbers may differ from national BRFSS tables. The analysis and charts in this repo are my own and are
not endorsed by CDPH.

Code and content in this repo are [MIT licensed](LICENSE). The data remains subject to its publisher's terms.

---

Created by **Shaz Moghaddam** · London
[Website](https://shazmoghaddam.github.io) · [LinkedIn](https://www.linkedin.com/in/shazmoghaddam)
