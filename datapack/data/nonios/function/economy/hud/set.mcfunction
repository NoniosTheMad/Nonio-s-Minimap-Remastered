# with storage nonios:eco hud {team, b, rw, rt, l, cap}
$scoreboard players display numberformat bank nx.sb_$(team) fixed {text:"$(b)",color:"gold",bold:true}
$scoreboard players display numberformat rate nx.sb_$(team) fixed {text:"$(rw).$(rt)%",color:"aqua"}
$scoreboard players display numberformat last nx.sb_$(team) fixed {text:"+$(l)/s$(cap)",color:"yellow"}
