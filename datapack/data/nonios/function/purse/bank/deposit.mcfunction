# Team bank (user, 2026-10-14): the whole purse goes into #<team> nx.bank (safe, weightless). No withdraw yet (M3).
$scoreboard players operation #$(team) nx.bank += @s nx.coins
$tellraw @a[team=$(team)] [{"selector":"@s","color":"green"},{"text":" deposited ","color":"green"},{"score":{"name":"@s","objective":"nx.coins"},"color":"yellow","bold":true},{"text":" coins. Team bank: ","color":"green"},{"score":{"name":"#$(team)","objective":"nx.bank"},"color":"yellow"}]
$execute unless entity @s[team=$(team)] run tellraw @s [{"text":"Deposited ","color":"green"},{"score":{"name":"@s","objective":"nx.coins"},"color":"yellow","bold":true},{"text":" coins. Bank: ","color":"green"},{"score":{"name":"#$(team)","objective":"nx.bank"},"color":"yellow"}]
execute at @s run playsound minecraft:block.note_block.chime player @s ~ ~ ~ 1 1.4
scoreboard players set @s nx.coins 0
