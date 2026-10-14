# {team}: #s_<team> nx.purse = max(#st, 100 + average nx.earned of the team's players * 100 / w_iref), at most w_smax
$scoreboard players operation #s_$(team) nx.purse = #st nx.purse
execute unless score #state nx.state matches 1..2 run return 0
execute if score #w_iref nx.purse matches ..0 run return 0
$execute store result score #n nx.purse if entity @a[team=$(team)]
execute if score #n nx.purse matches ..0 run return 0
scoreboard players set #si nx.purse 0
$scoreboard players operation #si nx.purse += @a[team=$(team)] nx.earned
scoreboard players operation #si nx.purse /= #n nx.purse
scoreboard players operation #si nx.purse *= #100 nx.purse
scoreboard players operation #si nx.purse /= #w_iref nx.purse
scoreboard players add #si nx.purse 100
$scoreboard players operation #s_$(team) nx.purse > #si nx.purse
$scoreboard players operation #s_$(team) nx.purse < #w_smax nx.purse
