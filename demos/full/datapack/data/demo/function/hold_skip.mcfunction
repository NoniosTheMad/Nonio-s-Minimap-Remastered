# +4 min of continuous hold for whoever holds the centre now
execute if score #hold_white nx.nxs matches 1.. run scoreboard players add #hold_white nx.nxs 240
execute if score #hold_black nx.nxs matches 1.. run scoreboard players add #hold_black nx.nxs 240
tellraw @s [{"text":"[demo] Centre held for (s) W ","color":"yellow"},{"score":{"name":"#hold_white","objective":"nx.nxs"},"color":"white"},{"text":" / B ","color":"yellow"},{"score":{"name":"#hold_black","objective":"nx.nxs"},"color":"white"},{"text":" (full rate at ","color":"yellow"},{"score":{"name":"#press_ramp","objective":"nx.const"},"color":"white"},{"text":")","color":"yellow"}]
