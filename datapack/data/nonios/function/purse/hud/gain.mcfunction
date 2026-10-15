# with storage nonios:purse hn {w whole, p,t fraction, c colour, b bold}
$execute if score #hp nx.purse matches 0 run return run data modify storage nonios:purse hud.g set value ',{"text":"  +$(w)","color":"$(c)","bold":$(b)}'
$execute if score #hz nx.purse matches 0 run return run data modify storage nonios:purse hud.g set value ',{"text":"  +$(w).$(t)","color":"$(c)","bold":$(b)}'
$execute if score #hp nx.purse matches ..9 run return run data modify storage nonios:purse hud.g set value ',{"text":"  +$(w).0$(p)","color":"$(c)","bold":$(b)}'
$data modify storage nonios:purse hud.g set value ',{"text":"  +$(w).$(p)","color":"$(c)","bold":$(b)}'
