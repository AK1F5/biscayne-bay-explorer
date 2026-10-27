# Dataset provenance

`biscayneBay_waterquality.csv` is the unmodified CSV from
[the CIS3590 Fall 2026 course repository](https://github.com/studentgreg/3590-Fall2026/blob/main/biscayneBay_waterquality.csv),
also linked in Canvas Week 3. Retrieved October 27, 2026.
Source Git blob: `a0dbbe2af453c93cff46e0fcedc0404939aead57`.

The course describes the data as aquatic-robot water-quality observations from
Biscayne Bay. The CSV contains 942 rows and 69 columns. The probe timestamp fields
`Date m/d/y   ` and `Time hh:mm:ss` span February 4, 2022, 16:18:47–16:34:33.
No timezone is specified. The app uses these full probe timestamps rather than
the separate, abbreviated vehicle `Time` field.

The app focuses on five explicitly labeled measurements: probe temperature
(`Temp C`), salinity (`Sal ppt`), pH (`pH`), dissolved oxygen (`ODO mg/L`), and
water-column depth (`Total Water Column (m)`). It does not merge similarly named
temperature or salinity sensor columns. All source fields remain in this file.

Every `Turbid+ NTU` reading is negative in this supplied CSV. These readings are
preserved, but turbidity is intentionally excluded from the selectable metrics;
the source does not provide calibration context that would support interpreting
them. Other telemetry fields can also contain sentinel values. The dashboard
is an exploration of this short historical survey, not a validated assessment
of present-day water quality or safety.

The course repository does not include a dataset license or detailed calibration
metadata. This file is attributed to the course and included for its assigned
educational exercise; no broader license or independent validation is asserted.
