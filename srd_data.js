/**
 * Certified SRD 5.2.1 Data Set for DM Encounter & Loot Toolkit
 * Content licensed under CC-BY-4.0 from Wizards of the Coast LLC.
 */

window.SRD_DATA = {
  // Monster SRD Database
  monsters: [
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
      name: "Chimera",
      cr: "6",
      xp: 2300,
      size: "Large",
      type: "Monstrosity",
      alignment: "Chaotic Evil",
      ac: 14,
      acType: "natural armor",
      hp: "114 (12d10 + 48)",
      speed: "30 ft., fly 60 ft.",
      stats: { str: 19, dex: 11, con: 19, int: 3, wis: 14, cha: 10 },
      skills: "Perception +8",
      senses: "Darkvision 60 ft., passive Perception 18",
      languages: "understands Draconic but can't speak",
      traits: [],
      actions: [
        { name: "Multiattack", desc: "The chimera makes three attacks: one with its bite, one with its horns, and one with its claws. When its fire breath is available, it can use the breath in place of its bite." },
        { name: "Fire Breath (Recharge 5-6)", desc: "The dragon head exhales fire in a 15-foot cone. Each creature in that area must make a DC 15 Dexterity saving throw, taking 31 (7d8) fire damage on a failed save, or half as much damage on a successful one." }
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
