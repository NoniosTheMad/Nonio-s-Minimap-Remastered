# as the attacking player (#49): scale #dmg nx.const by the attack charge like vanilla, x (0.2 + 0.8 c^2), with
# c = ticks since this player's last Barrier hit / their weapon cooldown (20 / attack_speed ticks), max 1.
# Vanilla's own charge can't be read (the interaction swallows the attack before it), so spam-clicking the Barrier
# deals ~20% per click, a hit per full swing deals 100%.
execute store result score #now nx.tmp run time query gametime
scoreboard players operation #el nx.tmp = #now nx.tmp
scoreboard players operation #el nx.tmp -= @s nx.nxlast
execute unless score @s nx.nxlast = @s nx.nxlast run scoreboard players set #el nx.tmp 1000
scoreboard players operation @s nx.nxlast = #now nx.tmp
execute if score #el nx.tmp matches 1000.. run return 0
execute if score #el nx.tmp matches ..-1 run return 0
# cooldown x100 ticks = 200000 / (attack_speed x100): sword 1250 (12.5 ticks), pickaxe 1667, fist 500
execute store result score #sp nx.tmp run attribute @s minecraft:attack_speed get 100
execute if score #sp nx.tmp matches ..0 run return 0
scoreboard players set #cdt nx.tmp 200000
scoreboard players operation #cdt nx.tmp /= #sp nx.tmp
# c x1000 = elapsed x100 x1000 / cooldown x100
scoreboard players operation #c nx.tmp = #el nx.tmp
scoreboard players operation #c nx.tmp *= #100000 nx.const
scoreboard players operation #c nx.tmp /= #cdt nx.tmp
execute if score #c nx.tmp matches 1000.. run return 0
# multiplier x1000 = 200 + 800 c^2 = 200 + c*c / 1250
scoreboard players operation #c nx.tmp *= #c nx.tmp
scoreboard players operation #c nx.tmp /= #1250 nx.const
scoreboard players add #c nx.tmp 200
scoreboard players operation #dmg nx.const *= #c nx.tmp
scoreboard players operation #dmg nx.const /= #1000 nx.const
execute if score #dmg nx.const matches ..0 run scoreboard players set #dmg nx.const 1
