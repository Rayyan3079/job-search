"""Sort fetched job descriptions into lanes and flag language.
Usage: python3 scripts/lanes.py runs/jd-cache-DATE  -> TSV: file lane lang german_req remote applicants company title loc url
lane: local (commutable from Ilmenau) | remote (posting says fully remote) | germany (on-site elsewhere)"""
import sys, glob, re
LOCAL = r"\b(ilmenau|erfurt|arnstadt|gotha|weimar|jena|suhl|schmalkalden|zella-mehlis|rudolstadt|saalfeld|s[öo]mmerda|apolda|ohrdruf|eisenach|bad berka|stadtilm|plaue|gehren|langewiesen|großbreitenbach|neuhaus am rennweg|meiningen|hildburghausen)\b"
REMOTE = r"(100\s?%\s?(remote|home[- ]?office|mobil)|fully remote|full[- ]remote|remote[- ]first|remote-only|100% remote|komplett remote|vollständig remote|ortsunabhängig|deutschlandweit remote|remote \(germany\)|work from anywhere in germany|\(remote\))"
GREQ = r"((sehr gute|gute|sichere|fließende|verhandlungssichere|ausgezeichnete|hervorragende)[^.\n]{0,25}deutsch|deutsch[^.\n]{0,40}(c1|b2|fließend|verhandlungssicher|muttersprach|sehr gut)|(fluent|excellent|very good|good|business[- ]fluent|proficient)[^.\n]{0,25}german\b|german[^.\n]{0,25}(c1|b2|fluent|required|native)|both german and english|german and english)"
for f in sorted(glob.glob(sys.argv[1].rstrip('/') + '/[0-9][0-9][0-9].txt')):
    t = open(f).read(); h = dict(re.findall(r'^(URL|TITLE|COMPANY|LOC|POSTED|applicants): (.*)$', t, re.M))
    low = t.lower(); body = t.split('---', 1)[-1].lower()
    en = len(re.findall(r'\b(the|and|you|with|our)\b', body)); de = len(re.findall(r'\b(und|die|der|du|mit|wir)\b', body))
    loc = h.get('LOC', '').lower()
    remote = bool(re.search(REMOTE, low)) or bool(re.search(REMOTE, h.get('TITLE','').lower()))
    lane = 'local' if re.search(LOCAL, loc) and 'walldorf' not in loc else ('remote' if remote else 'germany')
    greq = bool(re.search(GREQ, low)) and not re.search(r'german (is|as|would be) (a |an )?(plus|advantage|asset|beneficial|nice)|deutsch(kenntnisse)? (sind|ist|wären)? ?(von vorteil|ein plus|wünschenswert)', low)
    print('\t'.join([f.split('/')[-1], lane, 'EN' if en > de else 'DE', 'GERMAN-REQ' if greq else '-', 'REMOTE' if remote else '-', h.get('applicants',''), h.get('COMPANY',''), h.get('TITLE',''), h.get('LOC',''), h.get('URL','')]))
