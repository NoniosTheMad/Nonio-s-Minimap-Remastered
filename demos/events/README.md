# events
Arena events (feedback #41 #42, branch feat/arena-v3): every event the arena can roll, one button each, on the placeholder
map. Frog rain moved here from the general demos (it is now a troll event, off in the match: `config.trolls`).

## Flow
`arena/event/random` (timer `event_every`) or `event/start {i}` -> `event/fire`: picks the node, sets `#ev_wait` =
`event_warn` (600) and shows bossbar `nonios:arena/event` ("NAME  where  Ns", counting down) + raid horn + short title.
`event/pending` (arena loop) counts down -> `event/go`: announce, run `fn`. A timed event's fn sets `#ev_run`; the bar then
shows its time left (`event/running`). `event/now {i}` skips the countdown. `arena/stop` drops a pending event.

## Events (src: arena/config `events`)
| id | where | weight | effect |
|----|-------|--------|--------|
| emerald_surge | node | 3 | 8 waves of flung emeralds |
| supply_drop | node | 3 | chest (`loot arena/supply`) falls from 24 blocks; leftovers removed on reset |
| golden_hour | arena | 2 | 60 s: centre generator x3, `#mult` 2 (interest node) |
| bounty_hunt | arena | 2 | 60 s: kills inside `bounds` +50 coins (`#nonios:economy/kill_bonus` entry `arena/event/bounty_bonus`) |
| low_gravity | arena | 2 | 45 s: jump boost III + slow falling inside `bounds` |
| frog_rain | node | 1, troll | frogs + Cracy Frog (only with `config.trolls`) |

## Buttons
1 Start + battle now, 2 Stop match, 3-14 Announce / Now for events 0-5, 15 Random event, 16 Trolls on/off,
17 Warning 5 s / 30 s, 18 Time x10, 19 Tp: arena, 20 Enemy dummy, 21 Switch team, 22 Status.
