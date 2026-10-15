# Emerald Dream portals of the match (DESIGN §2.8): one pad per field (map/gen/dream_pad), unlocked per team for
# config dream_cost coins (V2: 1000) paid from the purse at the pad. The dream itself lives in nonios:dream/*;
# this module only plugs into its hooks (#nonios:dream/gate, on_enter, on_exit, fallback_return).
# Everything here is inert until the match map exists (#map nx.state = 1), so the dream demo keeps its own rules.
# Team unlocks: #white / #black in nx.portal (1 = open), reset at match start.
scoreboard objectives add nx.portal dummy
scoreboard objectives add nx.portal_t trigger
# per player: the match and team (1 white, 2 black) they entered the dream from; a way back from another match/team is void
scoreboard objectives add nx.dmatch dummy
scoreboard objectives add nx.dteam dummy
scoreboard players add #white nx.portal 0
scoreboard players add #black nx.portal 0
execute unless data storage nonios:config dream_cost run data modify storage nonios:config dream_cost set value 1000
