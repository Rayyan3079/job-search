#!/usr/bin/env bash
# Lists LinkedIn job postings in Germany from the last N hours (default 72) for each keyword.
# Output: TSV  posted_iso <TAB> title <TAB> company <TAB> location <TAB> url
HOURS="${HOURS:-72}"
SECS=$((HOURS*3600))
KEYWORDS=(
  "Werkstudent SAP" "Working Student SAP" "Werkstudent SAP Analytics" "Werkstudent Business Intelligence"
  "Working Student Business Intelligence" "Werkstudent Data Analyst" "Working Student Data Analyst"
  "Working Student Data Analytics" "Werkstudent Reporting" "Werkstudent Data Science" "Working Student Data Science"
  "Working Student Machine Learning" "Werkstudent Machine Learning" "Working Student AI" "Werkstudent Data Engineering"
  "Working Student Data Engineering" "Werkstudent IT Consulting" "Working Student SAP Consulting"
)
for kw in "${KEYWORDS[@]}"; do
  for start in 0 25; do
    curl -s -m 20 -A "Mozilla/5.0" -G "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search" \
      --data-urlencode "keywords=$kw" --data-urlencode "location=Germany" \
      --data-urlencode "f_TPR=r$SECS" --data-urlencode "start=$start"
    sleep 1
  done
done | python3 -c '
import sys,re,html
data=sys.stdin.read()
seen=set()
for card in data.split("<li>"):
    url=re.search(r"href=\"(https://[a-z]+\.linkedin\.com/jobs/view/[^\"?]+)",card)
    if not url: continue
    u=url.group(1)
    jid=re.search(r"(\d{6,})",u)
    key=jid.group(1) if jid else u
    if key in seen: continue
    seen.add(key)
    g=lambda p: html.unescape(re.sub(r"\s+"," ",(re.search(p,card,re.S) or [None,""])[1] or "")).strip()
    title=g(r"base-search-card__title\">(.*?)</h3>")
    company=re.sub(r"<[^>]+>","",g(r"base-search-card__subtitle\">(.*?)</h4>")).strip()
    loc=g(r"job-search-card__location\">(.*?)</span>")
    dt=(re.search(r"datetime=\"([^\"]+)\"",card) or [None,""])[1]
    print("\t".join([dt,title,company,loc,"https://www.linkedin.com/jobs/view/"+key]))
'
