# V2 special 88 "Dragon Skull [Disabled]": listed at 3200, but the buy check wanted 3,200,000 coins and then only
# ran "say dragon". Kept as the joke it was (src/specials.json; the shop charges nothing, this decides).
execute if score @s nx.coins matches 3200000.. run return run say dragon
function nonios:shop/msg {m:"[Disabled]",c:"dark_gray"}
playsound minecraft:entity.villager.no master @s ~ ~ ~ 1 1
