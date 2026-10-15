# as a dreamer whose chest item has no Dream Wings yet: make it glide (elytra already do) and add the boost enchantment
execute unless items entity @s armor.chest minecraft:elytra run item modify entity @s armor.chest nonios:dream/glide
item modify entity @s armor.chest nonios:dream/wing
playsound minecraft:item.armor.equip_elytra player @s ~ ~ ~ 0.6 1.4
