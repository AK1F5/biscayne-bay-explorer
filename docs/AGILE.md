# Agile development record

## Product goal

Let a student explore the course's Biscayne Bay survey, inspect the measurements
behind each visualization, and explain observed patterns without overstating them.
This is an individual assignment implemented in short, verifiable iterations.

## Prioritized backlog

| ID | User story | Acceptance criteria | Priority | Status |
| --- | --- | --- | --- | --- |
| US1 | As a visitor, I can open the app without setup or an upload. | Bundled course CSV loads; source and survey date are visible; invalid input produces a helpful error. | Must | To do |
| US2 | As a student, I can choose a measurement and survey interval. | Selector and range slider update charts, statistics, and table consistently; reset restores defaults. | Must | To do |
| US3 | As a reader, I can interpret the visualizations accurately. | Plotly charts have titles, units, axis labels, legends, and hover values; chronology is correct. | Must | To do |
| US4 | As a reviewer, I can verify the underlying data and calculations. | Filtered table, CSV download, summary statistics, methodology, and data caveats are available. | Must | To do |
| US5 | As a phone or desktop visitor, I can navigate comfortably. | Clear sections, readable controls, responsive charts, and mobile checks. | Must | To do |
| US6 | As an instructor, I can reproduce and access the app. | Modular code, pinned requirements, README, passing tests, public repository and Streamlit URL. | Must | To do |

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

### Iteration 2 — Interactive exploration

Scope: US2–US5; charts, controls, data display, calculated insights, and responsive UI.

### Iteration 3 — Release and verification

Scope: US6; documentation, automated checks, browser review, GitHub, and deployment.

## Review and retrospective

To be completed with observed results after each iteration. No meetings, peer
reviews, or instructor feedback are claimed unless they actually occurred.

