# (re)start the interest clock: next payout in interest_period seconds (#int_at nx.eco = its gametime, shown in the bank dialog)
execute store result score #iper nx.eco run data get storage nonios:config interest_period
execute if score #iper nx.eco matches ..0 run scoreboard players set #iper nx.eco 60
execute store result storage nonios:eco arm.t int 1 run scoreboard players get #iper nx.eco
execute store result score #int_at nx.eco run time query gametime
scoreboard players operation #iper nx.eco *= #20 nx.eco
scoreboard players operation #int_at nx.eco += #iper nx.eco
function nonios:bank/interest/schedule with storage nonios:eco arm
