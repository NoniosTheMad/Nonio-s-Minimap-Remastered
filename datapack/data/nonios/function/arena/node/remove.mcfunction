# as + at a node marker, macro (its data): delete marker and bossbar (+ a hologram left by an older version)
$bossbar remove nonios:arena/$(id)
kill @e[type=text_display,tag=nx.node_holo,distance=..12]
kill @s
