# Shop: dialog menu built from storage nonios:shop items (see shop/catalog). Buttons = /trigger nx.shop (no op prompt).
# nx.shop values: 1 = open, 100+i = buy items[i]. Opens only next to your own team's shopkeeper (shop/allowed). nx.coins = the purse.
scoreboard objectives add nx.coins dummy {"text":"Coins","color":"gold"}
scoreboard objectives add nx.shop trigger
function nonios:shop/catalog
