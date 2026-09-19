(function (global) {
  "use strict";

  var STORAGE_KEY = "pypuzzle-lite-state-v1";
  var memoryFallback = null;

  function defaultState() {
    return {
      version: 1,
      currentPuzzleId: 1,
      completedPuzzles: [],
      currentCategory: "all",
      streak: 0,
      bestStreak: 0,
      wrongPuzzleIds: [],
      totalAttempts: 0,
      totalCorrect: 0,
      lastSessionAt: null
    };
  }

  function toInt(value, fallback) {
    var n = Number(value);
    if (!Number.isFinite(n) || n < 0) {
      return fallback;
    }
    return Math.floor(n);
  }

  function toUniqueNumberArray(value) {
    if (!Array.isArray(value)) {
      return [];
    }
    var seen = {};
    var out = [];
    for (var i = 0; i < value.length; i += 1) {
      var n = Number(value[i]);
      if (Number.isFinite(n) && n > 0) {
        n = Math.floor(n);
        if (!seen[n]) {
          seen[n] = true;
          out.push(n);
        }
      }
    }
    return out;
  }

  function sanitizeState(raw) {
    var base = defaultState();
    if (!raw || typeof raw !== "object") {
      return base;
    }

    base.currentPuzzleId = toInt(raw.currentPuzzleId, 1);
    base.completedPuzzles = toUniqueNumberArray(raw.completedPuzzles);
    base.currentCategory = typeof raw.currentCategory === "string" ? raw.currentCategory : "all";
    base.streak = toInt(raw.streak, 0);
    base.bestStreak = toInt(raw.bestStreak, 0);
    base.wrongPuzzleIds = toUniqueNumberArray(raw.wrongPuzzleIds);
    base.totalAttempts = toInt(raw.totalAttempts, 0);
    base.totalCorrect = toInt(raw.totalCorrect, 0);
    base.lastSessionAt = typeof raw.lastSessionAt === "string" ? raw.lastSessionAt : null;

    if (base.bestStreak < base.streak) {
      base.bestStreak = base.streak;
    }

    return base;
  }

  function parseStored(rawText) {
    if (!rawText) {
      return null;
    }
    try {
      return JSON.parse(rawText);
    } catch (error) {
      return null;
    }
  }

  function loadState() {
    var raw = null;
    try {
      raw = global.localStorage.getItem(STORAGE_KEY);
    } catch (error) {
      raw = memoryFallback;
    }

    if (!raw) {
      return defaultState();
    }

    return sanitizeState(parseStored(raw));
  }

  function saveState(nextState) {
    var safe = sanitizeState(nextState);
    var text = JSON.stringify(safe);
    try {
      global.localStorage.setItem(STORAGE_KEY, text);
    } catch (error) {
      memoryFallback = text;
    }
    return safe;
  }

  function clearState() {
    try {
      global.localStorage.removeItem(STORAGE_KEY);
    } catch (error) {
      memoryFallback = null;
    }
  }

  global.PyPuzzleStorage = {
    key: STORAGE_KEY,
    defaultState: defaultState,
    loadState: loadState,
    saveState: saveState,
    clearState: clearState
  };
})(window);
