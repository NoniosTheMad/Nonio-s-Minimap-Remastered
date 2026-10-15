# V2 gap classes (design drafts, not built)

V2 listed these classes in its menu and price signs but never built a kit for them (see `docs/v2-gap-inventory.md` section 6). The prices are V2's. Each kit uses 26.x tech: spears/lunge, mace smash, happy ghast, scale and attribute modifiers, goat-horn cooldowns, display entities and post shaders.

## Paladin (300): the holy front-liner
- **Kit:** Iron armour locked on, a gold-trimmed shield and a Spear (lunge charge, 26.x spear).
- **Aura of Devotion:** allies within 6 blocks take 15% less damage. A faint gold ring (particles) shows it.
- **Judgement** (horn, 20 s): your next spear lunge stuns the target 1 s and heals the 3 nearest allies 2 hearts each.
- **Smite undead:** double damage against Monster, Reaper and Death Knight.
- **Weakness:** slow to sprint (no sprint while the shield is raised). It can't heal itself.

## Death Knight (500): the draining dark tank
- **Kit:** Netherite helmet locked on with blackened leather, plus a Runeblade (netherite sword).
- **Frost Path:** you leave frosted ice (frost walker) and enemies on it get Slowness I.
- **Death Grip** (horn, 15 s): pull the targeted enemy 12 blocks to you (tongue tech, shorter).
- **Army of the Dead:** each kill raises a wither skeleton thrall for 30 s (team-tagged, ignores your allies, max 3).
- **Blood Rune:** hits heal 10% of the damage dealt, rising to 30% below 5 hearts. It has no regeneration otherwise.
- **Weakness:** takes fire damage x1.5 and can't drink potions.

## Titan (1500): the walking siege
- **Kit:** scale 1.8, 30 extra hearts, a Mace locked on. No armour slots (natural armour 12).
- **Earthshaker:** the mace smash scales with fall height as usual. Your landings crack blocks in radius 2 (not barriers).
- **Boulder** (horn, 10 s): throw a falling-block boulder (block_display plus a snowball carrier). It deals 6 damage and breaks glass and planks.
- **Bulwark:** while sneaking you become a wall: knockback immunity, Resistance II and Slowness IV.
- **Weakness:** can't sprint-jump, big hitbox, takes x2 damage from arrows.

## Destroyer (2000): structure breaker
- **Kit:** Netherite pickaxe (Efficiency X equivalent) plus a TNT Launcher (crossbow that fires primed TNT, 3 charges and a recharge).
- **Demolisher:** breaks player-placed blocks and barrier segments 3x faster. It deals x2 to Nexus/barrier hits.
- **Breach Charge** (horn, 30 s): plant a charge on a wall. After 3 s it carves a 3x3 tunnel 6 deep (it skips protected blocks).
- **Blast Plating:** immune to explosion damage and knockback, its own included.
- **Weakness:** weak in melee (attack damage -3), and Glowing for 5 s after every launch.

## Guardian Angel (5000): the team's wings (unlike the 150-coin Angel, it doesn't heal; it saves)
- **Kit:** scale 1.4, rides a harnessed happy ghast with a gold glow, or flies on Seraph Wings with infinite rockets on a cooldown.
- **Bond:** right-click a teammate to bind them (one at a time). A golden tether (trail particle) shows the link.
- **Intervention:** when the bound ally takes lethal damage, they're saved at 1 heart, made invulnerable for 2 s and teleported to you (once per 60 s).
- **Ascension** (horn, 90 s): 6 s of a team-wide holy shader. Every ally gets Resistance III and the dead respawn instantly beside you.
- **Weakness:** almost no damage (fists only). If the Guardian Angel dies, every ally loses 2 hearts for 30 s.
