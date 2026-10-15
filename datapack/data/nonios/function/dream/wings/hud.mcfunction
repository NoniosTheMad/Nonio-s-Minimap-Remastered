# charge pips on the action bar while gliding
scoreboard players operation #c nx.dream = @s nx.dchg
scoreboard players operation #c nx.dream /= #wing_cost nx.dream
execute if score #c nx.dream matches ..0 run title @s actionbar {"text":"◇◇◇","color":"dark_gray"}
execute if score #c nx.dream matches 1 run title @s actionbar [{"text":"◆","color":"#7dffc8"},{"text":"◇◇","color":"dark_gray"}]
execute if score #c nx.dream matches 2 run title @s actionbar [{"text":"◆◆","color":"#7dffc8"},{"text":"◇","color":"dark_gray"}]
execute if score #c nx.dream matches 3.. run title @s actionbar {"text":"◆◆◆","color":"#7dffc8"}
