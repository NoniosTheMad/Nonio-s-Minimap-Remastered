# with storage nonios:purse hn {p,t}: the purse fraction, light blue, right after the whole coins
$execute if score #hz nx.purse matches 0 run return run data modify storage nonios:purse hud.f set value ',{"text":".$(t)","color":"#6FB7FF"}'
$execute if score #hp nx.purse matches ..9 run return run data modify storage nonios:purse hud.f set value ',{"text":".0$(p)","color":"#6FB7FF"}'
$data modify storage nonios:purse hud.f set value ',{"text":".$(p)","color":"#6FB7FF"}'
