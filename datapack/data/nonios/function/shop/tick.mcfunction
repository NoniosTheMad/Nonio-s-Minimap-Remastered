execute as @a[scores={nx.shop=1..}] at @s run function nonios:shop/act
# enable last, every tick (never 'reset @a' after this: it would re-lock the trigger)
scoreboard players enable @a nx.shop
