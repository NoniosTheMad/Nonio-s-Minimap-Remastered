# {m1, m2, c}: result line shown at the top of the reopened dialog: "<m1><#amt><m2>" (#amt only when m2 is not empty)
$data modify storage nonios:bank msg set value {m1:"$(m1)",m2:"$(m2)",c:"$(c)",n:""}
execute unless data storage nonios:bank msg{m2:""} store result storage nonios:bank msg.n int 1 run scoreboard players get #amt nx.eco
function nonios:bank/msg_set with storage nonios:bank msg
