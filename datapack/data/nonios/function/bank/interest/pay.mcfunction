# one interest payout for both team banks (also the demo's "fast-forward interest")
execute store result score #rate nx.eco run data get storage nonios:config interest_rate
execute store result score #icap nx.eco run data get storage nonios:config interest_cap
scoreboard players operation #rw nx.eco = #rate nx.eco
scoreboard players operation #rw nx.eco /= #10 nx.eco
scoreboard players operation #rt nx.eco = #rate nx.eco
scoreboard players operation #rt nx.eco %= #10 nx.eco
function nonios:bank/interest/team {team:"white"}
function nonios:bank/interest/team {team:"black"}
