# as player: succeeds at most once per 15 ticks (nx.msg_t = next allowed gametime). No per-tick scan.
execute store result score #now nx.const run time query gametime
execute if score @s nx.msg_t > #now nx.const run return fail
scoreboard players operation @s nx.msg_t = #now nx.const
scoreboard players add @s nx.msg_t 15
return 1
