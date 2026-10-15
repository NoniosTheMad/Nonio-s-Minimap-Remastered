# advancement nonios:class/reaper_burst: the charged scythe finished its 0.5 s use. Its use_remainder puts the dormant
# scythe back in that hand (same slot, no flicker) and the use applies the 8 s cooldown to both.
advancement revoke @s only nonios:class/reaper_burst
execute at @s run function nonios:class/reaper/release
