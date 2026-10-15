"""Title-level triage of scan results (Arbeitsagentur pipeline.md + LinkedIn TSV).
Usage: python3 scripts/triage.py data/pipeline.md runs/DATE-linkedin.tsv > runs/DATE-shortlist.tsv"""
import re, sys
STRONG = r"sap|datasphere|analytics cloud|\bsac\b|\bbw\b|s/4|business intelligence|\bbi\b|power bi|reporting|data analy|daten ?analy|data science|data scientist|machine learning|\bml\b|\bai\b|\bki\b|künstliche|computer vision|nlp|data engineer|daten|analytics|analyst|dashboard"
MEDIUM = r"consult|beratung|digital|it-|\bit\b|informatik|python|sql|process|prozess|erp"
STUDENT = r"werkstudent|working student|studentische|student assistant|studentin|student\b"
NEG = r"controlling|accounting|buchhaltung|rechnungswesen|marketing|sales|vertrieb|personal|hr\b|recruit|social media|einkauf|logistik|lager|pflege|steuer|tax|audit|legal|recht"
rows = []
for path in sys.argv[1:]:
    for line in open(path, encoding="utf-8"):
        if path.endswith(".md"):
            m = re.match(r"- \[ \] (\S+) \| (.*?) \| (.*?) \| (.*)", line.strip())
            if not m: continue
            url, company, title, loc = m.groups(); posted = "≤3d (AA)"
        else:
            p = line.rstrip("\n").split("\t")
            if len(p) < 5: continue
            posted, title, company, loc, url = p
        t = title.lower()
        s = 3 * len(re.findall(STRONG, t)) + len(re.findall(MEDIUM, t))
        if re.search(NEG, t) and not re.search(r"sap|data|daten|analytics|bi\b", t): s -= 5
        student = bool(re.search(STUDENT, t))
        if s <= 0: continue
        rows.append((s + (2 if student else 0), student, posted, company.strip(), title.strip(), loc.strip(), url))
seen = set(); out = []
for r in sorted(rows, key=lambda r: -r[0]):
    k = (r[3].lower()[:20], re.sub(r"\W", "", r[4].lower())[:40])
    if k in seen: continue
    seen.add(k); out.append(r)
for r in out: print("\t".join(map(str, r)))
