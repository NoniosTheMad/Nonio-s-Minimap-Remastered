# #nonios:arena/config entry: trolls on (button "Trolls" flips #trolls demo.evc), optional short warning
data modify storage nonios:arena config.trolls set value 1b
execute if score #trolls demo.evc matches 0 run data modify storage nonios:arena config.trolls set value 0b
execute if score #short demo.evc matches 1 run data modify storage nonios:arena config.event_warn set value 100
