# Changelog

All notable changes to this project are listed here. Versions are dated by month, like `v2026.11`.

## v2026.11 · November 2026

A full rebuild, from a single notebook into a tested, reproducible analysis.

### Fixed

- The 2017 jump was read as a possible real rise. The report now sets out four signs that the survey changed that year,
  and compares groups over 2012 to 2016 instead
- 55–64 year olds and adults with some college were named the highest groups from 2018 alone, where neither can be told
  apart from most other groups. Five years pooled confirm both patterns
- The classifier, with 154 group-year rows and only year and group to go on, was mostly memorising which groups are high.
  It's replaced by comparisons that use the survey's own confidence intervals

### Added

- A findings report with seven findings, written from the data by `findings/build.py`
- Five charts and four tiles, drawn with [bezel-charts](https://pypi.org/project/bezel-charts/). The tiles mark which
  groups are clearly above or below all adults
- Inverse-variance pooling of 2012 to 2016, with standard errors worked back from the published confidence limits
- Tests, an automatic check on every pull request, Dependabot and a security policy
- Social preview image in `assets/social-preview.png`

### Changed

- New folder structure: `data/`, `findings/`, `notebooks/`, `charts/` and `tests/`
- README rewritten around the findings, keeping the data credit
- Notebook rewritten and moved to `notebooks/depression_analysis.ipynb`
- Data moved to `data/adult_depression_lghc_indicator_24.csv`, unchanged
- scikit-learn is no longer needed

## v1.0.0 · November 2026

- Charts rebuilt with bezel-charts in a colour-blind-safe palette
- Target leakage fixed: the models no longer used the confidence limits and case counts
- Data source and credit added to the README

## November 2025

- First version: one notebook and a README
