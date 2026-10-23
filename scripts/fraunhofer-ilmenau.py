"""Lists Fraunhofer job postings in Ilmenau (IDMT, IOSB-AST) as TSV: posted<TAB>title<TAB>company<TAB>location<TAB>url.
Posting dates are not on the list page, so 'posted' is empty; data/seen.tsv dedup makes each posting appear once."""
import re, html, subprocess
h = subprocess.run(["curl","-s","-L","-m","25","-A","Mozilla/5.0","https://jobs.fraunhofer.de/search/?q=&locationsearch=Ilmenau"],capture_output=True,text=True).stdout
seen=set()
for m in re.finditer(r'href="(/job/[^"]+)"[^>]*>(.*?)</a>', h, re.S):
    t = html.unescape(re.sub(r"<[^>]+>","",m.group(2))).strip(); u = "https://jobs.fraunhofer.de"+m.group(1)
    if not t or u in seen or re.search(r"Initiativ|Initiative|Mitarbeiter|employee", t): continue
    seen.add(u); print("\t".join(["open", t, "Fraunhofer (Ilmenau)", "Ilmenau", u]))
