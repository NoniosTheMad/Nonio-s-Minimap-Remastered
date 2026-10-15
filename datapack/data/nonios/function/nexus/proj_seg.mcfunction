# closest approach of the segment P -> P + M to the centre (inputs x100): t = clamp(D.M / M.M, 0, 1) (x1000),
# #d2 = |t M - D|^2 (x10000), #mm = M.M (x10000).
scoreboard players operation #mm nx.tmp = #mx nx.tmp
scoreboard players operation #mm nx.tmp *= #mx nx.tmp
scoreboard players operation #q nx.tmp = #my nx.tmp
scoreboard players operation #q nx.tmp *= #my nx.tmp
scoreboard players operation #mm nx.tmp += #q nx.tmp
scoreboard players operation #q nx.tmp = #mz nx.tmp
scoreboard players operation #q nx.tmp *= #mz nx.tmp
scoreboard players operation #mm nx.tmp += #q nx.tmp
scoreboard players set #t nx.tmp 0
execute if score #mm nx.tmp matches 1.. run function nonios:nexus/proj_t
scoreboard players operation #qx nx.tmp = #mx nx.tmp
scoreboard players operation #qx nx.tmp *= #t nx.tmp
scoreboard players operation #qx nx.tmp /= #1000 nx.const
scoreboard players operation #qx nx.tmp -= #dx nx.tmp
scoreboard players operation #qy nx.tmp = #my nx.tmp
scoreboard players operation #qy nx.tmp *= #t nx.tmp
scoreboard players operation #qy nx.tmp /= #1000 nx.const
scoreboard players operation #qy nx.tmp -= #dy nx.tmp
scoreboard players operation #qz nx.tmp = #mz nx.tmp
scoreboard players operation #qz nx.tmp *= #t nx.tmp
scoreboard players operation #qz nx.tmp /= #1000 nx.const
scoreboard players operation #qz nx.tmp -= #dz nx.tmp
scoreboard players operation #d2 nx.tmp = #qx nx.tmp
scoreboard players operation #d2 nx.tmp *= #qx nx.tmp
scoreboard players operation #q nx.tmp = #qy nx.tmp
scoreboard players operation #q nx.tmp *= #qy nx.tmp
scoreboard players operation #d2 nx.tmp += #q nx.tmp
scoreboard players operation #q nx.tmp = #qz nx.tmp
scoreboard players operation #q nx.tmp *= #qz nx.tmp
scoreboard players operation #d2 nx.tmp += #q nx.tmp
