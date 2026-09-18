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
  let activeRefTab = "conditions";

  // DOM Elements
  const partySizeInput = document.getElementById("party-size");
  const partyLevelInput = document.getElementById("party-level");
  const difficultySelect = document.getElementById("difficulty");
  const generateBtn = document.getElementById("generate-btn");
  const regenerateBtn = document.getElementById("regenerate-btn");
  const encounterSummary = document.getElementById("encounter-summary");
  const monsterGrid = document.getElementById("monster-grid");
  const rollLootBtn = document.getElementById("roll-loot-btn");
  const lootOutput = document.getElementById("loot-output");
  const printCardsContainer = document.getElementById("print-cards-container");
  const printBtn = document.getElementById("print-btn");

  // Save / Copy Elements
  const saveEncounterBtn = document.getElementById("save-encounter-btn");
  const copyTextBtn = document.getElementById("copy-text-btn");
  const savedEncountersList = document.getElementById("saved-encounters-list");

  // Dice Roller Elements
  const diceBtns = document.querySelectorAll(".btn-dice");
  const diceModInput = document.getElementById("dice-mod");
  const diceQtyInput = document.getElementById("dice-qty");
  const diceLog = document.getElementById("dice-log");
  const clearDiceLogBtn = document.getElementById("clear-dice-log-btn");

  // Quick Reference Elements
  const tabConditionsBtn = document.getElementById("tab-conditions-btn");
  const tabHazardsBtn = document.getElementById("tab-hazards-btn");
  const refContent = document.getElementById("ref-content");

  // Pro Modal Elements
  const proModalBtn = document.getElementById("pro-modal-btn");
  const proModal = document.getElementById("pro-modal");
  const closeModalBtn = document.getElementById("close-modal-btn");
  const activateProBtn = document.getElementById("activate-pro-btn");
  const licenseKeyInput = document.getElementById("license-key");
  const proStatusMsg = document.getElementById("pro-status-msg");
  const proPartyNote = document.getElementById("pro-party-note");
  const headerProBadge = document.getElementById("header-pro-badge");
  const adBanner = document.getElementById("ad-banner");

  // Utility: Parse Die String e.g. "4d6", "2d6x10"
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

  // Quick Dice Roller Functionality
  function rollSelectedDie(diceType) {
    const sides = parseInt(diceType.replace("d", ""), 10) || 20;
    const qty = Math.max(1, parseInt(diceQtyInput.value, 10) || 1);
    const mod = parseInt(diceModInput.value, 10) || 0;

    const rolls = [];
    let total = 0;
    for (let i = 0; i < qty; i++) {
      const r = Math.floor(Math.random() * sides) + 1;
      rolls.push(r);
      total += r;
    }
    total += mod;

    const modSign = mod >= 0 ? `+${mod}` : `${mod}`;
    const modStr = mod !== 0 ? ` (${modSign})` : "";
    const rollsStr = qty > 1 ? ` [${rolls.join(", ")}]` : "";
    const isNat20 = sides === 20 && rolls.includes(20);

    const entry = document.createElement("div");
    entry.className = isNat20 ? "dice-roll-entry dice-roll-crit" : "dice-roll-entry";
    entry.innerHTML = `<strong>${qty}${diceType}${modStr}:</strong> Total = <strong>${total}</strong>${rollsStr}${isNat20 ? " 🎉 NAT 20!" : ""}`;

    if (diceLog.querySelector(".placeholder-text")) {
      diceLog.innerHTML = "";
    }
    diceLog.appendChild(entry);
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
    renderEncounter(xpBudget, currentXP);
  }

  // Render Encounter Cards and Summary
  function renderEncounter(targetXP, actualXP) {
    encounterSummary.innerHTML = `
      <div>Target XP: <span class="summary-tag">${targetXP.toLocaleString()} XP</span></div>
      <div>Encounter XP: <span class="summary-tag">${actualXP.toLocaleString()} XP</span></div>
      <div>Difficulty: <span class="summary-tag" style="text-transform: capitalize">${currentDifficulty}</span></div>
      ${isProUnlocked ? `<div>Pro Mode: <span class="summary-tag">✨ Active (+20 Max Party Cap)</span></div>` : ""}
    `;

    monsterGrid.innerHTML = "";
    printCardsContainer.innerHTML = "";

    if (currentEncounterMonsters.length === 0) {
      monsterGrid.innerHTML = `<p class="placeholder-text">No monsters generated.</p>`;
      return;
    }

    currentEncounterMonsters.forEach(({ monster, count }) => {
      const cardHTML = renderStatCardHTML(monster, count);
      monsterGrid.insertAdjacentHTML("beforeend", cardHTML);
      printCardsContainer.insertAdjacentHTML("beforeend", cardHTML);
    });
  }

  // Render Single Monster Stat Card HTML
  function renderStatCardHTML(m, count = 1) {
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
          <h3>${m.name}${countBadge}</h3>
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

  // Copy Encounter Stat Block to Clipboard as Plain Text
  function copyEncounterText() {
    if (currentEncounterMonsters.length === 0) {
      alert("No active encounter to copy!");
      return;
    }

    const textLines = ["=== ENCOUNTER STAT BLOCKS ===", ""];
    currentEncounterMonsters.forEach(({ monster: m, count }) => {
      textLines.push(`${m.name.toUpperCase()}${count > 1 ? ` (x${count})` : ""}`);
      textLines.push(`${m.size} ${m.type}, ${m.alignment}`);
      textLines.push(`AC: ${m.ac} (${m.acType || 'natural'}) | HP: ${m.hp} | Speed: ${m.speed}`);
      textLines.push(`STR: ${m.stats.str} | DEX: ${m.stats.dex} | CON: ${m.stats.con} | INT: ${m.stats.int} | WIS: ${m.stats.wis} | CHA: ${m.stats.cha}`);
      textLines.push(`CR: ${m.cr} (${m.xp} XP)`);
      if (m.traits && m.traits.length) {
        textLines.push("Traits:");
        m.traits.forEach(t => textLines.push(` - ${t.name}: ${t.desc}`));
      }
      if (m.actions && m.actions.length) {
        textLines.push("Actions:");
        m.actions.forEach(a => textLines.push(` - ${a.name}: ${a.desc}`));
      }
      textLines.push("----------------------------------------");
    });

    navigator.clipboard.writeText(textLines.join("\n")).then(() => {
      alert("Encounter stat blocks copied to clipboard!");
    }).catch(err => {
      console.error("Copy failed:", err);
    });
  }

  // Save Current Encounter to LocalStorage
  function saveCurrentEncounter() {
    if (currentEncounterMonsters.length === 0) {
      alert("Generate an encounter first!");
      return;
    }

    const saved = JSON.parse(localStorage.getItem("srd_saved_encounters") || "[]");
    const name = prompt("Enter a title for this encounter:", `Level ${partyLevelInput.value} ${currentDifficulty.toUpperCase()} Encounter`);
    if (!name) return;

    const newSaved = {
      id: Date.now(),
      name,
      partySize: partySizeInput.value,
      partyLevel: partyLevelInput.value,
      difficulty: currentDifficulty,
      monsters: currentEncounterMonsters,
      savedAt: new Date().toLocaleDateString()
    };

    saved.push(newSaved);
    localStorage.setItem("srd_saved_encounters", JSON.stringify(saved));
    renderSavedEncounters();
  }

  // Render Saved Encounters List
  function renderSavedEncounters() {
    const saved = JSON.parse(localStorage.getItem("srd_saved_encounters") || "[]");
    if (saved.length === 0) {
      savedEncountersList.innerHTML = `<p class="placeholder-text">No saved encounters yet. Click "Save Encounter" above to store your favorites locally!</p>`;
      return;
    }

    savedEncountersList.innerHTML = saved.map(e => `
      <div class="saved-card">
        <div class="saved-card-header">
          <span>${e.name}</span>
          <span class="saved-card-meta">${e.savedAt}</span>
        </div>
        <div class="saved-card-meta">
          Party: Size ${e.partySize}, Lvl ${e.partyLevel} (${e.difficulty})
          <br>Monsters: ${e.monsters.map(m => `${m.monster.name} x${m.count}`).join(", ")}
        </div>
        <div class="saved-card-actions">
          <button class="btn btn-secondary btn-sm" onclick="loadSavedEncounter(${e.id})">📂 Load</button>
          <button class="btn btn-secondary btn-sm" onclick="deleteSavedEncounter(${e.id})">🗑️ Delete</button>
        </div>
      </div>
    `).join("");
  }

  // Global Handlers for Saved Encounters
  window.loadSavedEncounter = (id) => {
    const saved = JSON.parse(localStorage.getItem("srd_saved_encounters") || "[]");
    const item = saved.find(e => e.id === id);
    if (!item) return;

    partySizeInput.value = item.partySize;
    partyLevelInput.value = item.partyLevel;
    difficultySelect.value = item.difficulty;
    currentEncounterMonsters = item.monsters;
    currentDifficulty = item.difficulty;

    const totalXP = currentEncounterMonsters.reduce((sum, m) => sum + (m.monster.xp * m.count), 0);
    renderEncounter(totalXP, totalXP);
  };

  window.deleteSavedEncounter = (id) => {
    let saved = JSON.parse(localStorage.getItem("srd_saved_encounters") || "[]");
    saved = saved.filter(e => e.id !== id);
    localStorage.setItem("srd_saved_encounters", JSON.stringify(saved));
    renderSavedEncounters();
  };

  // Quick Reference Tab Rendering
  function renderQuickReference() {
    if (activeRefTab === "conditions") {
      tabConditionsBtn.classList.add("active");
      tabHazardsBtn.classList.remove("active");
      refContent.innerHTML = `
        <div class="ref-grid">
          ${window.SRD_DATA.conditions.map(c => `
            <div class="ref-card">
              <h4>${c.name}</h4>
              <p>${c.desc}</p>
            </div>
          `).join("")}
        </div>
      `;
    } else {
      tabHazardsBtn.classList.add("active");
      tabConditionsBtn.classList.remove("active");
      refContent.innerHTML = `
        <div class="ref-grid">
          ${window.SRD_DATA.hazards.map(h => `
            <div class="ref-card">
              <h4>${h.name}</h4>
              <p>${h.effect}</p>
            </div>
          `).join("")}
        </div>
      `;
    }
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

    // Bonus Pro Loot Item if Pro is Unlocked
    const proBonus = isProUnlocked ? `<p><strong>✨ Pro Bonus Item:</strong> ${tierData.magicItems[Math.floor(Math.random() * tierData.magicItems.length)]}</p>` : "";

    lootOutput.innerHTML = `
      <p><strong>Currency:</strong> ${coinsEarned.join(", ") || "None"}</p>
      <p><strong>Valuables:</strong> ${gemOrArt}</p>
      <p><strong>Magic Item:</strong> ${magicItem}</p>
      ${proBonus}
    `;
  }

  // Pro Unlock Activation
  function activateProKey() {
    const key = licenseKeyInput.value.trim().toUpperCase();
    if (VALID_PRO_KEYS.includes(key)) {
      isProUnlocked = true;
      proStatusMsg.className = "status-msg success";
      proStatusMsg.textContent = "Pro Unlocked! Extended party sizes (up to 20), Pro Bonus Loot, & Ad-Free mode activated.";
      proPartyNote.classList.remove("hidden");
      if (headerProBadge) headerProBadge.classList.remove("hidden");
      partySizeInput.setAttribute("max", "20");
      if (adBanner) adBanner.style.display = "none";
      if (proModalBtn) {
        proModalBtn.textContent = "✨ Pro Active";
        proModalBtn.style.background = "#10b981";
      }
      setTimeout(() => proModal.classList.add("hidden"), 1500);

      // Refresh current encounter view to display Pro status
      if (currentEncounterMonsters.length > 0) {
        const xpBudget = getPartyXPBudget(parseInt(partySizeInput.value, 10) || 4, parseInt(partyLevelInput.value, 10) || 1, currentDifficulty);
        const actualXP = currentEncounterMonsters.reduce((sum, m) => sum + (m.monster.xp * m.count), 0);
        renderEncounter(xpBudget, actualXP);
      }
    } else {
      proStatusMsg.className = "status-msg error";
      proStatusMsg.textContent = "Invalid license key. Try 'DM-TOOLKIT-PRO-2025' or 'DM-HERO-PRO'.";
    }
  }

  // Event Listeners
  generateBtn.addEventListener("click", generateEncounter);
  regenerateBtn.addEventListener("click", generateEncounter);
  rollLootBtn.addEventListener("click", rollLoot);
  printBtn.addEventListener("click", () => window.print());

  saveEncounterBtn.addEventListener("click", saveCurrentEncounter);
  copyTextBtn.addEventListener("click", copyEncounterText);

  diceBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      rollSelectedDie(btn.getAttribute("data-dice"));
    });
  });

  clearDiceLogBtn.addEventListener("click", () => {
    diceLog.innerHTML = `<span class="placeholder-text">Click any die above to roll!</span>`;
  });

  tabConditionsBtn.addEventListener("click", () => {
    activeRefTab = "conditions";
    renderQuickReference();
  });

  tabHazardsBtn.addEventListener("click", () => {
    activeRefTab = "hazards";
    renderQuickReference();
  });

  proModalBtn.addEventListener("click", () => {
    proStatusMsg.textContent = "";
    proModal.classList.remove("hidden");
  });
  closeModalBtn.addEventListener("click", () => proModal.classList.add("hidden"));
  activateProBtn.addEventListener("click", activateProKey);

  // Initial Load Routines
  generateEncounter();
  renderSavedEncounters();
  renderQuickReference();
});
