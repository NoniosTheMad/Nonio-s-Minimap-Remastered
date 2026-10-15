# Exodia, the Forbidden One (#81, design draft, not built)

Hooks into `#nonios:dream/exodia_grant` (feat/dream-v3 stub: altar in the Nightmare Spire, once per team). Status: waiting for the user's call.

- **Earned:** the first player per team to touch the summit altar after the 2 wardens fall. It's free and replaces their current class (the old class is stored and returned at the end). The whole server sees "<name> has claimed Exodia." and a purple beacon pillar marks them for 10 s.
- **The fantasy:** you are a sealed giant. Only the Head is free at first. Each unsealed limb makes you bigger (scale 1.3 to 2.0) and adds a power. Chains (item_display links) orbit you and break one by one.
- **Kit:** no armour slots. Base: 40 hearts, Netherite-tier toughness via attributes, slow walk. Chain Gauntlets (mace-like fists; the mace smash rules apply) locked in the main hand. The "forbidden" post shader is on for Exodia only: chain vignette and sigil glow.
- **Head (on claim): The Eye.** Enemies within 24 blocks glow (Exodia-only glow team). You can't be blinded or darkened.
- **Right Arm: Seal-Breaker.** Ground slam (goat-horn cooldown, 12 s): a 6-block shockwave with knockback and Slowness.
- **Left Arm: Chain Grab.** Hook the player you're aiming at (20 blocks) and drag them to your feet (the frog-tongue tech).
- **Right Leg: Quake Stride.** Sprinting leaves cracked earth (cobweb-slow for 3 s). You also gain step height and jump boost.
- **Left Leg: Unbound.** Knockback immunity and speed back to normal. Fall damage is converted into an AoE landing.
- **Unsealing:** 1 limb per player kill or per 3 min alive (whichever comes first; order is fixed: R arm, L arm, R leg, L leg).
- **All five: OBLITERATE.** A 4 s channel, rooted, with a beam visible map-wide. It fires a 40-block cone that deals lethal damage and destroys the targeted enemy barrier/Nexus segment.
- **How it ends:** after Obliterate, Exodia crumbles to dust (particles plus a sound for all) and the player gets the stored class back. If Exodia dies first, the seal breaks: the killer's team gets a 300-coin bounty and Exodia is gone for that team for the rest of the match.
