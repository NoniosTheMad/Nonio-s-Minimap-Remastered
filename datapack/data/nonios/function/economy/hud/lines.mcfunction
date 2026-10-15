# {team}: the sidebar's fixed rows (sorted by score: 3 at the top). Values are drawn as fixed number formats by hud/set,
# so a redraw every second changes only the right-hand text (no row reordering, no flicker).
$scoreboard players reset next nx.sb_$(team)
$scoreboard players set bank nx.sb_$(team) 3
$scoreboard players display name bank nx.sb_$(team) {text:"Bank",color:"gray"}
$scoreboard players set rate nx.sb_$(team) 2
$scoreboard players display name rate nx.sb_$(team) {text:"Interest",color:"gray"}
$scoreboard players set last nx.sb_$(team) 1
$scoreboard players display name last nx.sb_$(team) {text:"Income",color:"gray"}
