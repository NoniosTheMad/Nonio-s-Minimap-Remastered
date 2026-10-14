# current interest terms from the match clock: #rate nx.eco (permille), #icap nx.eco (coins per payout, 0 = no cap),
# #rw / #rt nx.eco = the rate as "<rw>.<rt>%". Outside a match: the starting values.
scoreboard players set #emin nx.eco 0
execute if score #state nx.state matches 1..2 store result score #emin nx.eco run time query gametime
execute if score #state nx.state matches 1..2 run scoreboard players operation #emin nx.eco -= #t0 nx.eco
scoreboard players operation #emin nx.eco /= #20 nx.eco
scoreboard players operation #emin nx.eco /= #60 nx.eco
execute if score #emin nx.eco matches ..-1 run scoreboard players set #emin nx.eco 0
execute store result score #rate nx.eco run data get storage nonios:config interest_grow
scoreboard players operation #rate nx.eco *= #emin nx.eco
execute store result score #c nx.eco run data get storage nonios:config interest_rate
scoreboard players operation #rate nx.eco += #c nx.eco
execute store result score #c nx.eco run data get storage nonios:config interest_rate_max
execute if score #c nx.eco matches 1.. run scoreboard players operation #rate nx.eco < #c nx.eco
execute store result score #icap nx.eco run data get storage nonios:config interest_cap
execute store result score #c nx.eco run data get storage nonios:config interest_cap_grow
scoreboard players operation #c nx.eco *= #emin nx.eco
execute if score #icap nx.eco matches 1.. run scoreboard players operation #icap nx.eco += #c nx.eco
scoreboard players operation #rw nx.eco = #rate nx.eco
scoreboard players operation #rw nx.eco /= #10 nx.eco
scoreboard players operation #rt nx.eco = #rate nx.eco
scoreboard players operation #rt nx.eco %= #10 nx.eco
