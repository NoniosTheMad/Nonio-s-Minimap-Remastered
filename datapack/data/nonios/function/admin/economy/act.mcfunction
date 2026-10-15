# admin economy page (#av nx.tmp 30..49, from admin/act; the admin tag is already checked). 30 open | 47 back to the main panel
# 31/32 kill reward -/+5 | 33/34 bounty per streak kill -/+5 | 35/36 bounty min streak -/+1 | 37/38 bounty cap -/+50
# 39/40 interest at the start -/+0.5% | 41/42 interest at the end of the ramp -/+1% | 43/44 interest cap -/+5 per second | 45/46 bank range -/+1
execute if score #av nx.tmp matches 47 run return run function nonios:admin/open
execute if score #av nx.tmp matches 31 run function nonios:admin/adjust {key:"kill_reward",op:"remove",n:5,min:0,max:500}
execute if score #av nx.tmp matches 32 run function nonios:admin/adjust {key:"kill_reward",op:"add",n:5,min:0,max:500}
execute if score #av nx.tmp matches 33 run function nonios:admin/adjust {key:"bounty_per_kill",op:"remove",n:5,min:0,max:500}
execute if score #av nx.tmp matches 34 run function nonios:admin/adjust {key:"bounty_per_kill",op:"add",n:5,min:0,max:500}
execute if score #av nx.tmp matches 35 run function nonios:admin/adjust {key:"bounty_min_streak",op:"remove",n:1,min:1,max:20}
execute if score #av nx.tmp matches 36 run function nonios:admin/adjust {key:"bounty_min_streak",op:"add",n:1,min:1,max:20}
execute if score #av nx.tmp matches 37 run function nonios:admin/adjust {key:"bounty_cap",op:"remove",n:50,min:0,max:5000}
execute if score #av nx.tmp matches 38 run function nonios:admin/adjust {key:"bounty_cap",op:"add",n:50,min:0,max:5000}
execute if score #av nx.tmp matches 39 run function nonios:admin/adjust {key:"interest_start",op:"remove",n:50,min:0,max:2000}
execute if score #av nx.tmp matches 40 run function nonios:admin/adjust {key:"interest_start",op:"add",n:50,min:0,max:2000}
execute if score #av nx.tmp matches 41 run function nonios:admin/adjust {key:"interest_end",op:"remove",n:100,min:0,max:2000}
execute if score #av nx.tmp matches 42 run function nonios:admin/adjust {key:"interest_end",op:"add",n:100,min:0,max:2000}
execute if score #av nx.tmp matches 43 run function nonios:admin/adjust {key:"interest_cap_s",op:"remove",n:5,min:0,max:1000}
execute if score #av nx.tmp matches 44 run function nonios:admin/adjust {key:"interest_cap_s",op:"add",n:5,min:0,max:1000}
execute if score #av nx.tmp matches 45 run function nonios:admin/adjust {key:"bank_range",op:"remove",n:1,min:2,max:16}
execute if score #av nx.tmp matches 46 run function nonios:admin/adjust {key:"bank_range",op:"add",n:1,min:2,max:16}
function nonios:admin/economy/open
