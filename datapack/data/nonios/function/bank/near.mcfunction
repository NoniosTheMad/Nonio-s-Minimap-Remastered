# succeeds if @s is within config bank_range of their own team's bank (marker nx.bank_zone + nx.<team>)
function nonios:bank/near_at with storage nonios:config
return run scoreboard players get #near nx.eco
