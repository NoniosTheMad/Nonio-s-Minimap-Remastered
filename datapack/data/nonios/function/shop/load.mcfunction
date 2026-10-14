# Shop: dialog pages built from storage nonios:shop (shop/catalog, generated from src/shop.json). Buttons = /trigger nx.shop (no op prompt).
# nx.shop values: 1 = first page (section menu), 10+k = page k, 100+i = buy items[i]. nx.shop_sec = page the player is on (0 = menu, k+1 = page k).
# Opens only next to your own team's shopkeeper (shop/allowed). nx.coins = the purse.
scoreboard objectives add nx.coins dummy {"text":"Coins","color":"gold"}
scoreboard objectives add nx.shop trigger
scoreboard objectives add nx.shop_sec dummy
function nonios:shop/catalog
