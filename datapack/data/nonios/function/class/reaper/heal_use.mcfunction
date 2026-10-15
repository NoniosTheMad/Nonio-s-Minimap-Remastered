# advancement nonios:class/reaper_heal: the charged scythe finished its 0.25 s use (no cooldown). Its use_remainder puts the
# dormant scythe back in that hand; the tick re-charges it while souls remain.
advancement revoke @s only nonios:class/reaper_heal
execute at @s run function nonios:class/reaper/heal
