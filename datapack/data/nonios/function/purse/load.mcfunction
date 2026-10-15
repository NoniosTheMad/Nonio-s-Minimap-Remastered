# Coin purse: mining earns coins (scoreboard "coins", shared with the shop), carrying them slows you down,
# dying hands the purse to your killer (or drops it as a coin bag). Config lives in nx.purse / nx.coinval.
scoreboard objectives add nx.coins dummy {"text":"Coins","color":"gold"}
scoreboard objectives add nx.purse dummy
scoreboard objectives add nx.coinval dummy
scoreboard objectives add nx.bank dummy
scoreboard objectives add nx.died deathCount
scoreboard objectives add nx.pslow dummy
scoreboard objectives add nx.plast dummy
# stats: coins earned by mining this match (ore value, minus placed-back)
scoreboard objectives add nx.mined dummy
# per player: gametime until which the coin actionbar stays quiet (a barrier message is showing)
scoreboard objectives add nx.ab_hold dummy
# coins owed for coin blocks placed while broke (purse/mine/placed), repaid from mining income first
scoreboard objectives add nx.pdebt dummy

# --- config (only set when missing, so /scoreboard tweaks survive /reload) ---
# weight (feedback #35): coins are valued at the match's money scale S (percent, 100 at the start):
#   effective coins = coins * 100 / S;  penalty (permille) = min(max(effective - w_free, 0) * w_num / w_den, w_cap)
#   S = min(max(100 + w_grow * match minutes, 100 + team average earned * 100 / w_iref), w_smax)
# so later in the match (or once the team earns fast) more coins are free and each coin weighs less.
# Defaults: 0.1%/coin after 20 free coins, max 40%; S +10% per minute, +100% per 500 coins earned per teammate, max 10x.
execute unless score #w_num nx.purse = #w_num nx.purse run scoreboard players set #w_num nx.purse 1
execute unless score #w_den nx.purse = #w_den nx.purse run scoreboard players set #w_den nx.purse 1
# the first #w_free coins (at match-start value) weigh nothing (user, 2026-10-14)
execute unless score #w_free nx.purse = #w_free nx.purse run scoreboard players set #w_free nx.purse 20
execute unless score #w_cap nx.purse = #w_cap nx.purse run scoreboard players set #w_cap nx.purse 400
execute unless score #w_grow nx.purse = #w_grow nx.purse run scoreboard players set #w_grow nx.purse 10
# 0 = ignore income (time only)
execute unless score #w_iref nx.purse = #w_iref nx.purse run scoreboard players set #w_iref nx.purse 500
execute unless score #w_smax nx.purse = #w_smax nx.purse run scoreboard players set #w_smax nx.purse 1000
# per player: coins earned this match (purse increases, minus bank withdrawals) and the money scale they are weighed at
scoreboard objectives add nx.earned dummy
scoreboard objectives add nx.pscale dummy
# actionbar refresh period (ticks)
execute unless score #ab_every nx.purse = #ab_every nx.purse run scoreboard players set #ab_every nx.purse 40

# --- coins per mined block: src/yields.json -> purse/gen/yields (tools/build_yields.py). Hundredths of a coin;
# the remainder below 1 coin is kept per player in nx.pfrac and paid once it adds up. Unlisted blocks (stone,
# deepslate, cobblestone...) earn nothing and cost nothing to place. Fortune: +#fortune_pct % per level.
scoreboard objectives add nx.pfrac dummy
# purse gain popup (purse/gain): last total in hundredths, gain on show (hundredths), popup ticks left
scoreboard objectives add nx.ptot dummy
scoreboard objectives add nx.pgain dummy
scoreboard objectives add nx.ptime dummy
scoreboard objectives add nx.page dummy
function nonios:purse/gen/yields
# --- emerald items: coins on pickup (purse/emerald), same as the centre generator's coin outcomes (#ce1 / #ce9 nx.gen) ---
execute unless score #emerald_item nx.coinval = #emerald_item nx.coinval run scoreboard players set #emerald_item nx.coinval 5
execute unless score #emerald_block_item nx.coinval = #emerald_block_item nx.coinval run scoreboard players set #emerald_block_item nx.coinval 45

scoreboard players set #10 nx.purse 10
scoreboard players set #100 nx.purse 100
scoreboard players set #-1 nx.purse -1
scoreboard players set #60 nx.purse 60
scoreboard players set #20 nx.purse 20
execute unless score #s_white nx.purse matches 100.. run scoreboard players set #s_white nx.purse 100
execute unless score #s_black nx.purse matches 100.. run scoreboard players set #s_black nx.purse 100
