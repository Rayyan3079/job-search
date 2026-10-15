"""Fetch a job description as plain text. Usage: python3 scripts/fetch-jd.py URL  -> stdout text.
Supports LinkedIn (guest API) and arbeitsagentur.de job detail pages; falls back to generic HTML text."""
import sys, re, html, subprocess
url = sys.argv[1]
def get(u):
    return subprocess.run(["curl", "-s", "-L", "-m", "25", "-A", "Mozilla/5.0", u], capture_output=True, text=True).stdout
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
    t = text(h)
    if "arbeitsagentur.de" in url:
        i = t.find("Stellenbeschreibung")
        t = t[i:] if i > 0 else t
        j = t.find("Weitere Informationen")
        t = t[:j] if j > 0 else t
    print(t[:12000])
