# Where each claim comes from

Used to check the page against primary documents. "Report" means the final year report; "Paper" is the EE3PEC paper.

| Claim on the page | Source |
|---|---|
| MACCS+ dates, ESP32-C6, ESP-IDF, FreeRTOS, Matter, Apple Home/Siri | Final year report |
| 92 tests: 83 pass, 7 partial, 2 fail; 30-minute soak test | Report, test chapter |
| 5 V rail 5.02 V under load; protection and buck stage | Report, hardware chapter |
| Alexa discovery failed; effect switching via Matter not working | Report, limitations |
| 17 mm vs 18 mm hole spacing caught from datasheet | Placement/project logs |
| Simulink model values (20 kW, 50 Hz, ma 0.8, mf 15, 750 Hz, 10 us) | Paper |
| Gate drive: +15/-15 V, about 8 us dead-time, about 10 ns rise/fall, 300 ns to 1 us delay | Paper, Figs 38-40 and results |
| Pin-out mismatch found during soldering | Paper |
| Renishaw: test jig redesign, ESD sweep up to 12 kV, pulse testing, soldering and Zuken training | Placement report and monthly logs; kept general |
| STEM Ambassador, ECN Challenge 2nd of 8 | Placement reflection and logs |
| Graduate Electrical Engineer, Amey Consulting, from September 2026 | Stated by Ismail |
| Amey workflow: proposals brief to deliverable, client queries, OS tiles in AutoCAD, M/C/P class selection, Lighting Reality, stats packs (overhead, BT, HV, LV, water, gas) | Stated by Ismail |
| BS 5489-1 guides class selection; BS EN 13201-2 sets the performance requirements for each class | BS 5489-1:2020 foreword (supports the BS EN 13201 series); BS EN 13201-2:2015 "Performance requirements"; PD CEN/TR 13201-1 (M, C, P classes) |
| Section 38 = adoption of new roads by the highway authority; Section 278 = developer works to the existing public highway (Highways Act 1980) | legislation.gov.uk s.38; council guidance (e.g. Wigan, Surrey, Bedford) |
| First Class Honours, MIET | Stated by Ismail |
| School Rep (Engineering and Physical Sciences), Student Rep (EEE) | Stated by Ismail |
| GEEP mentor; programme description | Stated by Ismail; programme described on the Royal Academy of Engineering GEEP pages |

Unverified items to confirm: that Ismail works on both Section 38 and Section 278 schemes (the page says he does); location wording "West Midlands, UK".

## Sales edition (sales/index.html and the sales CV PDF)

Source: Ismail's sales-targeted CV (Nov 2026), which is a private document, plus facts he has stated directly (Best-One store work in 2021, open to relocation). The public page and PDF are a web-safe rewrite:

- Internal production details and internal sales rankings from the private CV are left out. The RESOLUTE test-board point is worded as "led the redesign ... reducing a risk to production", because the redesign reached board testing but was not deployed.
- The Renishaw role is shown as "Electronics Engineer (placement year), 2024 to 2025".
- Best-One (2021) is added for face-to-face customer experience.
- Public product names (RESOLUTE, ATOM, TONiC, ADT) are on Renishaw's website and are kept.
- No phone number is published.

`tests/test_sales.py` checks the page and the PDF against general patterns (classification labels, equipment counts, sales rankings, phone numbers), so private wording never has to be written into this public repo.
