"""Worldwide remote part-time / junior jobs in his field (Lane W).
Sources: Remotive, RemoteOK, Himalayas, Jobicy, Working Nomads (public JSON feeds) + LinkedIn worldwide remote part-time/contract/internship.
Output TSV: posted<TAB>title<TAB>company<TAB>location | type<TAB>url. Usage: python3 scripts/remote-world.py [DAYS]"""
import json, re, subprocess, sys, time, html, urllib.parse
from datetime import datetime, timezone, timedelta
DAYS = int(sys.argv[1]) if len(sys.argv) > 1 else 7
CUT = datetime.now(timezone.utc) - timedelta(days=DAYS)
UA = "Mozilla/5.0 (X11; Linux x86_64) Chrome/124"
def get(u):
    return subprocess.run(["curl", "-s", "-L", "-m", "30", "-A", UA, u], capture_output=True, text=True).stdout
def js(u):
    try: return json.loads(get(u))
    except Exception: return {}
REL = r"data analyst|data analytics|analytics|business intelligence|\bbi\b|power bi|tableau|looker|reporting|dashboard|\bsap\b|analytics cloud|datasphere|data engineer|etl|\bsql\b|machine learning|\bml\b|data scien|ai trainer|data annotat|data quality|data entry|python"
SENIOR = r"senior|\bsr\.?\b|lead\b|principal|staff|head of|director|vp\b|manager|architect|expert"
OKLOC = r"worldwide|anywhere|global|europe|\beu\b|emea|germany|deutschland|cet|cest|remote$|^$"
rows, seen = [], set()
def add(dt, title, company, loc, jtype, url):
    if not url or url in seen: return
    t = (title or "").lower(); l = (loc or "").lower().strip()
    if not re.search(REL, t) or re.search(SENIOR, t): return
    if l and not re.search(OKLOC, l): return
    try:
        d = datetime.fromisoformat(str(dt).replace("Z", "+00:00")) if not str(dt).isdigit() else datetime.fromtimestamp(int(dt), timezone.utc)
        if d.tzinfo is None: d = d.replace(tzinfo=timezone.utc)
        if d < CUT: return
        dt = d.date().isoformat()
    except Exception: pass
    seen.add(url); rows.append("\t".join(str(x).replace("\t", " ") for x in [dt, html.unescape(title or ""), company or "", f"{loc or 'Worldwide'} | {jtype or ''}", url]))
for q in ["data", "analytics", "sql", "sap", "business intelligence", "machine learning"]:
    for j in js("https://remotive.com/api/remote-jobs?search=" + urllib.parse.quote(q)).get("jobs", []):
        add(j.get("publication_date"), j.get("title"), j.get("company_name"), j.get("candidate_required_location"), j.get("job_type"), j.get("url"))
    time.sleep(1)
for tag in ["data", "analytics", "sql", "sap", "data-science"]:
    d = js("https://remoteok.com/api?tag=" + tag)
    for j in (d[1:] if isinstance(d, list) else []):
        add(j.get("date"), j.get("position"), j.get("company"), j.get("location"), "", j.get("url"))
    time.sleep(1)
for q in ["data analyst", "business intelligence", "sap", "data engineer", "machine learning"]:
    d = js("https://himalayas.app/jobs/api/search?q=" + urllib.parse.quote(q))
    for j in d.get("jobs", []):
        locs = j.get("locationRestrictions") or []
        add(j.get("pubDate"), j.get("title"), j.get("companyName"), ", ".join(locs) if isinstance(locs, list) else str(locs), j.get("employmentType"), j.get("applicationLink") or j.get("guid"))
    time.sleep(1)
for tag in ["data", "analytics", "sap", "sql", "python"]:
    d = js(f"https://jobicy.com/api/v2/remote-jobs?count=50&tag={tag}")
    for j in d.get("jobs", []):
        add(j.get("pubDate"), j.get("jobTitle"), j.get("companyName"), j.get("jobGeo"), ",".join(j.get("jobType") or []), j.get("url"))
    time.sleep(1)
d = js("https://www.workingnomads.com/api/exposed_jobs/")
for j in (d if isinstance(d, list) else []):
    add(j.get("pub_date"), j.get("title"), j.get("company_name"), j.get("location"), j.get("category_name"), j.get("url"))
# LinkedIn: worldwide / EU remote, part-time (P), contract (C), internship (I)
for loc in ["Worldwide", "European Union"]:
    for kw in ["data analyst", "SAP Analytics Cloud", "business intelligence", "data engineer", "SQL", "power bi", "machine learning", "AI trainer"]:
        u = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?" + urllib.parse.urlencode({"keywords": kw, "location": loc, "f_WT": "2", "f_JT": "P,C,I", "f_TPR": f"r{DAYS*86400}"})
        h = get(u)
        for card in h.split("<li>"):
            m = re.search(r"linkedin\.com/jobs/view/[^\"?]*?(\d{6,})", card)
            if not m: continue
            g = lambda p: html.unescape(re.sub(r"<[^>]+>", "", (re.search(p, card, re.S) or [None, ""])[1] or "")).strip()
            add((re.search(r'datetime="([^"]+)"', card) or [0, ""])[1], g(r'base-search-card__title">(.*?)</h3>'), g(r'base-search-card__subtitle">(.*?)</h4>'),
                "", "LinkedIn remote part-time/contract/intern (" + loc + ")", "https://www.linkedin.com/jobs/view/" + m.group(1))
        time.sleep(1)
print("\n".join(rows))
