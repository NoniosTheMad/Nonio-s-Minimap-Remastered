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
