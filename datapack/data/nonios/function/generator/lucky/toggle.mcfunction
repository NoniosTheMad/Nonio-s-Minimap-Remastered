# lucky block proposal on/off (runtime switch #lucky nx.gen; config default #lucky_def from src/generators.json)
execute store success score #was nx.gen if score #lucky nx.gen matches 1
execute if score #was nx.gen matches 1 run scoreboard players set #lucky nx.gen 0
execute if score #was nx.gen matches 0 run scoreboard players set #lucky nx.gen 1
