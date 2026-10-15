# +60 s of interest in the live mode, then redraw
execute unless score #state nx.state matches 1..2 run return run function demo:im/open
scoreboard players set #demo_n nx.eco 60
function demo:interest_loop
function nonios:economy/hud/second
function demo:im/open
