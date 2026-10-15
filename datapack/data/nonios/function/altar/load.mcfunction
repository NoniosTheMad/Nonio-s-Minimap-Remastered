# Team offering altar (V2 "Offerings"): one per field (map/config <team>.altar, built by map/gen/altar). Teammates bring
# blocks of iron / gold / diamond; once a step is fully paid the team's basic-class level (#<team> nx.cls_lvl) goes up.
# Right-click the altar (interaction nx.altar_npc -> advancement nonios:altar/click) = hand over what the next step still
# needs, straight from the inventory (never more). Paid blocks are kept per team in nx.altar (#<team>_iron/_gold/_diamond).
# config altar_steps[k] = the cost of reaching level k+1 (V2 Kit I/II/III = 8/8/2, 16/16/8, 64/64/64). Teams start at
# level 1 (= V2 Kit I, game/start), so the first offering of a match pays steps[1]. Max level = length of the list.
scoreboard objectives add nx.altar dummy
execute unless data storage nonios:config altar_steps run data modify storage nonios:config altar_steps set value [{iron:8,gold:8,diamond:2},{iron:16,gold:16,diamond:8},{iron:64,gold:64,diamond:64}]
scoreboard players add #white_iron nx.altar 0
scoreboard players add #white_gold nx.altar 0
scoreboard players add #white_diamond nx.altar 0
scoreboard players add #black_iron nx.altar 0
scoreboard players add #black_gold nx.altar 0
scoreboard players add #black_diamond nx.altar 0
