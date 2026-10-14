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
