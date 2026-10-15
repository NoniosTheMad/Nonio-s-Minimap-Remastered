# barrier clock to battle minute 20: from now both Barriers lose 10% of their max per minute (down at minute 30)
scoreboard players set #on nx.nxs 1
scoreboard players operation #bsec nx.nxs = #decay_min nx.const
scoreboard players operation #bsec nx.nxs *= #60 nx.const
tellraw @s [{"text":"[demo] Barrier clock at minute ","color":"yellow"},{"score":{"name":"#decay_min","objective":"nx.const"},"color":"white"},{"text":": both Barriers now decay (","color":"yellow"},{"score":{"name":"#decay_pm","objective":"nx.const"},"color":"white"},{"text":" per mille of max / min).","color":"yellow"}]
