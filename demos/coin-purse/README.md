# coin-purse
M1 spike: mining earns coins (scoreboard `nx.coins`, shared with the shop), coins weigh you down, your killer takes your purse.
G -> "Demo: Coin Purse": add/empty coins, Purse Thief, drop purse, refill mine, weight x5, bank balance.

Game code: `datapack/data/nonios/function/purse/` + advancement `nonios:purse/killed`.
- Mining: per block a `minecraft.mined:` objective `nx.mn.<block>`; value = `#<block> nx.coinval` (set in `purse/load`, only if missing).
  Only ores (+ emerald_block = 100) are worth coins; building blocks earn nothing. Placing one (`minecraft.used:` = `nx.pl.<block>`) costs its value back.
- Weight: penalty permille = min((coins - #w_free) * #w_num / #w_den, #w_cap) in `nx.purse` (default 1/1, first 20 free, cap 400 = 40%), applied as
  movement_speed modifier `nonios:purse_weight` (add_multiplied_total) only when coins change. Actionbar on change + every #ab_every (40) ticks while > 0.
- Death: advancement `entity_killed_player` (victim side, fires at the moment of death) -> `execute on attacker`: a player
  or an entity tagged `nx.purse_holder` takes the whole purse. Otherwise (no killer, or a mob) it drops as a coin bag at `LastDeathLocation` (works with immediate respawn):
  gold nugget item, PickupDelay 32767 (no vanilla pickup/merge), score `nx.coins` on the item, the nearest living player within 1.6 blocks takes it.
  Bags despawn after the vanilla 5 min; void deaths lose it.
- Bank stub: marker tagged `nx.bank_zone`; standing within 2.5 blocks moves `nx.coins` into the team bank `#<team> nx.bank` (pads tagged nx.white/nx.black accept only that team; teamless = `#none`). No withdraw.
Demo only: the Purse Thief (husk, `nx.purse_holder`) drops what it stole as a bag when killed (`demo:tick` tracks it with a marker).
