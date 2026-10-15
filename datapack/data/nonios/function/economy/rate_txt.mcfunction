# with storage nonios:eco rt {w, f (hundredths of a percent), u}
$execute if score #rt nx.eco matches ..9 run return run data modify storage nonios:eco rtxt set value "$(w).0$(f)%/$(u)"
$data modify storage nonios:eco rtxt set value "$(w).$(f)%/$(u)"
