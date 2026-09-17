/**
 * DM Encounter & Loot Toolkit Core Logic
 * Operates on window.SRD_DATA
 */

document.addEventListener("DOMContentLoaded", () => {
  // Valid Pro License Keys
  const VALID_PRO_KEYS = ["DM-TOOLKIT-PRO-2025", "DM-HERO-PRO", "SRD521-PRO-MASTER"];
  let isProUnlocked = false;
  let currentEncounterMonsters = [];
  let currentDifficulty = "medium";
  let currentTargetXP = 0;
  let currentActualXP = 0;

  // DOM Elements
  const partySizeInput = document.getElementById("party-size");
  const partyLevelInput = document.getElementById("party-level");
  const difficultySelect = document.getElementById("difficulty");
  const generateBtn = document.getElementById("generate-btn");
  const regenerateBtn = document.getElementById("regenerate-btn");
  const saveEncounterBtn = document.getElementById("save-encounter-btn");
  const savedEncountersList = document.getElementById("saved-encounters-list");
  const encounterSummary = document.getElementById("encounter-summary");
  const monsterGrid = document.getElementById("monster-grid");
  const rollLootBtn = document.getElementById("roll-loot-btn");
  const lootOutput = document.getElementById("loot-output");
  const printCardsContainer = document.getElementById("print-cards-container");
  const printBtn = document.getElementById("print-btn");
  const conditionsGrid = document.getElementById("conditions-grid");
  const diceLog = document.getElementById("dice-log");
  const clearDiceLogBtn = document.getElementById("clear-dice-log");

  // Pro Modal Elements
  const proModalBtn = document.getElementById("pro-modal-btn");
  const proModal = document.getElementById("pro-modal");
  const closeModalBtn = document.getElementById("close-modal-btn");
  const activateProBtn = document.getElementById("activate-pro-btn");
  const licenseKeyInput = document.getElementById("license-key");
  const proStatusMsg = document.getElementById("pro-status-msg");
  const proPartyNote = document.getElementById("pro-party-note");
  const adBanner = document.getElementById("ad-banner");

  // Utility: Roll Die by sides
  function rollDie(sides) {
    return Math.floor(Math.random() * sides) + 1;
  }

  // Utility: Parse Die String e.g. "4d6", "2d6x10", "1d4"
  function rollDiceString(str) {
    if (!str) return 0;
    if (str.includes("x")) {
      const parts = str.split("x");
      return rollDiceString(parts[0]) * parseInt(parts[1], 10);
    }
    const match = str.match(/(\d+)d(\d+)/);
    if (!match) return parseInt(str, 10) || 0;
    const num = parseInt(match[1], 10);
    const sides = parseInt(match[2], 10);
    let total = 0;
    for (let i = 0; i < num; i++) {
      total += Math.floor(Math.random() * sides) + 1;
    }
    return total;
  }

  // Calculate Party XP Budget
  function getPartyXPBudget(partySize, partyLevel, difficulty) {
    const diffIndex = { easy: 0, medium: 1, hard: 2, deadly: 3 }[difficulty] || 1;
    const levelThresholds = window.SRD_DATA.xpThresholds[partyLevel] || window.SRD_DATA.xpThresholds[1];
    const basePerChar = levelThresholds[diffIndex];
    return basePerChar * partySize;
  }

  // Generate Encounter Compositions
  function generateEncounter() {
    let partySize = parseInt(partySizeInput.value, 10) || 4;
    const partyLevel = Math.min(Math.max(parseInt(partyLevelInput.value, 10) || 1, 1), 20);
    currentDifficulty = difficultySelect.value;

    // Enforce Pro Max Cap if not unlocked
    if (!isProUnlocked && partySize > 10) {
      partySize = 10;
      partySizeInput.value = 10;
      alert("Free tier limited to party size <= 10. Unlock Pro for up to 20!");
    }

    const xpBudget = getPartyXPBudget(partySize, partyLevel, currentDifficulty);
    const availableMonsters = window.SRD_DATA.monsters.filter(m => m.xp <= xpBudget);

    if (availableMonsters.length === 0) {
      monsterGrid.innerHTML = `<p class="placeholder-text">No suitable SRD monsters found for this budget. Try adjusting level/difficulty.</p>`;
      return;
    }

    // Select 1 to 3 monster types to build the encounter
    const numTypes = Math.floor(Math.random() * 2) + 1;
    const selectedMonsters = [];
    let currentXP = 0;

    for (let i = 0; i < numTypes; i++) {
      const candidate = availableMonsters[Math.floor(Math.random() * availableMonsters.length)];
      const maxQty = Math.max(1, Math.floor((xpBudget - currentXP) / candidate.xp));
      const qty = Math.min(maxQty, Math.floor(Math.random() * 4) + 1);

      selectedMonsters.push({
        monster: candidate,
        count: qty
      });
      currentXP += candidate.xp * qty;
      if (currentXP >= xpBudget) break;
    }

    currentEncounterMonsters = selectedMonsters;
    currentTargetXP = xpBudget;
    currentActualXP = currentXP;
    renderEncounter(xpBudget, currentXP);
  }

  // Render Encounter Cards and Summary
  function renderEncounter(targetXP, actualXP) {
    encounterSummary.innerHTML = `
      <div>Target XP: <span class="summary-tag">${targetXP.toLocaleString()} XP</span></div>
      <div>Encounter XP: <span class="summary-tag">${actualXP.toLocaleString()} XP</span></div>
      <div>Difficulty: <span class="summary-tag" style="text-transform: capitalize">${currentDifficulty}</span></div>
    `;

    monsterGrid.innerHTML = "";
    printCardsContainer.innerHTML = "";

    if (currentEncounterMonsters.length === 0) {
      monsterGrid.innerHTML = `<p class="placeholder-text">No monsters generated.</p>`;
      return;
    }

    currentEncounterMonsters.forEach(({ monster, count }, idx) => {
      const cardHTML = renderStatCardHTML(monster, count, idx);
      monsterGrid.insertAdjacentHTML("beforeend", cardHTML);
      printCardsContainer.insertAdjacentHTML("beforeend", cardHTML);
    });

    // Attach copy event listeners
    document.querySelectorAll(".copy-stat-btn").forEach(btn => {
      btn.addEventListener("click", (e) => {
        const monsterIdx = e.target.dataset.index;
        const entry = currentEncounterMonsters[monsterIdx];
        if (entry) {
          const formattedText = formatMonsterPlainText(entry.monster, entry.count);
          navigator.clipboard.writeText(formattedText).then(() => {
            const originalText = e.target.textContent;
            e.target.textContent = "✓ Copied!";
            e.target.classList.add("btn-copied");
            setTimeout(() => {
              e.target.textContent = originalText;
              e.target.classList.remove("btn-copied");
            }, 1800);
          }).catch(err => {
            console.error("Copy failed", err);
          });
        }
      });
    });
  }

  // Format Plain Text Stat Block
  function formatMonsterPlainText(m, count = 1) {
    const countHeader = count > 1 ? ` (x${count})` : "";
    const calcAbilityMod = (val) => {
      const mod = Math.floor((val - 10) / 2);
      return mod >= 0 ? `+${mod}` : `${mod}`;
    };
    let text = `${m.name}${countHeader}\n${m.size} ${m.type}, ${m.alignment}\n`;
    text += `Armor Class: ${m.ac} ${m.acType ? `(${m.acType})` : ""}\n`;
    text += `Hit Points: ${m.hp}\nSpeed: ${m.speed}\n`;
    text += `STR: ${m.stats.str} (${calcAbilityMod(m.stats.str)}) | DEX: ${m.stats.dex} (${calcAbilityMod(m.stats.dex)}) | CON: ${m.stats.con} (${calcAbilityMod(m.stats.con)})\n`;
    text += `INT: ${m.stats.int} (${calcAbilityMod(m.stats.int)}) | WIS: ${m.stats.wis} (${calcAbilityMod(m.stats.wis)}) | CHA: ${m.stats.cha} (${calcAbilityMod(m.stats.cha)})\n`;
    text += `Challenge: ${m.cr} (${m.xp} XP)\nSenses: ${m.senses}\nLanguages: ${m.languages}\n`;
    if (m.traits && m.traits.length > 0) {
      text += `\n--- TRAITS ---\n`;
      m.traits.forEach(t => { text += `${t.name}: ${t.desc}\n`; });
    }
    if (m.actions && m.actions.length > 0) {
      text += `\n--- ACTIONS ---\n`;
      m.actions.forEach(a => { text += `${a.name}: ${a.desc}\n`; });
    }
    return text;
  }

  // Render Single Monster Stat Card HTML
  function renderStatCardHTML(m, count = 1, idx = 0) {
    const countBadge = count > 1 ? ` (x${count})` : "";
    const calcAbilityMod = (val) => {
      const mod = Math.floor((val - 10) / 2);
      return mod >= 0 ? `+${mod}` : `${mod}`;
    };

    const traitsHTML = (m.traits || []).map(t => `<p><strong>${t.name}.</strong> ${t.desc}</p>`).join("");
    const actionsHTML = (m.actions || []).map(a => `<p><strong>${a.name}.</strong> ${a.desc}</p>`).join("");

    return `
      <div class="stat-card">
        <div class="stat-header">
          <div class="stat-header-top">
            <h3>${m.name}${countBadge}</h3>
            <button class="btn btn-sm btn-secondary copy-stat-btn" data-index="${idx}">📋 Copy</button>
          </div>
          <div class="stat-meta">${m.size} ${m.type}, ${m.alignment}</div>
        </div>
        <div class="stat-vitals">
          <div>Armor Class: ${m.ac} ${m.acType ? `(${m.acType})` : ""}</div>
          <div>Hit Points: ${m.hp}</div>
          <div>Speed: ${m.speed}</div>
        </div>
        <div class="stat-scores">
          <div class="score-box"><label>STR</label>${m.stats.str} (${calcAbilityMod(m.stats.str)})</div>
          <div class="score-box"><label>DEX</label>${m.stats.dex} (${calcAbilityMod(m.stats.dex)})</div>
          <div class="score-box"><label>CON</label>${m.stats.con} (${calcAbilityMod(m.stats.con)})</div>
          <div class="score-box"><label>INT</label>${m.stats.int} (${calcAbilityMod(m.stats.int)})</div>
          <div class="score-box"><label>WIS</label>${m.stats.wis} (${calcAbilityMod(m.stats.wis)})</div>
          <div class="score-box"><label>CHA</label>${m.stats.cha} (${calcAbilityMod(m.stats.cha)})</div>
        </div>
        <div class="stat-details">
          <p><strong>Challenge:</strong> ${m.cr} (${m.xp} XP)</p>
          <p><strong>Senses:</strong> ${m.senses}</p>
          <p><strong>Languages:</strong> ${m.languages}</p>
          ${traitsHTML ? `<div class="stat-section-title">Traits</div>${traitsHTML}` : ""}
          ${actionsHTML ? `<div class="stat-section-title">Actions</div>${actionsHTML}` : ""}
        </div>
      </div>
    `;
  }

  // Roll Loot for Current Encounter
  function rollLoot() {
    const partyLevel = parseInt(partyLevelInput.value, 10) || 1;
    let tierKey = "0-4";
    if (partyLevel >= 11) tierKey = "11-16";
    else if (partyLevel >= 5) tierKey = "5-10";

    const tierData = window.SRD_DATA.lootTables[tierKey];
    if (!tierData) return;

    // Roll Coinage
    const coinRoll = Math.floor(Math.random() * 100) + 1;
    const coinMatch = tierData.coins.find(c => coinRoll >= c.range[0] && coinRoll <= c.range[1]) || tierData.coins[0];
    const coinsEarned = [];

    if (coinMatch.cp) coinsEarned.push(`${rollDiceString(coinMatch.cp)} CP`);
    if (coinMatch.sp) coinsEarned.push(`${rollDiceString(coinMatch.sp)} SP`);
    if (coinMatch.ep) coinsEarned.push(`${rollDiceString(coinMatch.ep)} EP`);
    if (coinMatch.gp) coinsEarned.push(`${rollDiceString(coinMatch.gp)} GP`);
    if (coinMatch.pp) coinsEarned.push(`${rollDiceString(coinMatch.pp)} PP`);

    // Roll Gems / Art
    const gemOrArt = tierData.gemsArt[Math.floor(Math.random() * tierData.gemsArt.length)];

    // Roll Magic Items
    const magicItem = tierData.magicItems[Math.floor(Math.random() * tierData.magicItems.length)];

    lootOutput.innerHTML = `
      <p><strong>Currency:</strong> ${coinsEarned.join(", ") || "None"}</p>
      <p><strong>Valuables:</strong> ${gemOrArt}</p>
      <p><strong>Magic Item:</strong> ${magicItem}</p>
    `;
  }

  // Conditions Quick Reference Display
  function renderConditions() {
    if (!window.SRD_DATA.conditions) return;
    conditionsGrid.innerHTML = window.SRD_DATA.conditions.map(c => `
      <div class="condition-card">
        <h4>${c.name}</h4>
        <p>${c.desc}</p>
      </div>
    `).join("");
  }

  // Saved Encounters Manager (LocalStorage)
  function saveCurrentEncounter() {
    if (currentEncounterMonsters.length === 0) return;
    const name = prompt("Enter a label for this saved encounter:", `Lvl ${partyLevelInput.value} ${currentDifficulty.toUpperCase()} Encounter`);
    if (!name) return;

    const saved = JSON.parse(localStorage.getItem("srd_saved_encounters") || "[]");
    saved.push({
      id: Date.now(),
      name: name,
      partySize: partySizeInput.value,
      partyLevel: partyLevelInput.value,
      difficulty: currentDifficulty,
      targetXP: currentTargetXP,
      actualXP: currentActualXP,
      monsters: currentEncounterMonsters
    });
    localStorage.setItem("srd_saved_encounters", JSON.stringify(saved));
    renderSavedEncounters();
  }

  function renderSavedEncounters() {
    const saved = JSON.parse(localStorage.getItem("srd_saved_encounters") || "[]");
    if (saved.length === 0) {
      savedEncountersList.innerHTML = `<p class="placeholder-text">No saved encounters yet. Generate an encounter and click "Save".</p>`;
      return;
    }

    savedEncountersList.innerHTML = saved.map(item => `
      <div class="saved-item">
        <div>
          <strong>${item.name}</strong>
          <span class="saved-meta">(${item.monsters.map(m => `${m.monster.name} x${m.count}`).join(", ")})</span>
        </div>
        <div class="saved-actions">
          <button class="btn btn-sm btn-primary load-encounter-btn" data-id="${item.id}">Load</button>
          <button class="btn btn-sm btn-secondary delete-encounter-btn" data-id="${item.id}">Delete</button>
        </div>
      </div>
    `).join("");

    document.querySelectorAll(".load-encounter-btn").forEach(btn => {
      btn.addEventListener("click", (e) => {
        const id = parseInt(e.target.dataset.id, 10);
        const item = saved.find(s => s.id === id);
        if (item) {
          partySizeInput.value = item.partySize;
          partyLevelInput.value = item.partyLevel;
          difficultySelect.value = item.difficulty;
          currentDifficulty = item.difficulty;
          currentEncounterMonsters = item.monsters;
          renderEncounter(item.targetXP, item.actualXP);
        }
      });
    });

    document.querySelectorAll(".delete-encounter-btn").forEach(btn => {
      btn.addEventListener("click", (e) => {
        const id = parseInt(e.target.dataset.id, 10);
        const updated = saved.filter(s => s.id !== id);
        localStorage.setItem("srd_saved_encounters", JSON.stringify(updated));
        renderSavedEncounters();
      });
    });
  }

  // Dice Roller Handler
  document.querySelectorAll(".btn-dice").forEach(btn => {
    btn.addEventListener("click", () => {
      const sides = parseInt(btn.dataset.sides, 10);
      const roll = rollDie(sides);
      const placeholder = diceLog.querySelector(".dice-placeholder");
      if (placeholder) diceLog.innerHTML = "";

      const badge = document.createElement("span");
      badge.className = "dice-badge";
      badge.textContent = `d${sides}: ${roll}`;
      diceLog.prepend(badge);
    });
  });

  if (clearDiceLogBtn) {
    clearDiceLogBtn.addEventListener("click", () => {
      diceLog.innerHTML = `<span class="dice-placeholder">Click a die above to roll...</span>`;
    });
  }

  // Pro Unlock Activation
  function activateProKey() {
    const key = licenseKeyInput.value.trim().toUpperCase();
    if (VALID_PRO_KEYS.includes(key)) {
      isProUnlocked = true;
      proStatusMsg.className = "status-msg success";
      proStatusMsg.textContent = "Pro Unlocked! Extended party sizes & ad-free experience activated.";
      proPartyNote.classList.remove("hidden");
      partySizeInput.setAttribute("max", "20");
      adBanner.style.display = "none";
      setTimeout(() => proModal.classList.add("hidden"), 1500);
    } else {
      proStatusMsg.className = "status-msg error";
      proStatusMsg.textContent = "Invalid license key. Try 'DM-TOOLKIT-PRO-2025' or 'DM-HERO-PRO'.";
    }
  }

  // Event Listeners
  generateBtn.addEventListener("click", generateEncounter);
  regenerateBtn.addEventListener("click", generateEncounter);
  difficultySelect.addEventListener("change", generateEncounter);
  saveEncounterBtn.addEventListener("click", saveCurrentEncounter);
  rollLootBtn.addEventListener("click", rollLoot);
  printBtn.addEventListener("click", () => window.print());

  proModalBtn.addEventListener("click", () => {
    proStatusMsg.textContent = "";
    proModal.classList.remove("hidden");
  });
  closeModalBtn.addEventListener("click", () => proModal.classList.add("hidden"));
  activateProBtn.addEventListener("click", activateProKey);

  // Initializations
  renderConditions();
  renderSavedEncounters();
  generateEncounter();
});
