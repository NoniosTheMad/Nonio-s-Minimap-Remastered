# #v nx.tmp = 10 + page index -> nx.shop_sec = page index + 1 (shop/open falls back to the menu if the page is gone)
scoreboard players operation @s nx.shop_sec = #v nx.tmp
scoreboard players remove @s nx.shop_sec 9
