# Company career sites run (daily, ~20:40 Berlin, ready before 22:00)

Goal: find student jobs (Werkstudent, working student, internship, HiWi) in Germany **directly on multinationals' own career
systems**, so Rayyan gets roles that the LinkedIn/StepStone/XING run does not show. Same rules as [RUNBOOK.md](RUNBOOK.md)
(facts only from `cv.md`, obey `modes/_profile.md`, never submit anything, freelance not allowed), with these differences:

## 1. Discover

```bash
source scripts/setup.sh
T=$(date +%F)-co                      # separate run tag, e.g. 2026-11-18-co
python3 scripts/company-sites.py 30 > runs/$T-company.tsv   # Workday, Greenhouse, SmartRecruiters (~40 employers)
python3 scripts/collect.py $T          # drops everything already in data/seen.tsv, incl. jobs found on LinkedIn
D=runs/jd-cache-$T; mkdir -p $D
awk -F'\t' '{printf "%03d\t%s\n", NR, $0}' runs/$T-candidates.tsv > runs/$T-cand-num.tsv
tr '\n' '\0' < runs/$T-cand-num.tsv | xargs -0 -P 8 -I{} bash scripts/fetch-one.sh {} $D
python3 scripts/lanes.py $D > runs/$T-lanes.tsv
```

`collect.py` puts jobs located near Ilmenau (Arnstadt, Erfurt, Jena, Weimar, ...) in Lane L, everything else in Lane G.
Posting window here is **30 days**: company sites keep postings longer and these jobs are less crowded.
Because `data/seen.tsv` also holds every LinkedIn/StepStone/XING job ever found, anything left is new to Rayyan;
company+title matches against LinkedIn finds are removed too.

## 2. Qualify and package
As in RUNBOOK.md steps 2-3: English accepted (no German requirement), fit >= 2.5 (any fit for Lane L), max 8 packages, Lane L first.
German-language postings that require German are listed only. Folder: `output/<date>/<slug>/` (no `-co` suffix), README notes
"Source: company career site (<system>)". Contact section per `modes/_custom.md`.

## 3. Record and save
Append to `data/seen.tsv` (lane `company`), `data/applications.md`, write `digests/<date>-company.md`, add one line under
"Latest run" in README.md. Commit `Company sites run <date>: N packages`, push, send PDFs with SendUserFile.

## Adding employers
Edit the lists at the top of `scripts/company-sites.py`.
- **Workday:** POST `https://<tenant>.<wdN>.myworkdayjobs.com/wday/cxs/<tenant>/x/jobs` → a 404 mentioning
  `Job_Posting_Site_ID` means the tenant exists; then try site ids (`External`, `Careers`, `<Tenant>Careers`, ...).
- **Greenhouse:** `https://boards-api.greenhouse.io/v1/boards/<token>/jobs` returns JSON.
- **SmartRecruiters:** `https://api.smartrecruiters.com/v1/companies/<Id>/postings?country=de`.
Not reachable from the cloud container (403 / JS-only): SAP (jobs.sap.com), Siemens, Mercedes-Benz, BMW, Allianz, Zeiss.
