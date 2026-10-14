# as + at a node marker, macro (its data): delete marker, bossbar and hologram (the indicator block stays)
$bossbar remove nonios:arena/$(id)
$kill @e[type=text_display,tag=nx.node_holo,distance=..$(hy).5,sort=nearest,limit=1]
kill @s
