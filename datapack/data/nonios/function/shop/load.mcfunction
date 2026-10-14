# Shop: dialog menu built from storage nonios:shop items (see shop/catalog). Buttons = /trigger nx.shop (no op prompt).
# nx.shop values: 1 = open, 100+i = buy items[i]. nx.coins = placeholder currency (coin purse spike replaces the source).
scoreboard objectives add nx.coins dummy {"text":"Coins","color":"gold"}
scoreboard objectives add nx.shop trigger
function nonios:shop/catalog
