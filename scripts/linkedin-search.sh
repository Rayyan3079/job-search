#!/usr/bin/env bash
# Lists LinkedIn job postings for each keyword.
# Env: HOURS (default 72), LOCATION (default "Germany"), DISTANCE (km, optional), KWSET (germany|local|remote)
# Output: TSV  posted_iso <TAB> title <TAB> company <TAB> location <TAB> url
HOURS="${HOURS:-72}"; SECS=$((HOURS*3600)); LOCATION="${LOCATION:-Germany}"; KWSET="${KWSET:-germany}"
case "$KWSET" in
  local) KEYWORDS=("Werkstudent" "Working Student" "Studentische Hilfskraft" "Student Assistant" "Praktikum" "Internship" "Werkstudent IT" "Werkstudent Data" "Werkstudent SAP" "Werkstudent Informatik" "Abschlussarbeit Data");;
  remote) KEYWORDS=("Working Student remote" "Werkstudent remote" "Werkstudent 100% remote" "Working Student Data remote" "Werkstudent Data Analyst remote" "Working Student SAP remote" "Werkstudent SAP remote" "Working Student AI remote" "Werkstudent BI remote" "Werkstudent Home Office Data");;
  *) KEYWORDS=("Working Student" "Werkstudent English" "Working Student IT" "Working Student Operations" "Working Student Digital" "Working Student Analyst" "Internship Data" "Student Assistant" "Werkstudent SAP" "Working Student SAP" "Werkstudent SAP Analytics" "Werkstudent Business Intelligence" "Working Student Business Intelligence" "Werkstudent Data Analyst" "Working Student Data Analyst" "Working Student Data Analytics" "Werkstudent Reporting" "Werkstudent Data Science" "Working Student Data Science" "Working Student Machine Learning" "Werkstudent Machine Learning" "Working Student AI" "Werkstudent Data Engineering" "Working Student Data Engineering" "Werkstudent IT Consulting" "Working Student SAP Consulting");;
esac
EXTRA=(); [ -n "$DISTANCE" ] && EXTRA=(--data-urlencode "distance=$DISTANCE")
for kw in "${KEYWORDS[@]}"; do
  for start in 0 25; do
    curl -s -m 20 -A "Mozilla/5.0" -G "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search" \
      --data-urlencode "keywords=$kw" --data-urlencode "location=$LOCATION" "${EXTRA[@]}" \
      --data-urlencode "f_TPR=r$SECS" --data-urlencode "start=$start"
    sleep 1
  done
done | python3 -c '
import sys,re,html
data=sys.stdin.read(); seen=set()
for card in data.split("<li>"):
    url=re.search(r"href=\"(https://[a-z]+\.linkedin\.com/jobs/view/[^\"?]+)",card)
    if not url: continue
    jid=re.search(r"(\d{6,})",url.group(1)); key=jid.group(1) if jid else url.group(1)
    if key in seen: continue
    seen.add(key)
    g=lambda p: html.unescape(re.sub(r"\s+"," ",(re.search(p,card,re.S) or [None,""])[1] or "")).strip()
    title=g(r"base-search-card__title\">(.*?)</h3>")
    company=re.sub(r"<[^>]+>","",g(r"base-search-card__subtitle\">(.*?)</h4>")).strip()
    loc=g(r"job-search-card__location\">(.*?)</span>")
    dt=(re.search(r"datetime=\"([^\"]+)\"",card) or [None,""])[1]
    print("\t".join([dt,title,company,loc,"https://www.linkedin.com/jobs/view/"+key]))
'
