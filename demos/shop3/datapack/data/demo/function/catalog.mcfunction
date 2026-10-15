# swap the shop catalog: stress (362 extra items in nested categories) or the real one
$function $(f)
scoreboard players set @a nx.shop_sec 0
scoreboard players set @a nx.shop_pg 0
scoreboard players reset @a nx.shop_last
$tellraw @s {"text":"[demo] Catalog: $(m).","color":"yellow"}
