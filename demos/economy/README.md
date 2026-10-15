# economy
M3 economy, testable solo: team bank dialog, interest, kill rewards with killstreak bounties. The game pack does the work;
this demo adds test buttons (G > "Demo: Economy") and builds the placeholder map on first load.

Game code (datapack/data/nonios):
- `bank/`: vault on each team's gold pad (`map/gen/bank`: block_display vault + interaction `nx.bank_npc`, advancement `bank/click`).
  Dialog built in storage `nonios:bank ui.d`: purse, team bank, interest line; `number_range` sliders `dep`/`wd` +
  `dynamic/run_command` -> `/trigger nx.bankd|nx.bankw set $(dep|wd)`; "all" buttons -> `/trigger nx.bankt set 2|3`; open = `nx.bankt 1`.
  Every request re-checks: own team's vault within `bank_range`, match in prep/battle (`bank/allowed`, reasons in `#why nx.eco`).
- `bank/interest/`: `schedule` loop every `interest_period` s; pays `interest_rate` permille (max `interest_cap`) in prep/battle,
  fractional remainder carried per team (`#acc_<team> nx.eco`). Re-armed at match start and when the admin changes the period.
- `economy/kill/`: advancement `economy/kill` (player_killed_entity, type player) -> reward = `kill_reward` + bounty
  (victim streak >= `bounty_min_streak`: streak x `bounty_per_kill`, max `bounty_cap`) + `#nonios:economy/kill_bonus` (runs as the victim,
  adds to `#bonus nx.eco`; default entry = tier bonus by the victim's `nx.tier`, config `tier_bonus` [0,20,90,190]).
  The purse transfer stays in `purse/death/take` (not counted again). Actionbar the next tick lists kill/bounty/bonus/purse.
  Streak (`nx.streak`) ends on any death (`economy/died` from `nonios:death`). Dummies (`game/dummy_killed`) use `#dummy nx.streak/nx.tier`.
- `admin/economy/`: G > Nonios's Map > Admin panel > Economy... (all values above + bank range).

Economy v3 (feat/econ-v3, feedback #35 #36 #41):
- Yields: `src/yields.json` -> `tools/build_yields.py` -> `purse/gen/yields` (table, hundredths of a coin, versioned) + `purse/gen/check`.
  `purse/mine/award`: N * value * (100 + Fortune level * fortune_pct) / 100 into `nx.pfrac`, whole coins to the purse (debt first).
  `purse/mine/placed`: placing costs the value at Fortune `fortune_max` (#place_mult), from `nx.pfrac` then the purse, rest = `nx.pdebt`.
- Weight: `purse/scale` every second: money scale S per team = min(max(100 + w_grow * minutes, 100 + team avg `nx.earned` * 100 / w_iref), w_smax);
  `purse/weight` weighs coins * 100 / S (config in nx.purse: #w_free #w_num #w_den #w_cap #w_grow #w_iref #w_smax).
- Interest: `economy/rate` = min(interest_rate + interest_grow * minutes, interest_rate_max) permille, cap interest_cap + interest_cap_grow * minutes.
  No chat: team sidebar `economy/hud` (objectives nx.sb_white / nx.sb_black on sidebar.team.white / .dark_purple, fixed number formats).
- Bank dialog: fixed layout, greyed buttons (`storage nonios:bank off`, no action). Altar hologram icons: plain list root (no inherited tint).
- Demo buttons 16 ore wall + pickaxes, 17 match clock +5 min (#t0 nx.eco -= 6000), 18 status readout, 19 altar + offering blocks.

Bank v4 (feat/bank-v4, feedback #47; replaces the bank dialog sliders and the 60 s interest loop above):
- Deposit = contact: `map/gen/bank` puts 8 `light_weighted_pressure_plate`s around the vault. `bank/pad/tick` (every tick from
  `economy/tick`) fires `bank/pad/enter` once when a player steps onto a plate within 2.6 of a `nx.bank_zone` marker (tag `nx.bk.on`
  until they step off). Own team + prep/battle -> `bank/pad/deposit`: whole purse to the bank; depositor subtitle + sounds + particles,
  team chat line + chime, enemy team actionbar "<Team> banked N" + bell. Other team's pad: vault reject sound.
- Withdraw = vault dialog (`bank/open`): body purse / bank / interest; fixed buttons 10 50 100 200 500 1000 (`nx.bankw set N`),
  Half (`nx.bankt 4`), All (`nx.bankt 3`); greyed (no action, tooltip) when the bank holds less. A stale click larger than the bank is refused.
  Teammates get an actionbar line. Trigger `nx.bankd` removed.
- Interest: paid every second from `economy/tick` (prep + battle). `economy/rate`: rate (basis points) = interest_start +
  (interest_end - interest_start) * min(match s, interest_ramp) / interest_ramp (100 -> 1000 over 1800 s), cap interest_cap_s (20) coins/s.
  Fractions carried in `#acc_<team> nx.eco` (1/10000 coin); a capped second drops its remainder. No sound. Sidebar rows Bank / Interest / Income.
- Demo: "Interest: +60 s" pays 60 seconds at once; Status shows the carried fractions.

Bank v3 (feat/bank-v3, feedback #94; replaces the bank v4 pad and once-a-second payout above):
- Deposit = presence: `map/gen/bank` lays a 5x5 floor (raw gold rim, gold blocks inside) around the vault, no plates.
  `bank/zone/tick` (every tick) tags players inside a box over it (marker nx.bank_zone, `dx=4,dy=3,dz=4` from the rim corner,
  floor up to 4 blocks) with `nx.bk.in`; entering fires `bank/zone/enter` once (`nx.bk.on` until you leave), so walking,
  jumping or flying through deposits and withdrawing while inside never re-deposits. Cues unchanged (`bank/zone/deposit`);
  ambient wax_on glint over each floor once a second.
- Interest = smooth: `bank/interest/tick` every tick in prep/battle; per team #i = min(bank,1e6) x rate (1/10000 coin per s),
  capped at icap x 10000; `#acc_<team>` += #i, pays 1 coin per 200000 (so +1 every 20/N ticks; 20/s cap = +1 every tick).
  Same rate maths as v4. `bank/interest/pay` = 20 ticks (the demo's +60 s). Sidebar Bank row redraws on change every tick (`economy/hud/bank`).

Purse decimals (#107): the actionbar coin line shows `nx.pfrac` (hundredths) in light blue after the whole coins (`purse/show`,
pieces built in storage `nonios:purse hud` by `purse/hud/*`). `purse/gain` (every tick) compares coins x 100 + pfrac with the last
tick (`nx.ptot`); a rise shows "+N.NN" fading over 30 ticks (`nx.pgain`, `nx.ptime`). The bank only ever moves whole coins
(deposit takes `nx.coins`; the fraction stays in the purse).

Interest #108 (data-driven, storage nonios:config, `economy/load`): `interest_period` (60 = per minute), `interest_curve`
points {t: match s, r: ppm per period} joined by a monotone cubic (`bank/curve/build` tangents at load, `bank/curve/eval`),
`interest_base` (2000: only that much of the bank earns), `interest_scale` %. Defaults 0% -> 0.5% (10 min) -> 1% (20) -> 2% (30),
max 40 coins/min. Paid +1 at a time: per tick acc += min(bank, base) x ppm, a coin per period-ticks x 1e6. Text `nonios:eco rtxt`.
Admin page: base -/+500, curve x -/+25%, per second / per minute.

## #109: generators
Single block (gilded blackstone) is the default style; mined, it regrows the same tick (generator/tick). Upgrades only change the loot pool. Interaction 2.02 high so its top face wins the pick over the base: top click opens the upgrade dialog, the block on it stays mineable.

## #110: interest modes
`interest_mode` in storage nonios:config (economy/load): 1 = A (default, recommended) `interest_a_rate` 1000 ppm per second
on the bank, at most `interest_a_cap` coins/s (curve, 1/1000 coin: 0 -> 1 at min 10 -> 5 at min 20 -> 20 at min 30);
2 = B `interest_curve` per `interest_period`, no base (ppm and threshold / 100, `#idiv`, so huge banks fit); 3 = C the #108
scheme (curve on <= `interest_base`). `bank/curve/build` builds both curves; `bank/curve/eval_cap` swaps the cap curve in.
Demo picker `demo:im/open` (trigger 20-32): modes A/B/C (live, marked), match clock 0/10/20/30 min, team bank 500/2000/10000,
+60 s; body = each mode's coins/s now and x60 for one minute.

## #111 + mode A chosen
A is the default (`interest_av` 2 migrates older worlds to A and the new cap). Cap points 0 / 1 / 5 / 20 / 35 / 50 coins/s at
min 0 / 10 / 20 / 30 / 40 / 50, then `interest_a_grow` (+1/s) per minute with no ceiling (`bank/curve/eval_cap`; the last
tangent is set to that slope so the curve stays smooth). B and C stay selectable in the demo picker only (reference).
Talisman: `bank/interest/team` hands each tick's interest (#i) to `talisman/accrue`, which adds it `talisman_mult` (3) times to
`#tacc_<team> nx.talis` and pays every head-wearing holder of that team 0.1 coin per `#tth` (= #ithr / 10) into `nx.pfrac`
(`talisman/pay`; blue decimals + gain popup). The flat +1 / 3 s payout (`talisman/second`, `talisman_period/coins`) is gone.
Item: binding + vanishing curse. Picker body: "Talisman x3 = N/s" for the live mode. Clock row 2: 40 / 50 / 60 / 90 min.

## #112: talisman on its price
Correction of #111: the talisman earns talisman_mult x the live interest rate on its own price (shop catalog price, 200),
not on the team bank: mode A 3 x 0.1%/s x 200 = 0.6 coin/s, no bank cap, bank size irrelevant. `talisman/accrue` runs once
per interest tick from `bank/interest/tick` (one global `#tacc nx.talis`); `talisman/round` and the team hook are gone.

## #113: coin sound steps
`purse/pling` (from `purse/changed`, every purse increase): the coin sound plays only when the purse crosses a multiple of
step = 10^floor(log10(nx.earned / 100)), min 1 (under 1000 gathered: every coin; 1000+: every 10; 10000+: every 100; ...).
The "+N" popup still shows every gain (it already batches within its 1.5 s window).

## #114: popup lifetime
`purse/gain`: gains below the coin step (`purse/step`, shared with the sound) wait unseen (forgotten after 5 s); reaching a
step opens the popup for 1.5 s + 0.5 s per step in it, max 4 s, from its opening (`gain_open`, `gain_tick`, `gain_end`,
age in `nx.page`). Talisman trickle (0.6/s): hidden ~1.6 s, "+1.0 .. +2.5" for 2.5 s, closed, again.
