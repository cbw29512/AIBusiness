/**
 * Certified SRD 5.2.1 Data Set for DM Encounter & Loot Toolkit
 * Content licensed under CC-BY-4.0 from Wizards of the Coast LLC.
 */

window.SRD_DATA = {
  // Monster SRD Database
  monsters: [
    {
      name: "Commoner",
      cr: "0",
      xp: 10,
      size: "Medium",
      type: "Humanoid (any race)",
      alignment: "Any alignment",
      ac: 10,
      acType: "",
      hp: "4 (1d8)",
      speed: "30 ft.",
      stats: { str: 10, dex: 10, con: 10, int: 10, wis: 10, cha: 10 },
      senses: "passive Perception 10",
      languages: "any one language (usually Common)",
      traits: [],
      actions: [
        { name: "Club", desc: "Melee Weapon Attack: +2 to hit, reach 5 ft., one target. Hit: 2 (1d4) bludgeoning damage." }
      ]
    },
    {
      name: "Acolyte",
      cr: "1/8",
      xp: 25,
      size: "Medium",
      type: "Humanoid (any race)",
      alignment: "Any alignment",
      ac: 10,
      acType: "",
      hp: "9 (2d8)",
      speed: "30 ft.",
      stats: { str: 10, dex: 10, con: 10, int: 10, wis: 14, cha: 11 },
      skills: "Medicine +4, Religion +2",
      senses: "passive Perception 12",
      languages: "any one language (usually Common)",
      traits: [
        { name: "Spellcasting", desc: "The acolyte is a 1st-level spellcaster (Wisdom DC 12, +4 to hit with spell attacks). Spells: Cantrips: light, sacred flame, thaumaturgy; 1st level (3 slots): bless, cure wounds, sanctuary." }
      ],
      actions: [
        { name: "Club", desc: "Melee Weapon Attack: +2 to hit, reach 5 ft., one target. Hit: 2 (1d4) bludgeoning damage." }
      ]
    },
    {
      name: "Bandit",
      cr: "1/8",
      xp: 25,
      size: "Medium",
      type: "Humanoid (any race)",
      alignment: "Non-Lawful",
      ac: 12,
      acType: "leather armor",
      hp: "11 (2d8 + 2)",
      speed: "30 ft.",
      stats: { str: 11, dex: 12, con: 12, int: 10, wis: 10, cha: 10 },
      senses: "passive Perception 10",
      languages: "Common",
      traits: [],
      actions: [
        { name: "Scimitar", desc: "Melee Weapon Attack: +3 to hit, reach 5 ft., one target. Hit: 4 (1d6 + 1) slashing damage." },
        { name: "Light Crossbow", desc: "Ranged Weapon Attack: +3 to hit, range 80/320 ft., one target. Hit: 5 (1d8 + 1) piercing damage." }
      ]
    },
    {
      name: "Cultist",
      cr: "1/8",
      xp: 25,
      size: "Medium",
      type: "Humanoid (any race)",
      alignment: "Non-Good",
      ac: 12,
      acType: "leather armor",
      hp: "9 (2d8)",
      speed: "30 ft.",
      stats: { str: 11, dex: 12, con: 10, int: 10, wis: 11, cha: 10 },
      skills: "Deception +2, Religion +2",
      senses: "passive Perception 10",
      languages: "Common",
      traits: [
        { name: "Dark Devotion", desc: "The cultist has advantage on saving throws against being charmed or frightened." }
      ],
      actions: [
        { name: "Scimitar", desc: "Melee Weapon Attack: +3 to hit, reach 5 ft., one target. Hit: 4 (1d6 + 1) slashing damage." }
      ]
    },
    {
      name: "Kobold",
      cr: "1/8",
      xp: 25,
      size: "Small",
      type: "Humanoid (kobold)",
      alignment: "Lawful Evil",
      ac: 12,
      acType: "",
      hp: "5 (2d6 - 2)",
      speed: "30 ft.",
      stats: { str: 7, dex: 15, con: 9, int: 8, wis: 7, cha: 8 },
      senses: "Darkvision 60 ft., passive Perception 8",
      languages: "Draconic",
      traits: [
        { name: "Sunlight Sensitivity", desc: "While in sunlight, the kobold has disadvantage on attack rolls, as well as on Wisdom (Perception) checks that rely on sight." },
        { name: "Pack Tactics", desc: "The kobold has advantage on an attack roll against a creature if at least one of the kobold's allies is within 5 feet of the creature and the ally isn't incapacitated." }
      ],
      actions: [
        { name: "Dagger", desc: "Melee or Ranged Weapon Attack: +4 to hit, reach 5 ft. or range 20/60 ft., one target. Hit: 4 (1d4 + 2) piercing damage." },
        { name: "Sling", desc: "Ranged Weapon Attack: +4 to hit, range 30/120 ft., one target. Hit: 4 (1d4 + 2) bludgeoning damage." }
      ]
    },
    {
      name: "Stirge",
      cr: "1/8",
      xp: 25,
      size: "Tiny",
      type: "Beast",
      alignment: "Unaligned",
      ac: 14,
      acType: "",
      hp: "2 (1d4)",
      speed: "10 ft., fly 40 ft.",
      stats: { str: 4, dex: 16, con: 11, int: 2, wis: 8, cha: 6 },
      senses: "Darkvision 60 ft., passive Perception 9",
      languages: "",
      traits: [],
      actions: [
        { name: "Blood Drain", desc: "Melee Weapon Attack: +5 to hit, reach 5 ft., one creature. Hit: 5 (1d4 + 3) piercing damage, and the stirge attaches to the target." }
      ]
    },
    {
      name: "Goblin",
      cr: "1/4",
      xp: 50,
      size: "Small",
      type: "Humanoid (goblinoid)",
      alignment: "Neutral Evil",
      ac: 15,
      acType: "leather armor, shield",
      hp: "7 (2d6)",
      speed: "30 ft.",
      stats: { str: 8, dex: 14, con: 10, int: 10, wis: 8, cha: 8 },
      skills: "Stealth +6",
      senses: "Darkvision 60 ft., passive Perception 9",
      languages: "Common, Goblin",
      traits: [
        { name: "Nimble Escape", desc: "The goblin can take the Disengage or Hide action as a bonus action on each of its turns." }
      ],
      actions: [
        { name: "Scimitar", desc: "Melee Weapon Attack: +4 to hit, reach 5 ft., one target. Hit: 5 (1d6 + 2) slashing damage." },
        { name: "Shortbow", desc: "Ranged Weapon Attack: +4 to hit, range 80/320 ft., one target. Hit: 5 (1d6 + 2) piercing damage." }
      ]
    },
    {
      name: "Skeleton",
      cr: "1/4",
      xp: 50,
      size: "Medium",
      type: "Undead",
      alignment: "Lawful Evil",
      ac: 13,
      acType: "armor scraps",
      hp: "13 (2d8 + 4)",
      speed: "30 ft.",
      stats: { str: 10, dex: 14, con: 15, int: 6, wis: 8, cha: 5 },
      vulnerabilities: "Bludgeoning",
      immunities: "Poison",
      conditionImmunities: "Exhaustion, Poisoned",
      senses: "Darkvision 60 ft., passive Perception 9",
      languages: "understands languages it knew in life but can't speak",
      traits: [],
      actions: [
        { name: "Shortsword", desc: "Melee Weapon Attack: +4 to hit, reach 5 ft., one target. Hit: 5 (1d6 + 2) piercing damage." },
        { name: "Shortbow", desc: "Ranged Weapon Attack: +4 to hit, range 80/320 ft., one target. Hit: 5 (1d6 + 2) piercing damage." }
      ]
    },
    {
      name: "Zombie",
      cr: "1/4",
      xp: 50,
      size: "Medium",
      type: "Undead",
      alignment: "Neutral Evil",
      ac: 8,
      acType: "",
      hp: "22 (3d8 + 8)",
      speed: "20 ft.",
      stats: { str: 13, dex: 6, con: 16, int: 3, wis: 6, cha: 5 },
      immunities: "Poison",
      conditionImmunities: "Poisoned",
      senses: "Darkvision 60 ft., passive Perception 8",
      languages: "understands languages it knew in life but can't speak",
      traits: [
        { name: "Undead Fortitude", desc: "If damage reduces the zombie to 0 hit points, it must make a Constitution saving throw with a DC of 5 + the damage taken, unless the damage is radiant or from a critical hit. On a success, the zombie drops to 1 hit point instead." }
      ],
      actions: [
        { name: "Slam", desc: "Melee Weapon Attack: +3 to hit, reach 5 ft., one target. Hit: 4 (1d6 + 1) bludgeoning damage." }
      ]
    },
    {
      name: "Orc",
      cr: "1/2",
      xp: 100,
      size: "Medium",
      type: "Humanoid (orc)",
      alignment: "Chaotic Evil",
      ac: 13,
      acType: "hide armor",
      hp: "15 (2d8 + 6)",
      speed: "30 ft.",
      stats: { str: 16, dex: 12, con: 16, int: 7, wis: 11, cha: 10 },
      skills: "Intimidation +2",
      senses: "Darkvision 60 ft., passive Perception 10",
      languages: "Common, Orc",
      traits: [
        { name: "Aggressive", desc: "As a bonus action, the orc can move up to its speed toward a hostile creature that it can see." }
      ],
      actions: [
        { name: "Greataxe", desc: "Melee Weapon Attack: +5 to hit, reach 5 ft., one target. Hit: 9 (1d12 + 3) slashing damage." },
        { name: "Javelin", desc: "Melee or Ranged Weapon Attack: +5 to hit, reach 5 ft. or range 30/120 ft., one target. Hit: 6 (1d6 + 3) piercing damage." }
      ]
    },
    {
      name: "Hobgoblin",
      cr: "1/2",
      xp: 100,
      size: "Medium",
      type: "Humanoid (goblinoid)",
      alignment: "Lawful Evil",
      ac: 18,
      acType: "chain mail, shield",
      hp: "11 (2d8 + 2)",
      speed: "30 ft.",
      stats: { str: 13, dex: 12, con: 12, int: 10, wis: 10, cha: 9 },
      senses: "Darkvision 60 ft., passive Perception 10",
      languages: "Common, Goblin",
      traits: [
        { name: "Martial Advantage", desc: "Once per turn, the hobgoblin can deal an extra 7 (2d6) damage to a creature it hits with a weapon attack if that creature is within 5 feet of an ally of the hobgoblin that isn't incapacitated." }
      ],
      actions: [
        { name: "Longsword", desc: "Melee Weapon Attack: +3 to hit, reach 5 ft., one target. Hit: 5 (1d8 + 1) slashing damage, or 6 (1d10 + 1) slashing damage if used with two hands." },
        { name: "Longbow", desc: "Ranged Weapon Attack: +3 to hit, range 150/600 ft., one target. Hit: 5 (1d8 + 1) piercing damage." }
      ]
    },
    {
      name: "Bugbear",
      cr: "1",
      xp: 200,
      size: "Medium",
      type: "Humanoid (goblinoid)",
      alignment: "Chaotic Evil",
      ac: 16,
      acType: "hide armor, shield",
      hp: "27 (5d8 + 5)",
      speed: "30 ft.",
      stats: { str: 15, dex: 14, con: 13, int: 8, wis: 11, cha: 9 },
      skills: "Stealth +6, Survival +2",
      senses: "Darkvision 60 ft., passive Perception 10",
      languages: "Common, Goblin",
      traits: [
        { name: "Brute", desc: "A melee weapon deals one extra die of its damage when the bugbear hits with it (included in the attack)." },
        { name: "Surprise Attack", desc: "If the bugbear surprises a creature and hits it with an attack during the first round of combat, the target takes an extra 7 (2d6) damage from the attack." }
      ],
      actions: [
        { name: "Morningstar", desc: "Melee Weapon Attack: +4 to hit, reach 5 ft., one target. Hit: 11 (2d8 + 2) piercing damage." },
        { name: "Javelin", desc: "Melee or Ranged Weapon Attack: +4 to hit, reach 5 ft. or range 30/120 ft., one target. Hit: 9 (2d6 + 2) piercing damage in melee or 5 (1d6 + 2) piercing damage at range." }
      ]
    },
    {
      name: "Ghoul",
      cr: "1",
      xp: 200,
      size: "Medium",
      type: "Undead",
      alignment: "Chaotic Evil",
      ac: 12,
      acType: "",
      hp: "22 (5d8)",
      speed: "30 ft.",
      stats: { str: 13, dex: 15, con: 10, int: 7, wis: 10, cha: 6 },
      immunities: "Poison",
      conditionImmunities: "Charmed, Exhaustion, Poisoned",
      senses: "Darkvision 60 ft., passive Perception 10",
      languages: "Common",
      traits: [],
      actions: [
        { name: "Bite", desc: "Melee Weapon Attack: +2 to hit, reach 5 ft., one creature. Hit: 9 (2d6 + 2) piercing damage." },
        { name: "Claws", desc: "Melee Weapon Attack: +4 to hit, reach 5 ft., one target. Hit: 7 (2d4 + 2) slashing damage. If target is a creature other than an elf or undead, it must succeed on a DC 10 Constitution saving throw or be paralyzed for 1 minute." }
      ]
    },
    {
      name: "Gargoyle",
      cr: "2",
      xp: 450,
      size: "Medium",
      type: "Elemental",
      alignment: "Chaotic Evil",
      ac: 15,
      acType: "natural armor",
      hp: "52 (7d8 + 21)",
      speed: "30 ft., fly 60 ft.",
      stats: { str: 15, dex: 11, con: 16, int: 6, wis: 11, cha: 7 },
      resistances: "Bludgeoning, Piercing, and Slashing from Nonmagical Attacks that aren't Admantine",
      immunities: "Poison",
      conditionImmunities: "Exhaustion, Petrified, Poisoned",
      senses: "Darkvision 60 ft., passive Perception 10",
      languages: "Terran",
      traits: [
        { name: "False Appearance", desc: "While the gargoyle remains motionless, it is indistinguishable from an inanimate statue." }
      ],
      actions: [
        { name: "Multiattack", desc: "The gargoyle makes two attacks: one with its bite and one with its claws." },
        { name: "Bite", desc: "Melee Weapon Attack: +4 to hit, reach 5 ft., one target. Hit: 5 (1d6 + 2) piercing damage." },
        { name: "Claws", desc: "Melee Weapon Attack: +4 to hit, reach 5 ft., one target. Hit: 5 (1d6 + 2) slashing damage." }
      ]
    },
    {
      name: "Ogre",
      cr: "2",
      xp: 450,
      size: "Large",
      type: "Giant",
      alignment: "Chaotic Evil",
      ac: 11,
      acType: "hide armor",
      hp: "59 (7d10 + 21)",
      speed: "40 ft.",
      stats: { str: 19, dex: 8, con: 16, int: 5, wis: 7, cha: 7 },
      senses: "Darkvision 60 ft., passive Perception 8",
      languages: "Common, Giant",
      traits: [],
      actions: [
        { name: "Greatclub", desc: "Melee Weapon Attack: +6 to hit, reach 5 ft., one target. Hit: 13 (2d8 + 4) bludgeoning damage." },
        { name: "Javelin", desc: "Melee or Ranged Weapon Attack: +6 to hit, reach 5 ft. or range 30/120 ft., one target. Hit: 11 (2d6 + 4) piercing damage." }
      ]
    },
    {
      name: "Gelatinous Cube",
      cr: "2",
      xp: 450,
      size: "Large",
      type: "Ooze",
      alignment: "Unaligned",
      ac: 6,
      acType: "",
      hp: "84 (8d10 + 40)",
      speed: "15 ft.",
      stats: { str: 14, dex: 3, con: 20, int: 1, wis: 6, cha: 1 },
      conditionImmunities: "Blinded, Charmed, Deafened, Exhaustion, Frightened, Prone",
      senses: "Blindsight 60 ft. (blind beyond this radius), passive Perception 8",
      languages: "",
      traits: [
        { name: "Opaque / Transparent", desc: "Even when the cube is in plain sight, it takes a successful DC 15 Wisdom (Perception) check to spot a cube that has neither moved nor attacked." },
        { name: "Engulf", desc: "The cube moves up to its speed. It can enter Large or smaller creatures' spaces. Whenever the cube enters a creature's space, the creature must make a DC 12 Dexterity saving throw." }
      ],
      actions: [
        { name: "Pseudopod", desc: "Melee Weapon Attack: +4 to hit, reach 5 ft., one creature. Hit: 10 (3d6) acid damage." }
      ]
    },
    {
      name: "Mimic",
      cr: "2",
      xp: 450,
      size: "Medium",
      type: "Monstrosity (shapechanger)",
      alignment: "Neutral",
      ac: 12,
      acType: "natural armor",
      hp: "58 (9d8 + 18)",
      speed: "15 ft.",
      stats: { str: 17, dex: 12, con: 15, int: 5, wis: 13, cha: 8 },
      skills: "Stealth +5",
      immunities: "Acid",
      conditionImmunities: "Prone",
      senses: "Darkvision 60 ft., passive Perception 11",
      languages: "",
      traits: [
        { name: "Shapechanger", desc: "The mimic can use its action to polymorph into an object or back into its true, amorphous form." },
        { name: "Adhesive", desc: "The mimic adheres to anything that touches it. A Huge or smaller creature adhered to the mimic is also grappled (escape DC 13)." },
        { name: "False Appearance", desc: "While remaining motionless in object form, the mimic is indistinguishable from an ordinary object." }
      ],
      actions: [
        { name: "Pseudopod", desc: "Melee Weapon Attack: +5 to hit, reach 5 ft., one target. Hit: 7 (1d8 + 3) bludgeoning damage. If the mimic is in object form, the target is subjected to its Adhesive trait." },
        { name: "Bite", desc: "Melee Weapon Attack: +5 to hit, reach 5 ft., one target. Hit: 7 (1d8 + 3) piercing damage plus 4 (1d8) acid damage." }
      ]
    },
    {
      name: "Minotaur",
      cr: "3",
      xp: 700,
      size: "Large",
      type: "Monstrosity",
      alignment: "Chaotic Evil",
      ac: 14,
      acType: "natural armor",
      hp: "76 (9d10 + 27)",
      speed: "40 ft.",
      stats: { str: 18, dex: 11, con: 16, int: 6, wis: 16, cha: 9 },
      skills: "Perception +7",
      senses: "Darkvision 60 ft., passive Perception 17",
      languages: "Abyssal",
      traits: [
        { name: "Charge", desc: "If the minotaur moves at least 10 feet straight toward a target and then hits it with a gore attack on the same turn, the target takes an extra 9 (2d8) piercing damage. If the target is a creature, it must succeed on a DC 14 Strength saving throw or be pushed up to 10 feet away and knocked prone." },
        { name: "Labyrinthine Recall", desc: "The minotaur can perfectly recall any path it has traveled." },
        { name: "Reckless", desc: "At the start of its turn, the minotaur can gain advantage on all melee weapon attack rolls during that turn, but attack rolls against it have advantage until the start of its next turn." }
      ],
      actions: [
        { name: "Greataxe", desc: "Melee Weapon Attack: +6 to hit, reach 5 ft., one target. Hit: 17 (2d12 + 4) slashing damage." },
        { name: "Gore", desc: "Melee Weapon Attack: +6 to hit, reach 5 ft., one target. Hit: 13 (2d8 + 4) piercing damage." }
      ]
    },
    {
      name: "Phase Spider",
      cr: "3",
      xp: 700,
      size: "Large",
      type: "Monstrosity",
      alignment: "Unaligned",
      ac: 13,
      acType: "natural armor",
      hp: "32 (5d10 + 5)",
      speed: "30 ft., climb 30 ft.",
      stats: { str: 15, dex: 16, con: 12, int: 6, wis: 10, cha: 6 },
      skills: "Stealth +7",
      senses: "Darkvision 60 ft., Spider Sense 60 ft., passive Perception 10",
      languages: "",
      traits: [
        { name: "Ethereal Jaunt", desc: "As a bonus action, the spider can magically shift from the Material Plane to the Ethereal Plane, or vice versa." },
        { name: "Spider Climb", desc: "The spider can climb difficult surfaces, including upside down on ceilings, without needing to make an ability check." }
      ],
      actions: [
        { name: "Bite", desc: "Melee Weapon Attack: +4 to hit, reach 5 ft., one creature. Hit: 7 (1d10 + 2) piercing damage, and the target must make a DC 11 Constitution saving throw, taking 9 (2d8) poison damage on a failed save, or half as much on a successful one." }
      ]
    },
    {
      name: "Owlbear",
      cr: "3",
      xp: 700,
      size: "Large",
      type: "Monstrosity",
      alignment: "Unaligned",
      ac: 13,
      acType: "natural armor",
      hp: "59 (7d10 + 21)",
      speed: "40 ft.",
      stats: { str: 20, dex: 12, con: 17, int: 3, wis: 12, cha: 7 },
      skills: "Perception +7",
      senses: "Darkvision 60 ft., passive Perception 17",
      languages: "",
      traits: [
        { name: "Keen Sight and Smell", desc: "The owlbear has advantage on Wisdom (Perception) checks that rely on sight or smell." }
      ],
      actions: [
        { name: "Multiattack", desc: "The owlbear makes two attacks: one with its beak and one with its claws." },
        { name: "Beak", desc: "Melee Weapon Attack: +7 to hit, reach 5 ft., one target. Hit: 10 (1d10 + 5) piercing damage." },
        { name: "Claws", desc: "Melee Weapon Attack: +7 to hit, reach 5 ft., one target. Hit: 14 (2d8 + 5) slashing damage." }
      ]
    },
    {
      name: "Manticore",
      cr: "3",
      xp: 700,
      size: "Large",
      type: "Monstrosity",
      alignment: "Lawful Evil",
      ac: 14,
      acType: "natural armor",
      hp: "68 (8d10 + 24)",
      speed: "30 ft., fly 50 ft.",
      stats: { str: 17, dex: 16, con: 17, int: 7, wis: 12, cha: 8 },
      senses: "Darkvision 60 ft., passive Perception 11",
      languages: "Common",
      traits: [
        { name: "Tail Spike Regrowth", desc: "The manticore has 24 tail spikes. Used spikes regrow when the manticore finishes a long rest." }
      ],
      actions: [
        { name: "Multiattack", desc: "The manticore makes three attacks: one with its bite and two with its claws, or three with its tail spikes." },
        { name: "Bite", desc: "Melee Weapon Attack: +5 to hit, reach 5 ft., one target. Hit: 7 (1d8 + 3) piercing damage." },
        { name: "Tail Spike", desc: "Ranged Weapon Attack: +5 to hit, range 100/200 ft., one target. Hit: 7 (1d8 + 3) piercing damage." }
      ]
    },
    {
      name: "Basilisk",
      cr: "3",
      xp: 700,
      size: "Medium",
      type: "Monstrosity",
      alignment: "Unaligned",
      ac: 15,
      acType: "natural armor",
      hp: "52 (8d8 + 16)",
      speed: "20 ft.",
      stats: { str: 16, dex: 8, con: 15, int: 2, wis: 8, cha: 7 },
      senses: "Darkvision 60 ft., passive Perception 9",
      languages: "",
      traits: [
        { name: "Petrifying Gaze", desc: "If a creature starts its turn within 30 feet of the basilisk and the two can see each other, the basilisk can force the creature to make a DC 12 Constitution saving throw or begin turning to stone." }
      ],
      actions: [
        { name: "Bite", desc: "Melee Weapon Attack: +5 to hit, reach 5 ft., one target. Hit: 10 (2d6 + 3) piercing damage plus 7 (2d6) poison damage." }
      ]
    },
    {
      name: "Ettin",
      cr: "4",
      xp: 1100,
      size: "Large",
      type: "Giant",
      alignment: "Chaotic Evil",
      ac: 12,
      acType: "natural armor",
      hp: "85 (10d10 + 30)",
      speed: "40 ft.",
      stats: { str: 21, dex: 8, con: 17, int: 6, wis: 10, cha: 8 },
      skills: "Perception +4",
      senses: "Darkvision 60 ft., passive Perception 14",
      languages: "Orc, Giant",
      traits: [
        { name: "Two Heads", desc: "The ettin has advantage on Wisdom (Perception) checks and on saving throws against being blinded, charmed, deafened, frightened, stunned, and knocked unconscious." },
        { name: "Wakeful", desc: "When one of the ettin's heads is asleep, its other head is awake." }
      ],
      actions: [
        { name: "Multiattack", desc: "The ettin makes two attacks: one with its battleaxe and one with its morningstar." },
        { name: "Battleaxe", desc: "Melee Weapon Attack: +7 to hit, reach 5 ft., one target. Hit: 14 (2d8 + 5) slashing damage." },
        { name: "Morningstar", desc: "Melee Weapon Attack: +7 to hit, reach 5 ft., one target. Hit: 14 (2d8 + 5) piercing damage." }
      ]
    },
    {
      name: "Troll",
      cr: "5",
      xp: 1800,
      size: "Large",
      type: "Giant",
      alignment: "Chaotic Evil",
      ac: 15,
      acType: "natural armor",
      hp: "84 (8d10 + 40)",
      speed: "30 ft.",
      stats: { str: 18, dex: 13, con: 20, int: 7, wis: 9, cha: 7 },
      skills: "Perception +2",
      senses: "Darkvision 60 ft., passive Perception 12",
      languages: "Giant",
      traits: [
        { name: "Keen Smell", desc: "The troll has advantage on Wisdom (Perception) checks that rely on smell." },
        { name: "Regeneration", desc: "The troll regains 10 hit points at the start of its turn. If the troll takes acid or fire damage, this trait doesn't function at the start of the troll's next turn. The troll dies only if it starts its turn with 0 hit points and doesn't regenerate." }
      ],
      actions: [
        { name: "Multiattack", desc: "The troll makes three attacks: one with its bite and two with its claws." },
        { name: "Bite", desc: "Melee Weapon Attack: +7 to hit, reach 5 ft., one target. Hit: 7 (1d6 + 4) piercing damage." },
        { name: "Claw", desc: "Melee Weapon Attack: +7 to hit, reach 5 ft., one target. Hit: 11 (2d6 + 4) slashing damage." }
      ]
    },
    {
      name: "Wraith",
      cr: "5",
      xp: 1800,
      size: "Medium",
      type: "Undead",
      alignment: "Neutral Evil",
      ac: 13,
      acType: "",
      hp: "67 (9d8 + 27)",
      speed: "0 ft., fly 60 ft. (hover)",
      stats: { str: 6, dex: 16, con: 16, int: 12, wis: 14, cha: 15 },
      resistances: "Acid, Cold, Fire, Lightning, Thunder; Bludgeoning, Piercing, and Slashing from Nonmagical Attacks",
      immunities: "Necrotic, Poison",
      conditionImmunities: "Charmed, Exhaustion, Grappled, Paralysed, Petrified, Poisoned, Prone, Restrained",
      senses: "Darkvision 60 ft., passive Perception 12",
      languages: "understands languages it knew in life but can't speak",
      traits: [
        { name: "Incorporeal Movement", desc: "The wraith can move through other creatures and objects as if they were difficult terrain. It takes 5 (1d10) force damage if it ends its turn inside an object." },
        { name: "Sunlight Sensitivity", desc: "While in sunlight, the wraith has disadvantage on attack rolls, as well as on Wisdom (Perception) checks that rely on sight." }
      ],
      actions: [
        { name: "Life Drain", desc: "Melee Weapon Attack: +6 to hit, reach 5 ft., one creature. Hit: 21 (4d8 + 3) necrotic damage. The target must succeed on a DC 14 Constitution saving throw or its hit point maximum is reduced by an amount equal to the damage taken." }
      ]
    },
    {
      name: "Hill Giant",
      cr: "5",
      xp: 1800,
      size: "Huge",
      type: "Giant",
      alignment: "Chaotic Evil",
      ac: 13,
      acType: "natural armor",
      hp: "105 (10d12 + 40)",
      speed: "40 ft.",
      stats: { str: 21, dex: 8, con: 19, int: 5, wis: 9, cha: 6 },
      skills: "Perception +2",
      senses: "passive Perception 12",
      languages: "Giant",
      traits: [],
      actions: [
        { name: "Multiattack", desc: "The giant makes two greatclub attacks." },
        { name: "Greatclub", desc: "Melee Weapon Attack: +8 to hit, reach 10 ft., one target. Hit: 18 (3d8 + 5) bludgeoning damage." },
        { name: "Rock", desc: "Ranged Weapon Attack: +8 to hit, range 60/240 ft., one target. Hit: 21 (3d10 + 5) bludgeoning damage." }
      ]
    },
    {
      name: "Fire Elemental",
      cr: "5",
      xp: 1800,
      size: "Large",
      type: "Elemental",
      alignment: "Neutral",
      ac: 13,
      acType: "",
      hp: "102 (12d10 + 36)",
      speed: "50 ft.",
      stats: { str: 10, dex: 17, con: 16, int: 6, wis: 10, cha: 7 },
      resistances: "Bludgeoning, Piercing, and Slashing from Nonmagical Attacks",
      immunities: "Fire, Poison",
      conditionImmunities: "Exhaustion, Grappled, Paralysed, Petrified, Poisoned, Prone, Restrained, Unconscious",
      senses: "Darkvision 60 ft., passive Perception 10",
      languages: "Ignan",
      traits: [
        { name: "Fire Form", desc: "The elemental can move through a space as narrow as 1 inch wide without squeezing. A creature that touches the elemental or hits it with a melee attack takes 5 (1d10) fire damage." },
        { name: "Water Susceptibility", desc: "For every 5 feet the elemental moves in water, or for every gallon of water splashed on it, it takes 1 cold damage." }
      ],
      actions: [
        { name: "Multiattack", desc: "The elemental makes two touch attacks." },
        { name: "Touch", desc: "Melee Weapon Attack: +6 to hit, reach 5 ft., one target. Hit: 10 (2d6 + 3) fire damage." }
      ]
    },
    {
      name: "Mage",
      cr: "6",
      xp: 2300,
      size: "Medium",
      type: "Humanoid (any race)",
      alignment: "Any alignment",
      ac: 12,
      acType: "15 with mage armor",
      hp: "40 (9d8)",
      speed: "30 ft.",
      stats: { str: 9, dex: 14, con: 11, int: 17, wis: 12, cha: 11 },
      savingThrows: "Int +6, Wis +4",
      skills: "Arcana +6, History +6",
      senses: "passive Perception 11",
      languages: "any four languages",
      traits: [
        { name: "Spellcasting", desc: "The mage is a 9th-level spellcaster (Intelligence DC 14, +6 to hit with spell attacks). Prepared spells include fire bolt, mage armor, misty step, counterspell, fireball, cone of cold." }
      ],
      actions: [
        { name: "Dagger", desc: "Melee or Ranged Weapon Attack: +5 to hit, reach 5 ft. or range 20/60 ft., one target. Hit: 4 (1d4 + 2) piercing damage." }
      ]
    },
    {
      name: "Young Red Dragon",
      cr: "10",
      xp: 5900,
      size: "Large",
      type: "Dragon",
      alignment: "Chaotic Evil",
      ac: 18,
      acType: "natural armor",
      hp: "178 (17d10 + 85)",
      speed: "40 ft., climb 40 ft., fly 80 ft.",
      stats: { str: 23, dex: 10, con: 21, int: 14, wis: 11, cha: 19 },
      savingThrows: "Dex +4, Con +9, Wis +4, Cha +8",
      skills: "Perception +8, Stealth +4",
      immunities: "Fire",
      senses: "Blindsight 30 ft., Darkvision 120 ft., passive Perception 18",
      languages: "Common, Draconic",
      traits: [],
      actions: [
        { name: "Multiattack", desc: "The dragon makes three attacks: one with its bite and two with its claws." },
        { name: "Fire Breath (Recharge 5-6)", desc: "The dragon exhales fire in a 30-foot cone. Each creature in that area must make a DC 17 Dexterity saving throw, taking 56 (16d6) fire damage on a failed save, or half as much damage on a successful one." }
      ]
    },
    {
      name: "Stone Golem",
      cr: "10",
      xp: 5900,
      size: "Large",
      type: "Construct",
      alignment: "Unaligned",
      ac: 17,
      acType: "natural armor",
      hp: "178 (17d10 + 85)",
      speed: "30 ft.",
      stats: { str: 22, dex: 9, con: 20, int: 3, wis: 11, cha: 1 },
      immunities: "Poison, Psychic; Bludgeoning, Piercing, and Slashing from Nonmagical Attacks that aren't Adamantine",
      conditionImmunities: "Charmed, Exhaustion, Frightened, Paralysed, Petrified, Poisoned",
      senses: "Darkvision 120 ft., passive Perception 10",
      languages: "understands the languages of its creator but can't speak",
      traits: [
        { name: "Immutable Form", desc: "The golem is immune to any spell or effect that would alter its form." },
        { name: "Magic Resistance", desc: "The golem has advantage on saving throws against spells and other magical effects." }
      ],
      actions: [
        { name: "Multiattack", desc: "The golem makes two slam attacks." },
        { name: "Slam", desc: "Melee Weapon Attack: +10 to hit, reach 5 ft., one target. Hit: 19 (3d8 + 6) bludgeoning damage." },
        { name: "Slow (Recharge 5-6)", desc: "The golem targets one or more creatures it can see within 10 feet. Each target must succeed on a DC 17 Wisdom saving throw or be slowed for 1 minute." }
      ]
    },
    {
      name: "Vampire",
      cr: "13",
      xp: 10000,
      size: "Medium",
      type: "Undead (shapechanger)",
      alignment: "Lawful Evil",
      ac: 16,
      acType: "natural armor",
      hp: "144 (17d8 + 68)",
      speed: "30 ft.",
      stats: { str: 18, dex: 18, con: 18, int: 17, wis: 15, cha: 18 },
      savingThrows: "Dex +9, Wis +7, Cha +9",
      skills: "Perception +7, Stealth +9",
      resistances: "Necrotic; Bludgeoning, Piercing, and Slashing from Nonmagical Attacks",
      senses: "Darkvision 120 ft., passive Perception 17",
      languages: "the languages it knew in life",
      traits: [
        { name: "Shapechanger", desc: "If the vampire isn't in sunlight or running water, it can use its action to polymorph into a Tiny bat or Medium cloud of mist." },
        { name: "Regeneration", desc: "The vampire regains 20 hit points at the start of its turn if it has at least 1 hit point and isn't in sunlight or running water." }
      ],
      actions: [
        { name: "Multiattack (Vampire Form Only)", desc: "The vampire makes two attacks, only one of which can be a bite attack." },
        { name: "Unarmed Strike (Vampire Form Only)", desc: "Melee Weapon Attack: +9 to hit, reach 5 ft., one creature. Hit: 8 (1d8 + 4) bludgeoning damage." },
        { name: "Bite (Vampire or Bat Form Only)", desc: "Melee Weapon Attack: +9 to hit, reach 5 ft., one willing creature, or a creature grappled by the vampire. Hit: 7 (1d6 + 4) piercing damage plus 10 (3d6) necrotic damage." }
      ]
    },
    {
      name: "Adult Red Dragon",
      cr: "17",
      xp: 18000,
      size: "Huge",
      type: "Dragon",
      alignment: "Chaotic Evil",
      ac: 19,
      acType: "natural armor",
      hp: "256 (19d12 + 133)",
      speed: "40 ft., climb 40 ft., fly 80 ft.",
      stats: { str: 27, dex: 10, con: 25, int: 16, wis: 13, cha: 21 },
      savingThrows: "Dex +6, Con +13, Wis +7, Cha +11",
      skills: "Perception +13, Stealth +6",
      immunities: "Fire",
      senses: "Blindsight 60 ft., Darkvision 120 ft., passive Perception 23",
      languages: "Common, Draconic",
      traits: [
        { name: "Legendary Resistance (3/Day)", desc: "If the dragon fails a saving throw, it can choose to succeed instead." }
      ],
      actions: [
        { name: "Multiattack", desc: "The dragon can use its Frightful Presence. It then makes three attacks: one with its bite and two with its claws." },
        { name: "Fire Breath (Recharge 5-6)", desc: "The dragon exhales fire in a 60-foot cone. Each creature in that area must make a DC 21 Dexterity saving throw, taking 63 (18d6) fire damage on a failed save, or half as much on a successful one." }
      ]
    },
    {
      name: "Tarrasque",
      cr: "30",
      xp: 155000,
      size: "Gargantuan",
      type: "Monstrosity (titan)",
      alignment: "Unaligned",
      ac: 25,
      acType: "natural armor",
      hp: "676 (33d20 + 330)",
      speed: "40 ft.",
      stats: { str: 30, dex: 11, con: 30, int: 3, wis: 11, cha: 11 },
      savingThrows: "Int +5, Wis +9, Cha +9",
      immunities: "Fire, Poison; Bludgeoning, Piercing, and Slashing from Nonmagical Attacks",
      conditionImmunities: "Charmed, Frightened, Paralysed, Poisoned",
      senses: "Blindsight 120 ft., passive Perception 10",
      languages: "",
      traits: [
        { name: "Legendary Resistance (3/Day)", desc: "If the tarrasque fails a saving throw, it can choose to succeed instead." },
        { name: "Reflective Carapace", desc: "Any time the tarrasque is targeted by a line spell, a spell with a ranged attack roll, or magic missile, roll a d6. On a 1 to 5, the tarrasque is unaffected. On a 6, the spell is reflected back at the caster." }
      ],
      actions: [
        { name: "Multiattack", desc: "The tarrasque can use its Frightful Presence. It then makes five attacks: one with its bite, two with its claws, one with its horns, and one with its tail." },
        { name: "Bite", desc: "Melee Weapon Attack: +19 to hit, reach 10 ft., one target. Hit: 36 (4d12 + 10) piercing damage." }
      ]
    }
  ],

  // SRD 5.2.1 Environmental Hazards
  hazards: [
    { name: "Extreme Cold", effect: "DC 10 Constitution saving throw per hour or gain 1 level of Exhaustion unless wearing cold weather gear." },
    { name: "Extreme Heat", effect: "DC 10 Constitution saving throw per hour (DC +1 per hour) or gain 1 level of Exhaustion unless provided medium water." },
    { name: "High Altitude", effect: "Breathing difficulty above 10,000 feet. Creatures unaccustomed must succeed on DC 10 Constitution save per day or gain 1 level of Exhaustion." },
    { name: "Quicksand", effect: "Sinks 1d4 + 1 feet. DC 10 Strength check to escape. Creatures trapped sink further each turn." },
    { name: "Frigid Water", effect: "DC 10 Constitution save every 1 minute or gain 1 level of Exhaustion. Creature dies after minutes equal to Constitution score." },
    { name: "Heavy Precipitation", effect: "Everything within area is lightly obscured. Disadvantage on Wisdom (Perception) checks relying on sight or hearing." }
  ],

  // Conditions SRD 5.2.1 Data
  conditions: [
    { name: "Blinded", desc: "Can't see and automatically fails checks that require sight. Attack rolls against the creature have advantage, and creature's attack rolls have disadvantage." },
    { name: "Charmed", desc: "Can't attack the charmer or target charmer with harmful abilities or magical effects. Charmer has advantage on social interaction checks." },
    { name: "Frightened", desc: "Disadvantage on ability checks and attack rolls while source of fear is in sight. Can't willingly move closer to the source of fear." },
    { name: "Grappled", desc: "Speed becomes 0 and can't benefit from any bonus to speed. Ends if grappler is incapacitated or moved away." },
    { name: "Incapacitated", desc: "Can't take actions or reactions." },
    { name: "Invisible", desc: "Impossible to see without magic or special senses. Attacks against creature have disadvantage, creature's attacks have advantage." },
    { name: "Paralyzed", desc: "Incapacitated and can't move or speak. Automatically fails Strength and Dexterity saving throws. Attacks against creature have advantage, and melee attacks within 5 ft. are critical hits." },
    { name: "Petrified", desc: "Transformed into solid inanimate substance. Weight increases by x10. Incapacitated, unaware, automatically fails Str/Dex saves. Resistance to all damage." },
    { name: "Poisoned", desc: "Disadvantage on attack rolls and ability checks." },
    { name: "Prone", desc: "Can only crawl or spend half speed to stand. Disadvantage on attack rolls. Attacks against creature have advantage if within 5 ft., otherwise disadvantage." },
    { name: "Restrained", desc: "Speed becomes 0. Attacks against creature have advantage, creature's attacks have disadvantage. Disadvantage on Dexterity saving throws." },
    { name: "Stunned", desc: "Incapacitated, can't move, and speaks falteringly. Automatically fails Strength and Dexterity saving throws. Attacks against creature have advantage." },
    { name: "Unconscious", desc: "Incapacitated, can't move or speak, unaware. Drops held items and falls prone. Automatically fails Str/Dex saves. Attacks within 5 ft. are critical hits." }
  ],

  // XP Threshold Table per character level (Easy, Medium, Hard, Deadly)
  xpThresholds: {
    1:  [25, 50, 75, 100],
    2:  [50, 100, 150, 200],
    3:  [75, 150, 225, 400],
    4:  [125, 250, 375, 500],
    5:  [250, 500, 750, 1100],
    6:  [300, 600, 900, 1400],
    7:  [350, 700, 1100, 1700],
    8:  [450, 900, 1400, 2100],
    9:  [550, 1100, 1600, 2400],
    10: [600, 1200, 1900, 2800],
    11: [800, 1600, 2400, 3600],
    12: [1000, 2000, 3000, 4500],
    13: [1100, 2200, 3400, 5100],
    14: [1250, 2500, 3800, 5700],
    15: [1400, 2800, 4300, 6400],
    16: [1600, 3200, 4800, 7200],
    17: [2000, 3900, 5900, 8800],
    18: [2100, 4200, 6300, 9500],
    19: [2400, 4900, 7300, 10900],
    20: [2800, 5700, 8500, 12700]
  },

  // SRD Loot Tables categorized by CR Tiers
  lootTables: {
    "0-4": {
      coins: [
        { range: [1, 30], cp: "6d6", sp: "3d6" },
        { range: [31, 60], sp: "4d6", gp: "2d6" },
        { range: [61, 85], gp: "3d6", ep: "1d6" },
        { range: [86, 100], gp: "4d6", pp: "1d4" }
      ],
      gemsArt: [
        "10 gp Gemstone (Lapis lazuli, Malachite, or Turquoise)",
        "25 gp Art Object (Silver ewer, Carved bone statuette)",
        "50 gp Gemstone (Bloodstone, Carnelian, or Onyx)"
      ],
      magicItems: [
        "Potion of Healing",
        "Spell Scroll (1st level)",
        "Bag of Holding",
        "Wand of Magic Missiles",
        "Ring of Protection"
      ]
    },
    "5-10": {
      coins: [
        { range: [1, 30], cp: "2d6x100", sp: "2d6x10", gp: "4d6x10" },
        { range: [31, 60], gp: "2d8x10", pp: "1d6x10" },
        { range: [61, 85], gp: "4d8x10", pp: "2d4x10" },
        { range: [86, 100], gp: "1d10x100", pp: "3d6x10" }
      ],
      gemsArt: [
        "100 gp Gemstone (Amber, Amethyst, or Garnet)",
        "250 gp Art Object (Gold ring set with bloodstone, Carved ivory statuette)",
        "500 gp Gemstone (Alexandrite, Aquamarine, or Black Pearl)"
      ],
      magicItems: [
        "Potion of Greater Healing",
        "Weapon +1",
        "Shield +1",
        "Cloak of Elvenkind",
        "Boots of Speed",
        "Flame Tongue Sword"
      ]
    },
    "11-16": {
      coins: [
        { range: [1, 50], gp: "4d6x100", pp: "5d6x10" },
        { range: [51, 100], gp: "2d6x1000", pp: "1d6x100" }
      ],
      gemsArt: [
        "1,000 gp Gemstone (Emerald, Opal, or Sapphire)",
        "2,500 gp Art Object (Fine cloth jacket with gold embroidery, Platinum ring)"
      ],
      magicItems: [
        "Potion of Superior Healing",
        "Armor +1",
        "Weapon +2",
        "Staff of Power",
        "Ring of Regeneration"
      ]
    }
  }
};
