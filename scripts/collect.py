"""Merge all source TSVs for a run, drop already-seen jobs and irrelevant titles.
Usage: python3 scripts/collect.py DATE  -> runs/DATE-candidates.tsv, runs/DATE-srclane.tsv"""
import re, sys
from collections import Counter
T = sys.argv[1]
seen = set(l.split('\t')[0] for l in open('data/seen.tsv'))
seen_titles = set()
for l in open('data/seen.tsv'):
    p = l.rstrip('\n').split('\t')
    if len(p) > 3: seen_titles.add((p[2].lower()[:15], re.sub(r'\W', '', p[3].lower())[:35]))
NEG = (r'verkauf|verkäufer|kassier|\bsales\b|vertrieb|marketing|social media|customer care|kundenservice|kundenberatung|chat-beratung|'
       r'recht\b|legal|tax\b|steuer|\bbau\b|baumanagement|bauleitung|\bhr\b|personal|entgelt|recruit|talent|logistik|autovermietung|design|grafik|'
       r'pflege|soziale|psycholog|frischetheke|schüler|zoll|customs|versand|mikrobiologie|buchhaltung|empfang|events?\b|content|redaktion|'
       r'duales studium|innendienst|finanzberater|versicherung|ausbildung|auszubild|gleisbau|abholservice|restaurant|senior|lead\b|principal|head of')
# "Loosely in field" (since 2026-10-28): data/IT/AI plus operations, process, digital, consulting, product/project support in tech
REL = (r'data|daten|sap|erp|analy|\bai\b|\bki\b|it-|\bit\b|informatik|machine|\bbi\b|business intelligence|reporting|software|digital|'
       r'process|prozess|research|forschung|hilfskraft|student assistant|operations|consult|berat|python|sql|automation|automatisierung|'
       r'product|produkt|project|projekt|cloud|tech|engineering|controlling|supply chain|procurement|einkauf|quality|qualität|innovation')
STUDENT = r'werkstud|working student|student|intern|praktik|hiwi|hilfskraft|trainee'
out, lane, k = [], {}, set()
def add(L, p):
    if len(p) < 5 or p[4] in seen or p[4] in k: return
    t = p[1].lower()
    if (p[2].lower()[:15], re.sub(r'\W', '', t)[:35]) in seen_titles: return
    if re.search(NEG, t) and not re.search(r'data|daten|sap|analytics|\bai\b|\bki\b|informatik', t): return
    if L in ('G', 'R') and not re.search(REL, t): return
    if L == 'G' and not re.search(STUDENT, t): return
    k.add(p[4]); out.append('\t'.join(p[:5]) + '\n'); lane[p[4]] = L
for f, L in [('careers', 'L'), ('boards-local', 'L'), ('local', 'L'), ('aa', 'L'), ('remote', 'R'), ('boards-remote', 'R'),
             ('world', 'W'), ('linkedin', 'G'), ('boards-germany', 'G')]:
    try:
        for l in open(f'runs/{T}-{f}.tsv'): add(L, l.rstrip('\n').split('\t'))
    except FileNotFoundError: pass
open(f'runs/{T}-candidates.tsv', 'w').writelines(out)
open(f'runs/{T}-srclane.tsv', 'w').writelines(f"{u}\t{L}\n" for u, L in lane.items())
print('candidates', len(out), dict(Counter(lane.values())))
