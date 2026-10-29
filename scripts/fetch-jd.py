"""Fetch a job description as plain text. Usage: python3 scripts/fetch-jd.py URL  -> stdout text.
Supports LinkedIn (guest API) and arbeitsagentur.de job detail pages; falls back to generic HTML text."""
import sys, re, html, subprocess
url = sys.argv[1]
def get(u):
    return subprocess.run(["curl", "-s", "-L", "--compressed", "-m", "25", "-A", "Mozilla/5.0", u], capture_output=True).stdout.decode("utf-8", "replace")
def text(h):
    h = re.sub(r"<script.*?</script>|<style.*?</style>", " ", h, flags=re.S)
    h = re.sub(r"<(br|/p|/li|/h\d|/div)[^>]*>", "\n", h)
    t = html.unescape(re.sub(r"<[^>]+>", " ", h))
    return re.sub(r"[ \t]+", " ", re.sub(r"\n\s*\n+", "\n", t)).strip()
m = re.search(r"linkedin\.com/jobs/view/(\d+)", url)
if m:
    h = get(f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{m.group(1)}")
    meta = {k: (re.search(p, h, re.S) or [None, ""])[1].strip() for k, p in {
        "title": r'topcard__title">(.*?)<', "company": r'topcard__org-name-link[^>]*>(.*?)<',
        "posted": r'posted-time-ago__text[^>]*>(.*?)<', "applicants": r'num-applicants__caption[^>]*>(.*?)<'}.items()}
    body = (re.search(r'show-more-less-html__markup[^>]*>(.*?)</div>', h, re.S) or [None, ""])[1]
    off = (re.search(r'"(https?://[^"]+)"[^>]*data-tracking-control-name="public_jobs_apply-link-offsite', h) or [None, ""])[1]
    print("\n".join(f"{k}: {html.unescape(v)}" for k, v in meta.items()))
    print("apply_offsite:", html.unescape(off))
    print("---\n" + text(body))
else:
    h = get(url)
    # Most job boards (XING, StepStone, company ATS pages) embed a schema.org JobPosting with the full text.
    for blk in re.findall(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', h, re.S):
        try:
            import json
            j = json.loads(blk)
        except Exception:
            continue
        for o in (j if isinstance(j, list) else j.get("@graph", [j]) if isinstance(j, dict) else []):
            if isinstance(o, dict) and o.get("@type") == "JobPosting" and len(o.get("description") or "") > 200:
                org = o.get("hiringOrganization") or {}
                loc = o.get("jobLocation") or {}
                loc = loc[0] if isinstance(loc, list) and loc else loc
                addr = (loc.get("address") or {}) if isinstance(loc, dict) else {}
                print("title:", html.unescape(o.get("title", "")))
                print("company:", org.get("name", "") if isinstance(org, dict) else org)
                print("posted:", o.get("datePosted", ""))
                print("location:", addr.get("addressLocality", "") if isinstance(addr, dict) else "", "| remote:", o.get("jobLocationType", ""))
                print("---\n" + text(o["description"].replace("null", "")))
                sys.exit(0)
    t = text(h)
    if "arbeitsagentur.de" in url:
        i = t.find("Stellenbeschreibung")
        t = t[i:] if i > 0 else t
        j = t.find("Weitere Informationen")
        t = t[:j] if j > 0 else t
    print(t[:12000])
