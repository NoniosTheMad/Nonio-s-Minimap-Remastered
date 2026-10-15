# Emerald Talisman (V2 special 87, 200 coins): worn on the head it gives Luck +100 and pays its holder talisman_mult (3)
# times the bank interest rate applied to its own price (#111/#112: mode A 3 x 0.1%/s x 200 = 0.6 coin/s), whatever the
# mode, no bank cap, bank size irrelevant. talisman/accrue (every interest tick) pays 0.1 coin steps into the purse
# fraction (nx.pfrac, the blue decimals). Price = the shop catalog entry (storage nonios:shop items), 200 if missing.
# Curses of binding (once on, it stays on) and vanishing (gone on death). Give: function nonios:talisman/give (as the
# player). Sold by the shop from src/specials.json.
scoreboard objectives add nx.talis dummy
execute unless data storage nonios:config talisman_mult run data modify storage nonios:config talisman_mult set value 3
# the flat +1 coin every 3 s is gone (#111)
data remove storage nonios:config talisman_period
data remove storage nonios:config talisman_coins
scoreboard players reset #speed nx.talis
scoreboard players reset #t nx.talis
scoreboard players set #10 nx.talis 10
scoreboard players set #100 nx.talis 100
