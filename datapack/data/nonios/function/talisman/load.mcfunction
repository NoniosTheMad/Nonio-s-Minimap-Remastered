# Emerald Talisman (V2 special 87, 200 coins): worn on the head it gives Luck +100 and pays talisman_coins every
# talisman_period seconds (prep + battle; V2: +1 coin per shop clock pulse). Curse of binding: once on, it stays on.
# Give: function nonios:talisman/give (as the player). Sold by the shop from src/specials.json.
# #speed nx.talis = time multiplier for demos (period counts down #speed seconds per second).
scoreboard objectives add nx.talis dummy
execute unless score #speed nx.talis matches 1.. run scoreboard players set #speed nx.talis 1
execute unless data storage nonios:config talisman_period run data modify storage nonios:config talisman_period set value 3
execute unless data storage nonios:config talisman_coins run data modify storage nonios:config talisman_coins set value 1
