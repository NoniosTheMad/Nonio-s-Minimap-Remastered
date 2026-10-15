# the event timers just moved (arena loop / a new bar): event/bar_tick measures its slide from now, renames next tick
execute store result score #ev_gt nx.arena run time query gametime
scoreboard players set #ev_lsec nx.arena -1
