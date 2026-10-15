# once a second while the arena runs: Haste for a team holding a haste node, inside its own field;
# swift / ward (spare bonuses, no node uses them by default): Speed I / Resistance I inside the Arena bounds
execute if score #haste_white nx.arena matches 1.. if data storage nonios:arena config.fields.white run function nonios:arena/bonus/haste with storage nonios:arena config.fields.white
execute if score #haste_black nx.arena matches 1.. if data storage nonios:arena config.fields.black run function nonios:arena/bonus/haste with storage nonios:arena config.fields.black
execute if score #swift_white nx.arena matches 1.. run function nonios:arena/bonus/in_arena {team:"white",effect:"speed"}
execute if score #swift_black nx.arena matches 1.. run function nonios:arena/bonus/in_arena {team:"black",effect:"speed"}
execute if score #ward_white nx.arena matches 1.. run function nonios:arena/bonus/in_arena {team:"white",effect:"resistance"}
execute if score #ward_black nx.arena matches 1.. run function nonios:arena/bonus/in_arena {team:"black",effect:"resistance"}
