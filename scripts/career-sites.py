"""Company / institute career sites near Ilmenau (SuccessFactors-style /search pages).
Output TSV: posted<TAB>title<TAB>company<TAB>location<TAB>url. Posted = 'open' (list pages carry no date;
data/seen.tsv dedup makes each posting appear once). Run: python3 scripts/career-sites.py"""
import re, html, subprocess, time
UA = "Mozilla/5.0 (X11; Linux x86_64) Chrome/124"
SITES = [  # (company label, base, search query string, title filter)
    ("Fraunhofer (Ilmenau)", "https://jobs.fraunhofer.de", "/search/?q=&locationsearch=Ilmenau", r"."),
    ("Fraunhofer (Jena)", "https://jobs.fraunhofer.de", "/search/?q=&locationsearch=Jena", r"student|hilfskraft|praktik|intern|werkstud|abschluss|thesis"),
    ("Fraunhofer (Erfurt)", "https://jobs.fraunhofer.de", "/search/?q=&locationsearch=Erfurt", r"student|hilfskraft|praktik|intern|werkstud|abschluss|thesis"),
    ("X-FAB (Erfurt)", "https://jobs.xfab.com", "/search/?q=&locationsearch=Erfurt", r"student|werkstud|intern|praktik|thesis"),
    ("Jenoptik (Jena)", "https://careers.jenoptik.com", "/search/?q=werkstudent&locationsearch=Jena", r"."),
    ("Jenoptik (Jena)", "https://careers.jenoptik.com", "/search/?q=praktikum&locationsearch=Jena", r"."),
]
SKIP = r"Initiativ|Initiative|Unsolicited|Mitarbeiter\*?in \(|employee"
seen = set()
for label, base, q, filt in SITES:
    h = subprocess.run(["curl", "-s", "-L", "-m", "25", "-A", UA, base + q], capture_output=True, text=True).stdout
    for m in re.finditer(r'href="(/job/[^"]+)"[^>]*>(.*?)</a>', h, re.S):
        t = html.unescape(re.sub(r"<[^>]+>", "", m.group(2))).strip(); u = base + html.unescape(m.group(1))
        if not t or u in seen or re.search(SKIP, t) or not re.search(filt, t, re.I): continue
        seen.add(u); loc = re.search(r"/job/([^-/]+)-", m.group(1)); 
        print("\t".join(["open", t, label.split(" (")[0], loc.group(1) if loc else label, u]))
    time.sleep(1)
