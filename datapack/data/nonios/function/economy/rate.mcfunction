# current interest terms from the match clock (bank v4, #47): #rate nx.eco (basis points per second, 100 = 1%),
# #icap nx.eco (coins per second, 0 = no cap), #esec / #emin nx.eco = match seconds / minutes,
# #rw / #rt nx.eco = the rate as "<rw>.<rt>%" (one decimal). Outside a match: the starting values.
scoreboard players set #esec nx.eco 0
execute if score #state nx.state matches 1..2 store result score #esec nx.eco run time query gametime
execute if score #state nx.state matches 1..2 run scoreboard players operation #esec nx.eco -= #t0 nx.eco
scoreboard players operation #esec nx.eco /= #20 nx.eco
execute if score #esec nx.eco matches ..-1 run scoreboard players set #esec nx.eco 0
scoreboard players operation #emin nx.eco = #esec nx.eco
scoreboard players operation #emin nx.eco /= #60 nx.eco
# rate = start + (end - start) * min(esec, ramp) / ramp
execute store result score #rate nx.eco run data get storage nonios:config interest_start
execute store result score #c nx.eco run data get storage nonios:config interest_end
scoreboard players operation #c nx.eco -= #rate nx.eco
execute store result score #ramp nx.eco run data get storage nonios:config interest_ramp
execute if score #ramp nx.eco matches ..0 run scoreboard players set #ramp nx.eco 1
scoreboard players operation #s nx.eco = #esec nx.eco
scoreboard players operation #s nx.eco < #ramp nx.eco
scoreboard players operation #c nx.eco *= #s nx.eco
scoreboard players operation #c nx.eco /= #ramp nx.eco
scoreboard players operation #rate nx.eco += #c nx.eco
execute if score #rate nx.eco matches ..-1 run scoreboard players set #rate nx.eco 0
# 20%/s ceiling keeps bank x rate inside an int (bank/interest/team)
execute if score #rate nx.eco matches 2001.. run scoreboard players set #rate nx.eco 2000
execute store result score #icap nx.eco run data get storage nonios:config interest_cap_s
scoreboard players operation #rw nx.eco = #rate nx.eco
scoreboard players operation #rw nx.eco /= #100 nx.eco
scoreboard players operation #rt nx.eco = #rate nx.eco
scoreboard players operation #rt nx.eco %= #100 nx.eco
scoreboard players operation #rt nx.eco /= #10 nx.eco
