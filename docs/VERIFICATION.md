# Verification record

## Automated checks

- 20 tests passed with Python 3.12: source data/timestamps, filtering, reference
  statistics, missing values, malformed input, Plotly data/labels/legends,
  measurement changes, single samples, empty intervals, reset, and table columns.
- Reference oxygen results for all 942 rows: min 5.03, max 6.48,
  mean 5.37463906581741 mg/L.
- Static lint and formatting checks are part of the release workflow.

## Browser review

Reviewed the running application in Chrome at desktop size and at these explicit
viewport sizes: 360×800, 430×932, 844×390, 768×1024, and 1024×768.
Phone sidebar opening/closing, readable chart axes, responsive chart widths,
navigation, and the Insights panel were inspected. Page width stayed within
the viewport in the measured phone/tablet checks. Tables use internal scrolling.

The first browser review revealed a Streamlit 1.50 Plotly deprecation warning:
`width` was not supported by that version's chart API. The calls were corrected
to `use_container_width=True`; browser reinspection confirmed the warning was gone.
The startup test now also checks for visible warning elements.

The filtered CSV was downloaded through the browser and verified locally:
942 rows, seven expected columns, and first oxygen values of 6.48, 6.39, and
6.45 mg/L. A final desktop preview was also inspected at 1440×1000.

## Deployment

The public GitHub repository was opened and verified to contain the application,
data, requirements, README, tests, and Agile documentation.
Deployment was deferred at the user's request after the Streamlit sign-in page
was reached. There is no public app URL yet. Local tests do not establish that
Streamlit Community Cloud is deployed or publicly accessible.
