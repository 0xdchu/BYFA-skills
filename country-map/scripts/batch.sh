#!/bin/bash
# usage: batch.sh <queue.txt> <out.csv>
# Reads domains (one per line, highest MRR first) from queue.txt, scrapes Similarweb in the
# Orca browser until the daily limit, appends rows to out.csv and removes done domains from the queue.
H=$(cd "$(dirname "$0")" && pwd); Q=$1; OUT=$2; T=$(mktemp -d)
[ -s "$OUT" ] || echo "domain,period,monthly_visits,countries_total,rank,country,share_pct,date_read,source" > "$OUT"
while read -r d; do
  [ -z "$d" ] && continue
  "$H/sw.sh" "$T" "$d" >/dev/null
  if grep -q "Daily usage limit reached" "$T/$d".*.txt || ! grep -q "^$d$" "$T/$d.ov.txt"; then
    echo "LIMIT at $d"; break
  fi
  python3 "$H/parse.py" "$T" | tail -n +2 | grep "^$d," | sed 's|$|,Similarweb (Orca)|' >> "$OUT"
  sed -i "1{/^$d$/d}" "$Q"; rm -f "$T/$d".*; echo "OK $d"
done < <(cat "$Q")
rm -rf "$T"; echo "left: $(grep -c . "$Q")"
