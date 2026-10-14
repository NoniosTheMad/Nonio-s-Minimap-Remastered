# macro {i}: announce config.events[i] now (countdown, then it fires; does not touch the event timer)
data modify storage nonios:arena tmp.evs set value []
$data modify storage nonios:arena tmp.evs append from storage nonios:arena config.events[$(i)]
execute if data storage nonios:arena tmp.evs[0] run function nonios:arena/event/fire
