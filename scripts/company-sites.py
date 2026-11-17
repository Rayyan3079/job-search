"""Student jobs in Germany straight from multinationals' own career systems (not job boards).
Sources: Workday (cxs JSON API), Greenhouse (boards API), SmartRecruiters (public postings API).
Usage:
  python3 scripts/company-sites.py [DAYS]   -> TSV: posted<TAB>title<TAB>company<TAB>location<TAB>url  (default DAYS=30)
  python3 scripts/company-sites.py --jd URL -> job description in fetch-jd.py format (header lines, ---, text)
Add employers to the lists below; probe new Workday tenants with an empty site id (404 'Job_Posting_Site_ID' = tenant exists)."""
import sys, re, json, html, subprocess, datetime
from concurrent.futures import ThreadPoolExecutor

UA = "Mozilla/5.0 (X11; Linux x86_64) Chrome/124"
WORKDAY = [  # (company, tenant, wd host, site id)
    ("Philips", "philips", "wd3", "jobs-and-careers"), ("Sartorius", "sartorius", "wd3", "SartoriusCareers"),
    ("Evonik", "evonik", "wd3", "External_Careers"), ("Novartis", "novartis", "wd3", "Novartis_Careers"),
    ("Roche", "roche", "wd3", "roche-ext"), ("AstraZeneca", "astrazeneca", "wd3", "Careers"),
    ("GSK", "gsk", "wd5", "GskCareers"), ("Sanofi", "sanofi", "wd3", "SanofiCareers"),
    ("Pfizer", "pfizer", "wd1", "PfizerCareers"), ("Abbott", "abbott", "wd5", "AbbottCareers"),
    ("Medtronic", "medtronic", "wd1", "MedtronicCareers"), ("3M", "3m", "wd1", "Search"),
    ("Accenture", "accenture", "wd103", "AccentureCareers"), ("Intel", "intel", "wd1", "External"),
    ("Cisco", "cisco", "wd5", "Cisco_Careers"), ("HP", "hp", "wd5", "ExternalCareerSite"),
    ("Unilever", "unilever", "wd3", "Unilever_Experienced_Professionals"), ("Shell", "shell", "wd3", "ShellCareers"),
    ("GlobalFoundries", "globalfoundries", "wd1", "External"), ("NVIDIA", "nvidia", "wd5", "NVIDIAExternalCareerSite"),
]
GREENHOUSE = [("Celonis", "celonis"), ("N26", "n26"), ("Trade Republic", "traderepublicbank"), ("HelloFresh", "hellofresh"),
              ("SumUp", "sumup"), ("Contentful", "contentful"), ("Flix", "flix"), ("Raisin", "raisin"), ("Staffbase", "staffbase"),
              ("commercetools", "commercetools"), ("Solaris", "solarisbank"), ("trivago", "trivago"), ("MOIA", "moia"),
              ("Isar Aerospace", "isaraerospace"), ("Helsing", "helsing"), ("Moonfare", "moonfare")]
SMARTRECRUITERS = [("Bosch", "BoschGroup"), ("Continental", "Continental"), ("Delivery Hero", "DeliveryHero"), ("AbbVie", "AbbVie")]

STUDENT = re.compile(r"werkstud|working student|student|intern\b|internship|praktik|hiwi|hilfskraft|trainee", re.I)
NOT = re.compile(r"senior|lead\b|principal|manager|director|head of|abschlussarbeit|thesis|masterarbeit|bachelorarbeit|ausbildung|duales|"
                 r"phd|promotion|doktorand|pflichtpraktik|mandatory|schülerpraktik|pharmazie|pharmazeut|initiativ|mba", re.I)
DE = re.compile(r"germany|deutschland|^DE,|\bDE - |berlin|munich|münchen|hamburg|frankfurt|cologne|köln|stuttgart|düsseldorf|dusseldorf|"
                r"leipzig|dresden|hannover|nuremberg|nürnberg|bonn|mannheim|karlsruhe|darmstadt|jena|erfurt|göttingen|marburg|"
                r"wiesbaden|mainz|essen|dortmund|bremen|heidelberg|freiburg|ulm|regensburg|ingolstadt|aachen|walldorf|penzberg|"
                r"mannheim|ludwigshafen|leverkusen|hanau|biberach|wolfsburg|braunschweig|erlangen|tübingen|potsdam", re.I)
KEYWORDS = ["working student", "werkstudent", "internship", "praktikum", "student"]


def curl(url, data=None):
    cmd = ["curl", "-s", "-L", "--compressed", "-m", "30", "-A", UA, url]
    if data is not None:
        cmd += ["-H", "Content-Type: application/json", "-H", "Accept: application/json", "-d", json.dumps(data)]
    return subprocess.run(cmd, capture_output=True).stdout.decode("utf-8", "replace")


def text(h):
    h = re.sub(r"<script.*?</script>|<style.*?</style>", " ", h or "", flags=re.S)
    h = re.sub(r"<(br|/p|/li|/h\d|/div)[^>]*>", "\n", h)
    t = html.unescape(re.sub(r"<[^>]+>", " ", h))
    return re.sub(r"[ \t]+", " ", re.sub(r"\n\s*\n+", "\n", t)).strip()


def days_ago(posted):
    """Workday 'Posted Today' / 'Posted 3 Days Ago' / 'Posted 30+ Days Ago' -> int days."""
    p = (posted or "").lower()
    if "today" in p: return 0
    if "yesterday" in p: return 1
    m = re.search(r"(\d+)", p)
    return int(m.group(1)) + (1 if "+" in p else 0) if m else 99


def iso(d):
    return (datetime.date.today() - datetime.timedelta(days=d)).isoformat()


def workday(entry, max_days):
    company, t, n, site = entry
    out, seen = [], set()
    for kw in KEYWORDS:
        for offset in (0, 20, 40):
            raw = curl(f"https://{t}.{n}.myworkdayjobs.com/wday/cxs/{t}/{site}/jobs",
                       {"appliedFacets": {}, "limit": 20, "offset": offset, "searchText": kw})
            try: jobs = json.loads(raw).get("jobPostings", [])
            except Exception: break
            for j in jobs:
                path, title, loc = j.get("externalPath", ""), j.get("title", ""), j.get("locationsText", "")
                d = days_ago(j.get("postedOn"))
                if path in seen or d > max_days or not STUDENT.search(title) or NOT.search(title) or not DE.search(loc):
                    continue
                seen.add(path)
                out.append((iso(d), title, company, loc, f"https://{t}.{n}.myworkdayjobs.com/en-US/{site}{path}"))
            if len(jobs) < 20: break
    return out


def greenhouse(entry, max_days):
    company, token = entry
    try: jobs = json.loads(curl(f"https://boards-api.greenhouse.io/v1/boards/{token}/jobs")).get("jobs", [])
    except Exception: return []
    out = []
    for j in jobs:
        title, loc = j.get("title", ""), (j.get("location") or {}).get("name", "")
        upd = (j.get("updated_at") or "")[:10]
        try: d = (datetime.date.today() - datetime.date.fromisoformat(upd)).days
        except Exception: d = 0
        if d > max_days or not STUDENT.search(title) or NOT.search(title) or not DE.search(loc): continue
        out.append((upd, title, company, loc, j.get("absolute_url", "")))
    return out


def smartrecruiters(entry, max_days):
    company, cid = entry
    out, seen = [], set()
    for kw in KEYWORDS:
        try: res = json.loads(curl(f"https://api.smartrecruiters.com/v1/companies/{cid}/postings?country=de&limit=100&q={kw.replace(' ', '%20')}")).get("content", [])
        except Exception: continue
        for j in res:
            title, loc = j.get("name", ""), (j.get("location") or {}).get("city", "")
            rel = (j.get("releasedDate") or "")[:10]
            try: d = (datetime.date.today() - datetime.date.fromisoformat(rel)).days
            except Exception: d = 0
            if j["id"] in seen or d > max_days or not STUDENT.search(title) or NOT.search(title): continue
            seen.add(j["id"])
            out.append((rel, title, company, loc + ", Germany", f"https://jobs.smartrecruiters.com/{cid}/{j['id']}"))
    return out


def jd(url):
    """Print a job description for a Workday / Greenhouse / SmartRecruiters URL."""
    m = re.match(r"https://([^.]+)\.(wd\d+)\.myworkdayjobs\.com/(?:[a-z]{2}-[A-Z]{2}/)?([^/]+)(/job/.+)", url)
    if m:
        t, n, site, path = m.groups()
        info = json.loads(curl(f"https://{t}.{n}.myworkdayjobs.com/wday/cxs/{t}/{site}{path}")).get("jobPostingInfo", {})
        print(f"title: {info.get('title','')}\ncompany: {t}\nposted: {info.get('startDate','')}\nlocation: {info.get('location','')} | remote: {info.get('remoteType','')}")
        print("---\n" + text(info.get("jobDescription", ""))); return
    m = re.search(r"greenhouse\.io/([^/]+)/jobs/(\d+)", url) or re.search(r"[?&]gh_jid=(\d+)", url)
    if m and "greenhouse.io" in url:
        j = json.loads(curl(f"https://boards-api.greenhouse.io/v1/boards/{m.group(1)}/jobs/{m.group(2)}"))
        print(f"title: {j.get('title','')}\ncompany: {m.group(1)}\nposted: {j.get('updated_at','')[:10]}\nlocation: {(j.get('location') or {}).get('name','')}")
        print("---\n" + text(html.unescape(j.get("content", "")))); return
    m = re.search(r"smartrecruiters\.com/([^/]+)/(\d+)", url)
    if m:
        j = json.loads(curl(f"https://api.smartrecruiters.com/v1/companies/{m.group(1)}/postings/{m.group(2)}"))
        sec = (j.get("jobAd") or {}).get("sections", {})
        body = "\n".join(text((sec.get(k) or {}).get("text", "")) for k in ("companyDescription", "jobDescription", "qualifications", "additionalInformation"))
        print(f"title: {j.get('name','')}\ncompany: {(j.get('company') or {}).get('name','')}\nposted: {j.get('releasedDate','')[:10]}\nlocation: {(j.get('location') or {}).get('city','')}")
        print("---\n" + body); return
    print("unsupported url", url)


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--jd":
        jd(sys.argv[2]); sys.exit(0)
    max_days = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    tasks = [(workday, e) for e in WORKDAY] + [(greenhouse, e) for e in GREENHOUSE] + [(smartrecruiters, e) for e in SMARTRECRUITERS]
    with ThreadPoolExecutor(10) as ex:
        for rows in ex.map(lambda fe: fe[0](fe[1], max_days), tasks):
            for r in rows:
                print("\t".join(x.replace("\t", " ").replace("\n", " ") for x in r))
