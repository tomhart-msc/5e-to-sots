
# 📘 Swords of the Serpentine Adversaries Reference

## 📋 Standard Format for Adversaries (Markdown)

Use the following format for each adversary. Omit unused attack types (Warfare/Sorcery/Sway). Each field is clearly labeled on its own line for clarity and easy parsing:

```markdown
### [Adversary Name]
**Adjectives**: [comma-separated adjectives]

**Health Defense**
- Threshold: <number>
- Armour: <number>
- Health: <number>

**Morale Defense**
- Threshold: <number>
- Grit: <number>
- Morale: <number>

**Attacks**
- Warfare: +X; Damage Modifier +Y (weapon or method)
- Sorcery: +X; Damage Modifier +Y (sphere or effect)
- Sway: +X; Damage Modifier +Y (tone or method)

**Abilities**
- Malus: <number>
- Investigative: <optional, if any>
- General: <optional, if any>

**Special Abilities**
- <Name> (cost <N>)
- ...

**Misc**
- Alertness Modifier: <optional>
- Stealth Modifier: <optional>
- Other: <any unique notes>

**Refresh Tokens**: <1, 3, 5, or 7>

**Description**: [Brief narrative description of who they are and their role]
```

## 💥 Revised Special Abilities Reference

| **Ability** | **Cost** | **Summary** | **When to Use / Notes** |
|-------------|----------|-------------|--------------------------|
| **Allies** | 3 | Adversary’s allies avenge or assist them. | Use for well-connected foes. Applies after defeat or injury. |
| **Armour-Piercing** | 3 | Ignore 3 points of Armour vs Health for 1 round. | Use when striking heavily armoured Heroes. |
| **Bodyguard** | 3 per use | Absorb an ally’s Health damage. | Must be nearby. Can’t block Morale or Conditions. |
| **Bolster Morale** | 2 per Morale | Heal an ally's Morale like Sway. | Use outside immediate combat turns. Clarify if usable as a reaction. |
| **Death Curse** | All remaining | Inflict long-term curse on killer. | Triggers only at death; no roll. Use for sorcerers or narrative villains. |
| **Defense Boost** | 6 | +3 to Health and Morale Thresholds for 1 round. | Use when cornered or on the defensive. |
| **Disguise** | 1 or 3 | Illusory or mundane disguise (3 if impersonating someone specific). | 1 = generic disguise, 3 = perfect mimic. Use for spies or shapeshifters. |
| **Extra Action** | 3 | Gain an extra action this round. | Can act twice or gain two places in initiative. |
| **Extra Damage** | 3+ | Gain +1 damage die per 3 Malus spent (max 3 dice). | Use once per round. Describe cinematically. |
| **Fear** | 3 (1 target) / 6 (AoE) | Auto-inflict 3+ Morale damage without a roll. | Scare weak-minded foes. Bypasses Thresholds. |
| **Fearsome Blow** | 3 | Combine Warfare and Sway into one action. | Useful for terrifying brutes or dual-threat foes. |
| **Flashback** | 5 + Preparedness | Reveal a previously planned trap or backup. | Great for Masterminds. Clarify outcome and setup. |
| **Flight** | 0 or 3 | Adversary can fly or hover. | 0 = constant flight (e.g., birds); 3 = temporary (e.g., spell). |
| **Fluid** | 0 or 6 | Amorphous form; Armour 5 vs Health. | Use for swarms, oozes, worms, or spirit fogs. |
| **Healing** | 2 per Health | Heal ally’s Health like Bind Wounds. | Use outside direct attacks. Clarify if self-healing is allowed. |
| **Hivemind** | 0 | Share info and coordinate with identical creatures. | Lowers Hero Thresholds if many are present. |
| **Infection** | 0 | Spread disease on contact or attack. | Use for beggars, rats, or swamp monsters. Requires Health test. |
| **Insubstantial** | 0 or 6 | Immune to physical attacks; pass through solid matter. | 6 = activated effect. Still vulnerable to Morale or Sorcery. |
| **Invigorate** | 1 per point | Transfer Malus from one ally to another. | Minions empower their leader. Use for cultists or infernal servants. |
| **Invisibility** | 0 or 6 | Invisible; increases Stealth and Thresholds. | Clarify detection rules. Opposed by Vigilance. |
| **Lightning Speed** | 3 | Double movement and +1 Thresholds for the round. | Use in chase scenes or fast retreats. |
| **Linger** | 0 | Adversary only dies when both Health and Morale hit 0. | Use for undead or spirits. |
| **Magical Charm** | 3 | Charm target vs. Morale test. | Hero acts as if charmer is a close friend. Ends with damage or suspicion. |
| **Mastermind** | 0 | Adversary knows what the GM knows. | Use for long-term villains. No mechanics required. |
| **Mind Reading** | 3 | Read target’s thoughts and recent memories. | Morale test to resist. |
| **Monstrous Ability** | 3 | Trigger a thematic supernatural ability. | E.g., tentacles, wall-crawling, etc. Should be narratively appropriate. |
| **Oracle** | 3 | Adversary sees the future/past. | Use for prophets, witches, or haunted seers. |
| **Persuasive** | 3 | Ignore 3 Grit when dealing Morale damage. | Use for fiery leaders or cult zealots. |
| **Possession** | 3 | Possess a living target via Sorcery or Sway. | Use only for powerful foes. Target takes Morale damage if resisting. |
| **Regenerate** | 0 | Automatically heal damage over time. | Clarify how much and when (each round? per scene?). |
| **Seize Initiative** | 3 | Act at any moment in initiative order. | Use for boss fights or ambushes. |
| **Shape-Shift** | 3 | Take a different form or disguise. | Works best with Disguise. Use for monsters, doppelgangers, or items. |
| **Spellcasting** | 3+ | Activate a sorcerous effect (by Sphere). | Each 3 Malus = 1 spell. Clarify Sphere and # of uses. |
| **Spider Climb** | 0 | Climb walls and ceilings. | Use for monsters or assassins. |
| **Stony** | 0 or 6 | Armour 4; immune to fire; brittle to acid or falls. | 6 = transformation or magical state. |
| **Strength** | 0+ | Add +1 to +3 bonus Warfare damage. | 3 Malus = superhuman feat of strength (e.g., throw wagon). |
| **Summoning** | 3 | Call help (guards, creatures, etc). | Once per fight unless climactic. Clarify number and delay. |
| **Swimming** | 0 | Move in water as well as on land. | May include gills or underwater vision. |
| **Telepathy** | 0 or 3 | Mind-to-mind speech (3 = distant or unknown target). | 0 = line of sight. |
| **Teleport** | 3 or 6 | Instantly move locations (Short = 3, Far = 6). | Requires Sphere of Movement or similar. Clarify form. |
| **Universal Attack** | 6 | Attack all foes in range with separate rolls. | Use for bosses, elementals, or horde monsters. |
| **Venom** | 3 | Inflict poison. | Add Conditions or Health penalties. Clarify symptoms: e.g., “-1 die next turn.” |
| **Warded** | 6 | Halve all damage for 1 round. | Powerful bosses use this to stay alive. Clarify which damage type is affected. |

---

### 🧠 Usage Notes for LLMs

- If a cost is **variable**, apply **3 Malus per offensive effect** or **2 per healing effect**, unless otherwise stated.
- Use **one major effect per round**, unless the adversary is a deadly boss.
- Special Abilities should **reflect the adversary’s theme or role in the story**, not just power level.
- You may invent new abilities based on the above templates, assigning a cost of:
  - **3 Malus** for single-target offensive effects
  - **6 Malus** for AoE, major defense, or game-altering abilities
