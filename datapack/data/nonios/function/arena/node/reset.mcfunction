# as + at a node marker: back to neutral, payout timer restarted
scoreboard players set @s nx.ar_cap 0
scoreboard players set @s nx.ar_own 0
scoreboard players operation @s nx.ar_t = @s nx.ar_iv
scoreboard players set #st nx.arena 0
scoreboard players set #sgn nx.arena 0
function nonios:arena/node/restyle
scoreboard players set #abs nx.arena 0
function nonios:arena/node/bar with entity @s data
