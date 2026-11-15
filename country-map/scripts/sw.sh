#!/bin/bash
# usage: sw.sh outdir domain...
out=$1; shift
for d in "$@"; do
  orca goto --url "https://pro.similarweb.com/#/digitalsuite/websiteanalysis/website-audience/*/999/3m?webSource=Total&key=$d&selectedTab=geography" >/dev/null 2>&1
  sleep 14
  orca eval --expression "document.body.innerText" > "$out/$d.geo.txt" 2>&1
  orca goto --url "https://pro.similarweb.com/#/digitalsuite/websiteanalysis/overview/website-performance/*/999/3m?webSource=Total&key=$d" >/dev/null 2>&1
  sleep 14
  orca eval --expression "document.body.innerText" > "$out/$d.ov.txt" 2>&1
  echo "$d $(wc -c < $out/$d.geo.txt) $(grep -m1 -A3 'Total visits' $out/$d.ov.txt | tail -1)"
done
