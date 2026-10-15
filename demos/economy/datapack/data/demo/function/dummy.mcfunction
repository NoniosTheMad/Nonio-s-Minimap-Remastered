# an enemy-team husk 4 blocks in front of you. Dummies count as alive team members for the win check.
function demo:enemy
$summon minecraft:husk ^ ^ ^4 {$(ai)Tags:["nx.dummy","demo.new"],PersistenceRequired:1b,CustomNameVisible:1b,CustomName:{text:"$(n)",color:"red"}}
function demo:join_new with storage demo:tmp
$tellraw @s {"text":"[demo] $(n) spawned on the enemy team.","color":"yellow"}
