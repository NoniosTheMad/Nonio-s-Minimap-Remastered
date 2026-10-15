# Concept images (Gemini)

Use generated images to pin down what an effect or build *should* look like before prototyping, then compare the shaderlab, voxel and mcfilm output against them. They're for inspiration only and never ship.

## Route 1: Gemini web app (default; uses Nonios's Google AI Pro)
Dispatch a cheap browser agent (`model: haiku`) with the claude-in-chrome tools:
1. `tabs_context_mcp`, then open a new tab at https://gemini.google.com/images (sidebar "Images"; click "Try it" the first time).
2. Type the prompt in "Enter a prompt for Gemini" and click "Send message". An image takes ~10-15 s.
3. Click "Download full size image" (2752x1536 JPG goes to `C:\Users\danir\Downloads`). Move the newest file to `.mcdev/imagegen/<name>.jpg`.
4. To iterate, send follow-ups in the same chat ("same but ..."). Close the tab when done.
Never type credentials; stop if a login or consent screen appears.

## Route 2: API (`tools/imagegen.py`)
`python tools/imagegen.py "prompt" [-n 3] [--ref img]` needs paid API credits on the key's AI Studio project. As of 2026-10-15 those were depleted (402).

## Prompting
Hunt for the best inspiration, not a Minecraft mock-up (user, #103): "minecraft scene" prompts drag the quality of the effect down.
- Describe the effect itself (light, colour grade, particles, distortion, mood) as a cinematic still, concept art or painting. Iterate: vary the wording and keep the strongest frames.
- Minecraft-with-shaders prompts only when studying light on blocks (god rays, halos), where shader packs already excel. Not a default.
- Translate to the game afterwards: keep the centre readable, 16:9.
