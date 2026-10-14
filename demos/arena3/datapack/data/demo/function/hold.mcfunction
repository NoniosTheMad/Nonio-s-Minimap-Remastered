# simulated centre owner: off -> White -> Black -> off (overrides the real node; the ramp restarts on each change)
scoreboard players set #on nx.nxs 1
scoreboard players add #sim nx.nxs 1
execute if score #sim nx.nxs matches 3.. run scoreboard players set #sim nx.nxs 0
execute if score #sim nx.nxs matches 0 run tellraw @s {"text":"[demo] Centre hold simulation off (the real centre node counts).","color":"yellow"}
execute if score #sim nx.nxs matches 1 run tellraw @s {"text":"[demo] White holds the centre: the Black Barrier drains, ramping up over 5 min.","color":"yellow"}
execute if score #sim nx.nxs matches 2 run tellraw @s {"text":"[demo] Black holds the centre: the White Barrier drains, ramping up over 5 min.","color":"yellow"}
