import sys,glob,os,re,csv
d=sys.argv[1]; w=csv.writer(sys.stdout,lineterminator="\n")
w.writerow(["domain","period","monthly_visits","countries_total","rank","country","share_pct","date_read"])
for f in sorted(glob.glob(d+"/*.geo.txt")):
    dom=os.path.basename(f)[:-8]; L=[l.strip() for l in open(f)]
    ov=[l.strip() for l in open(f.replace(".geo.",".ov."))] if os.path.exists(f.replace(".geo.",".ov.")) else []
    vis=""; per=""
    if "Total visits" in ov:
        i=ov.index("Total visits"); per=ov[i+1]; vis=ov[i+3]
    n=next((re.sub(r"\D","",l) for l in L if re.fullmatch(r"\(\d+\)",l)),"")
    if "Upgrade your account" not in L:
        w.writerow([dom,per,vis,n,"","","", __import__("datetime").date.today().isoformat()]); continue
    u=L.index("Upgrade your account"); names=[x for x in L[u-5:u] if not x.isdigit()]
    last=max(i for i,l in enumerate(L) if l=="Upgrade your account")
    sh=[l for l in L[last+1:] if l.endswith("%")][:len(names)]
    for k,(c,s) in enumerate(zip(names,sh),1): w.writerow([dom,per,vis,n,k,c,s,__import__("datetime").date.today().isoformat()])
