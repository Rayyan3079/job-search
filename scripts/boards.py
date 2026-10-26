"""Search StepStone and XING. Output TSV: posted<TAB>title<TAB>company<TAB>location<TAB>url
Usage: python3 scripts/boards.py MODE   (MODE = local | remote | germany)"""
import sys, re, html, json, subprocess, urllib.parse, time
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
MODE = sys.argv[1] if len(sys.argv) > 1 else "local"
def get(u):
    return subprocess.run(["curl", "-s", "-L", "-m", "25", "-A", UA, u], capture_output=True, text=True).stdout
KW = {"local": ["werkstudent", "studentische hilfskraft", "praktikum", "working student", "werkstudent data", "werkstudent it", "werkstudent sap", "werkstudent informatik"],
      "remote": ["werkstudent remote", "working student remote", "werkstudent homeoffice data", "werkstudent remote sap", "werkstudent remote data analyst"],
      "germany": ["werkstudent sap", "working student data", "werkstudent data analyst", "werkstudent business intelligence", "working student machine learning", "werkstudent data science"]}[MODE]
out, seen = [], set()
def emit(posted, title, company, loc, url):
    if url in seen: return
    seen.add(url); out.append("\t".join(x.replace("\t", " ").strip() for x in [posted, title, company, loc, url]))
for kw in KW:
    # StepStone
    slug = urllib.parse.quote(kw.replace(" ", "-"))
    u = f"https://www.stepstone.de/jobs/{slug}/in-ilmenau?radius=60&sort=2&action=sort_publish" if MODE == "local" else f"https://www.stepstone.de/jobs/{slug}?sort=2&action=sort_publish" + ("&wfh=1" if MODE == "remote" else "")
    d = re.sub(r"<style[^>]*>.*?</style>", "", get(u), flags=re.S)
    for it in d.split('data-testid="job-item"')[1:]:
        m = re.search(r'href="(https://www\.stepstone\.de/stellenangebote--[^"]+)"', it)
        t = re.search(r'data-testid="job-item-title".*?>([^<>]{6,})</div>', it, re.S)
        c = re.search(r'data-at="job-item-company-name".*?</svg></span>(?:<[^>]+>)*([^<]+)<', it, re.S)
        l = re.search(r'data-at="job-item-location".*?</svg></span>(?:<[^>]+>)*([^<]+)<', it, re.S)
        dt = re.search(r'<time[^>]*datetime="([^"]+)"', it)
        if m and t:
            emit(dt.group(1)[:10] if dt else "stepstone", html.unescape(t.group(1)), html.unescape(c.group(1)) if c else "", html.unescape(l.group(1)) if l else "", m.group(1).split("?")[0])
    time.sleep(1)
    # XING
    q = urllib.parse.urlencode({"keywords": kw, **({"location": "Ilmenau", "radius": "60"} if MODE == "local" else {}), **({"remoteOption": "FULL_REMOTE.050e26"} if MODE == "remote" else {}), "sort": "date"})
    d = get("https://www.xing.com/jobs/search?" + q)
    for m in re.finditer(r'"VisibleJob:[^"]+":(\{.*?"userProfileMatches":null\})', d):
        try: j = json.loads(m.group(1))
        except Exception: continue
        emit((j.get("refreshedAt") or "")[:10], j.get("title", ""), (j.get("companyInfo") or {}).get("companyNameOverride", ""),
             ", ".join(x.get("city", "") for x in (j.get("locations") or [])), j.get("url", ""))
    time.sleep(1)
print("\n".join(out))
