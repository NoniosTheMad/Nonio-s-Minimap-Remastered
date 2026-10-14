# {team}: the sidebar's fixed rows (sorted by score: 4 at the top). Values are drawn as fixed number formats by hud/set.
$scoreboard players set bank nx.sb_$(team) 4
$scoreboard players display name bank nx.sb_$(team) {text:"Bank",color:"gray"}
$scoreboard players set rate nx.sb_$(team) 3
$scoreboard players display name rate nx.sb_$(team) {text:"Interest",color:"gray"}
$scoreboard players set last nx.sb_$(team) 2
$scoreboard players display name last nx.sb_$(team) {text:"Last payout",color:"gray"}
$scoreboard players set next nx.sb_$(team) 1
$scoreboard players display name next nx.sb_$(team) {text:"Next in",color:"gray"}
