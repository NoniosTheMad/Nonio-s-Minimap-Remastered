# one line right above the buttons: purse, then the result of the last click (ui.msg, a text component list)
execute store result storage nonios:shop ui.t.bal int 1 run scoreboard players get #bal nx.tmp
function nonios:shop/ui/body_line with storage nonios:shop ui.t
execute if data storage nonios:shop ui.msg run data modify storage nonios:shop ui.d.body[0].contents append value {text:"    "}
execute if data storage nonios:shop ui.msg run data modify storage nonios:shop ui.d.body[0].contents append from storage nonios:shop ui.msg[]
