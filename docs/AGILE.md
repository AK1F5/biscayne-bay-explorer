# Agile development record

## Product goal

Let a student explore the course's Biscayne Bay survey, inspect the measurements
behind each visualization, and explain observed patterns without overstating them.
This is an individual assignment implemented in short, verifiable iterations.

## Prioritized backlog

| ID | User story | Acceptance criteria | Priority | Status |
| --- | --- | --- | --- | --- |
| US1 | As a visitor, I can open the app without setup or an upload. | Bundled course CSV loads; source and survey date are visible; invalid input produces a helpful error. | Must | Done |
| US2 | As a student, I can choose a measurement and survey interval. | Selector and range slider update charts, statistics, and table consistently; reset restores defaults. | Must | Done |
| US3 | As a reader, I can interpret the visualizations accurately. | Plotly charts have titles, units, axis labels, legends, and hover values; chronology is correct. | Must | Done |
| US4 | As a reviewer, I can verify the underlying data and calculations. | Filtered table, CSV download, summary statistics, methodology, and data caveats are available. | Must | Done |
| US5 | As a phone or desktop visitor, I can navigate comfortably. | Clear sections, readable controls, responsive charts, and mobile checks. | Must | Done |
| US6 | As an instructor, I can reproduce and access the app. | Modular code, pinned requirements, README, passing tests, public repository and Streamlit URL. | Must | Done |

## Definition of done

- Acceptance criteria verified with data tests, Streamlit interaction tests, and browser checks.
- No fabricated measurements, silent unit conversions, or unsupported water-safety claims.
- Code formatted and linted; meaningful documentation updated.
- Changes committed in an increment that can be reviewed.
- Deployment is only marked done after the public app has been opened successfully.

## Iteration plan and activity

### Iteration 1 — Reliable data foundation

Scope: US1; parsing, metric definitions, validation, provenance, and data tests.
Planning evidence: read the assignment rubric, MC Module 2 overview/resources,
Week 3 Streamlit examples (including Example 7), course repository, and existing
local water dashboard before implementation.

Review: eight data tests passed. Confirmed 942 observations, inclusive time
filtering, correct probe timestamps, source-row preservation, reference oxygen
statistics, and explicit behavior for missing values and malformed files.
Inspection found all turbidity values negative; the scope was narrowed to five
interpretable measurements while retaining the untouched source CSV.

### Iteration 2 — Interactive exploration

Scope: US2–US5; charts, controls, data display, calculated insights, and responsive UI.

Review: the app now links the same filtered observations across two charts, the
table, downloads, and insights. Added point toggle, comparison selector, column
selector, and reset. All 20 data/chart/app tests passed. Browser checks covered
desktop, two portrait phone sizes, a landscape phone, and portrait/landscape
tablets. A Plotly API compatibility warning discovered in browser review was
fixed, then covered by a warning-free startup assertion.

### Iteration 3 — Release and verification

Scope: US6; documentation, automated checks, browser review, GitHub, and deployment.

Review: README, provenance, and verification record completed. Code and the
three implementation increments were uploaded to the public GitHub repository.
All 20 tests and lint checks passed. Browser CSV export was downloaded and
verified to contain 942 rows with the expected columns and initial values.

Released on Streamlit Community Cloud on October 27, 2026, using Python 3.12,
the `main` branch, and `app.py`. The public app opened in a separate browser
session without signing in. Measurement selection, time filtering, the data
section, and calculated insights were checked on the deployed app.
A reset warning found during cloud review was reproduced in a regression test
and fixed by initializing the time range through session state. All 20 tests,
lint, and formatting checks passed after the fix.

Public app: https://biscayne-bay-explorer-ak1f5.streamlit.app/
Assignment submission in Canvas remains a separate step.

## Review and retrospective

What worked: checking the source data first prevented mixing sensor fields or
misreading the time column. Small functions made it possible to test numeric
results independently of the interface.

What changed: turbidity was removed from the visualization scope after inspecting
the negative readings. Browser testing caught an API warning that successful
calculation tests alone could not catch.

Next improvement: obtain documented calibration metadata and multiple survey
days before making any broader environmental comparisons. Keep browser checks
alongside automated tests in later iterations.

No meetings, peer reviews, or instructor feedback are claimed.

