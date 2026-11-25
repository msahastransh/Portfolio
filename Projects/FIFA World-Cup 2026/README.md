# World Cup 2026 Prediction Project

## Subtitle

A football analytics project that predicts World Cup 2026 team probabilities using Poisson models and Monte Carlo simulation.

PS: You can re-use the content of this repo make sure to credit "Anas Riad" and give me a shout on LinkedIn (https://www.linkedin.com/in/riadanas/)

## Purpose

The goal of this project is to estimate each team’s chance of reaching different stages of the 2026 FIFA World Cup, from the group stage to winning the tournament.

The project also includes an interactive Streamlit app to explore predictions, run one live tournament simulation, and compare match probabilities between teams.

## What was done

* Collected and cleaned historical international football match data.
* Prepared the 2026 World Cup fixtures, group-stage structure, knockout bracket, FIFA ranking data, and confederation data.
* Built pre-match Elo ratings for teams.
* Created match-level features such as:

  * home Elo
  * away Elo
  * Elo difference
  * neutral venue
  * tournament weight
  * home and away confederations
* Trained two Poisson regression models:

  * one model for home-team goals
  * one model for away-team goals
* Converted expected goals into win, draw, and loss probabilities.
* Simulated:

  * group-stage matches
  * group tables
  * best third-placed teams
  * Round of 32 bracket
  * knockout rounds
  * full tournaments
* Ran Monte Carlo simulations to estimate stage probabilities.

## Project structure

```text
football_wc2026/
│
├── data/
│   ├── interim/
│   ├── processed/
│   ├── raw/
│   └── reference/
│
├── models/
│   ├── poisson_home.pkl
│   ├── poisson_away.pkl
│   └── feature_columns.pkl
│
├── notebooks/
│   ├── 0-data_fetch.ipynb
│   ├── 1-data_cleaning.ipynb
│   ├── 2-feature_engineering_ELO.ipynb
│   ├── 3-feature_engineering_match_metadata.ipynb
│   ├── 4-model_training.ipynb
│   └── 5-tournament_simulation.ipynb
│
├── src/
│   ├── data_loader.py
│   ├── prediction.py
│   ├── group_stage.py
│   ├── qualification.py
│   ├── bracket.py
│   ├── knockout.py
│   ├── tournament.py
│   └── styling.py
│
├── simulation_app.py
├── pyproject.toml
├── uv.lock
└── README.md
```

## Tools used

* Python
* pandas
* NumPy
* SciPy
* statsmodels
* Streamlit
* uv
* Jupyter notebooks
* Matplotlib / pandas plotting

## Summary of results

The final output is a probability table showing each team’s chance of reaching:

* Round of 32
* Round of 16
* Quarter-finals
* Semi-finals
* Final
* Winner

The 1,000-run Monte Carlo simulation showed that the model strongly favored teams with the highest Elo ratings, especially Argentina and Spain. The final results were saved to:

```text
data/processed/wc2026_tournament_probabilities.csv
```

The Streamlit app includes:

* a precomputed probability dashboard
* a live single-tournament simulation
* a match explorer for team-vs-team predictions
