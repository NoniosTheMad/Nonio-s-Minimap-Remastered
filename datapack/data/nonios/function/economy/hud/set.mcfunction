# with storage nonios:eco hud {team, b, r (rate text), u (unit), l, cap}
$scoreboard players display numberformat bank nx.sb_$(team) fixed {text:"$(b)",color:"gold",bold:true}
$scoreboard players display numberformat rate nx.sb_$(team) fixed {text:"$(r)",color:"aqua"}
$scoreboard players display numberformat last nx.sb_$(team) fixed {text:"+$(l)/$(u)$(cap)",color:"yellow"}
