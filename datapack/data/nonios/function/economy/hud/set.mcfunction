# with storage nonios:eco hud {team, b, rw, rt, l, cap, n}
$scoreboard players display numberformat bank nx.sb_$(team) fixed {text:"$(b)",color:"gold",bold:true}
$scoreboard players display numberformat rate nx.sb_$(team) fixed {text:"$(rw).$(rt)%",color:"aqua"}
$scoreboard players display numberformat last nx.sb_$(team) fixed {text:"+$(l)$(cap)",color:"yellow"}
$scoreboard players display numberformat next nx.sb_$(team) fixed {text:"$(n)s",color:"white"}
