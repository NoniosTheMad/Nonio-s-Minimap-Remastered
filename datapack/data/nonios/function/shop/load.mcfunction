# Shop v3: dialog screens built from storage nonios:shop (shop/catalog, generated from src/shop.json by tools/build_shop.py).
# Buttons = /trigger nx.shop (no op prompt), handled in shop/act:
#   1 home, 2 buy again, 3 prev page, 4 next page, 5 back (parent screen), 6-9 quantity x1/x8/x64/Stack, 10 redraw,
#   11-99 open screen nodes[v-10], 100+ buy items[v-100].
# Per player: nx.shop_sec screen (node), nx.shop_pg page, nx.shop_qm quantity mode (0 x1, 1 x8, 2 x64, 3 Stack),
# nx.shop_last items index + 1 of the last purchase (0 none), nx.shop_lastl its lots (buy again repeats both).
# Opens only next to your own team's shopkeeper (shop/allowed). nx.coins = the purse.
scoreboard objectives add nx.coins dummy {"text":"Coins","color":"gold"}
scoreboard objectives add nx.shop trigger
scoreboard objectives add nx.shop_sec dummy
scoreboard objectives add nx.shop_pg dummy
scoreboard objectives add nx.shop_qm dummy
scoreboard objectives add nx.shop_last dummy
scoreboard objectives add nx.shop_lastl dummy
scoreboard players set #8 nx.const 8
scoreboard players set #64 nx.const 64
function nonios:shop/catalog
function nonios:shop/ui/controls
