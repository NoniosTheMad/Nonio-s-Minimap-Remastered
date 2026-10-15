# Every tick (nonios:tick; one score check while the arena is off): the event bossbar slides smoothly (announce
# countdown, then a timed event's time left) and the enemy events (event/mob) run.
execute unless score #on nx.arena matches 1 run return 0
execute if score #ev_wait nx.arena matches 1.. run function nonios:arena/event/bar_tick {v:"#ev_wait",n:"bar_name"}
execute unless score #ev_wait nx.arena matches 1.. if score #ev_run nx.arena matches 1.. run function nonios:arena/event/bar_tick {v:"#ev_run",n:"bar_left"}
execute if score #mob_ev nx.arena matches 1.. run function nonios:arena/event/mob/tick
