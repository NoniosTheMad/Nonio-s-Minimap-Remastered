# Every tick while right-click is held on the dormant scythe (souls 0; it never finishes, so it is never used up).
# The charged scythe (souls > 0, see charge) also lands here while winding up: nothing to do then.
execute if score @s nx.cls_souls matches 1.. run return 0
execute store result score #now nx.cls_tmp run time query gametime
scoreboard players operation #d nx.cls_tmp = #now nx.cls_tmp
scoreboard players operation #d nx.cls_tmp -= @s nx.cls_nos
scoreboard players operation @s nx.cls_nos = #now nx.cls_tmp
# once per press (a held button fires every tick)
execute if score #d nx.cls_tmp matches 0..3 run return 0
function nonios:class/reaper/no_souls
