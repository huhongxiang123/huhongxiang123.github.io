(function (global) {
  "use strict";

  var data = global.PyPuzzleData || { puzzles: [], categories: [] };
  var storage = global.PyPuzzleStorage;
  var engine = global.PyPuzzleEngine;

  var puzzles = (data.puzzles || []).slice().sort(function (a, b) {
    return a.id - b.id;
  });

  var categories = [{ key: "all", label: "全部题目", description: "综合练习" }].concat(data.categories || []);
  var categoryMap = {};
  for (var i = 0; i < categories.length; i += 1) {
    categoryMap[categories[i].key] = categories[i];
  }

  var app = {
    state: storage ? storage.loadState() : {},
    selectedCategory: "all",
    currentPuzzle: null,
    initialOrder: [],
    workingOrder: [],
    pendingNextId: null,
    drag: {
      active: false,
      pointerId: null,
      startIndex: -1,
      currentIndex: -1,
      mismatchLookup: null
    }
  };

  var el = {};

  document.addEventListener("DOMContentLoaded", init);

  function init() {
    if (!storage || !engine || !puzzles.length) {
      document.body.innerHTML = "<main style='padding:24px;font-family:sans-serif;'>应用初始化失败，请检查脚本文件是否完整。</main>";
      return;
    }

    cacheElements();
    bindEvents();
    repairState();
    renderHome();
    showView("home");
  }

  function cacheElements() {
    el.viewHome = document.getElementById("view-home");
    el.viewPuzzle = document.getElementById("view-puzzle");
    el.viewResult = document.getElementById("view-result");
    el.viewStats = document.getElementById("view-stats");

    el.startBtn = document.getElementById("start-btn");
    el.continueBtn = document.getElementById("continue-btn");
    el.categoryGrid = document.getElementById("category-grid");
    el.selectedCategoryText = document.getElementById("selected-category-text");
    el.summaryCompleted = document.getElementById("summary-completed");
    el.summaryCategory = document.getElementById("summary-category");
    el.summaryStreak = document.getElementById("summary-streak");
    el.summaryBestStreak = document.getElementById("summary-best-streak");
    el.homeBanner = document.getElementById("home-banner");

    el.puzzleBackBtn = document.getElementById("puzzle-back-btn");
    el.puzzleStage = document.getElementById("puzzle-stage");
    el.puzzleTitle = document.getElementById("puzzle-title");
    el.puzzleDescription = document.getElementById("puzzle-description");
    el.codeList = document.getElementById("code-list");
    el.puzzleHint = document.getElementById("puzzle-hint");
    el.submitBtn = document.getElementById("submit-btn");
    el.resetBtn = document.getElementById("reset-btn");
    el.puzzleProgressText = document.getElementById("puzzle-progress-text");

    el.resultPanel = document.getElementById("result-panel");
    el.resultStatusTag = document.getElementById("result-status-tag");
    el.resultTitle = document.getElementById("result-title");
    el.resultSubtitle = document.getElementById("result-subtitle");
    el.resultCodeList = document.getElementById("result-code-list");
    el.resultExplanation = document.getElementById("result-explanation");
    el.resultExtra = document.getElementById("result-extra");
    el.nextBtn = document.getElementById("next-btn");
    el.retryBtn = document.getElementById("retry-btn");
    el.resultResetBtn = document.getElementById("result-reset-btn");
    el.homeBtn = document.getElementById("home-btn");

    el.statsGrid = document.getElementById("stats-grid");
    el.categoryProgressList = document.getElementById("category-progress-list");
    el.wrongList = document.getElementById("wrong-list");
    el.clearWrongBtn = document.getElementById("clear-wrong-btn");

    el.navButtons = Array.prototype.slice.call(document.querySelectorAll(".nav-btn"));
  }

  function bindEvents() {
    el.startBtn.addEventListener("click", function () {
      startPractice();
    });

    el.continueBtn.addEventListener("click", function () {
      continuePractice();
    });

    el.categoryGrid.addEventListener("click", onCategoryClick);

    el.puzzleBackBtn.addEventListener("click", function () {
      showView("home");
    });

    el.codeList.addEventListener("pointerdown", onDragStart);

    el.submitBtn.addEventListener("click", submitCurrentPuzzle);

    el.resetBtn.addEventListener("click", function () {
      resetCurrentOrder();
      setPuzzleHint("已恢复到本题初始打乱顺序。", "info");
    });

    el.nextBtn.addEventListener("click", goToNextPuzzle);

    el.retryBtn.addEventListener("click", function () {
      showView("puzzle");
      setPuzzleHint("继续拖拽调整后再提交。", "info");
      renderCodeList();
    });

    el.resultResetBtn.addEventListener("click", function () {
      resetCurrentOrder();
      showView("puzzle");
      setPuzzleHint("顺序已重置，重新拖拽试试。", "info");
    });

    el.homeBtn.addEventListener("click", function () {
      showView("home");
    });

    el.navButtons.forEach(function (button) {
      button.addEventListener("click", onBottomNavClick);
    });

    el.wrongList.addEventListener("click", onWrongItemClick);

    el.clearWrongBtn.addEventListener("click", function () {
      app.state.wrongPuzzleIds = [];
      persistState();
      renderStats();
      renderHome();
      setBanner("错题记录已清空。", "info");
    });
  }

  function repairState() {
    var puzzleIds = puzzles.map(function (item) {
      return item.id;
    });

    if (!categoryMap[app.state.currentCategory]) {
      app.state.currentCategory = "all";
    }

    if (puzzleIds.indexOf(app.state.currentPuzzleId) === -1) {
      app.state.currentPuzzleId = puzzles[0].id;
    }

    app.selectedCategory = app.state.currentCategory || "all";

    app.state.completedPuzzles = (app.state.completedPuzzles || []).filter(function (id) {
      return puzzleIds.indexOf(id) !== -1;
    });

    app.state.wrongPuzzleIds = (app.state.wrongPuzzleIds || []).filter(function (id) {
      return puzzleIds.indexOf(id) !== -1;
    });

    persistState();
  }

  function persistState() {
    app.state = storage.saveState(app.state);
  }

  function showView(name) {
    var viewMap = {
      home: el.viewHome,
      puzzle: el.viewPuzzle,
      result: el.viewResult,
      stats: el.viewStats
    };

    if (name !== "puzzle") {
      cancelDrag();
    }

    Object.keys(viewMap).forEach(function (key) {
      if (viewMap[key]) {
        viewMap[key].classList.toggle("is-active", key === name);
      }
    });

    if (name === "home") {
      renderHome();
      setActiveNav("home");
    } else if (name === "stats") {
      renderStats();
      setActiveNav("stats");
    } else {
      setActiveNav("practice");
    }

    if (typeof window.scrollTo === "function") {
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  }

  function setActiveNav(navName) {
    el.navButtons.forEach(function (button) {
      button.classList.toggle("is-active", button.getAttribute("data-nav") === navName);
    });
  }

  function onBottomNavClick(event) {
    var nav = event.currentTarget.getAttribute("data-nav");
    if (nav === "home") {
      showView("home");
      return;
    }
    if (nav === "stats") {
      showView("stats");
      return;
    }
    continuePractice();
  }

  function onCategoryClick(event) {
    var button = event.target.closest("button[data-category]");
    if (!button) {
      return;
    }

    applyCategory(button.getAttribute("data-category"), true);
    renderHome();
  }

  function applyCategory(categoryKey, showTip) {
    if (!categoryMap[categoryKey]) {
      categoryKey = "all";
    }
    app.selectedCategory = categoryKey;
    app.state.currentCategory = categoryKey;
    persistState();

    if (showTip) {
      setBanner("已切换到「" + categoryLabel(categoryKey) + "」。", "info");
    }
  }

  function getPuzzlesByCategory(categoryKey) {
    if (!categoryKey || categoryKey === "all") {
      return puzzles.slice();
    }
    return puzzles.filter(function (item) {
      return item.category === categoryKey;
    });
  }

  function getPuzzleById(puzzleId) {
    for (var i = 0; i < puzzles.length; i += 1) {
      if (puzzles[i].id === puzzleId) {
        return puzzles[i];
      }
    }
    return null;
  }

  function categoryLabel(categoryKey) {
    return categoryMap[categoryKey] ? categoryMap[categoryKey].label : "全部题目";
  }

  function startPractice() {
    var target = findStartPuzzleId(app.selectedCategory);
    if (!target) {
      setBanner("当前分类没有可练习题目。", "warn");
      return;
    }
    openPuzzle(target.id, true);
  }

  function continuePractice() {
    var targetId = app.state.currentPuzzleId;
    var list = getPuzzlesByCategory(app.selectedCategory);

    if (!list.length) {
      setBanner("当前分类暂无题目。", "warn");
      showView("home");
      return;
    }

    var found = list.some(function (item) {
      return item.id === targetId;
    });

    if (!found) {
      targetId = findStartPuzzleId(app.selectedCategory).id;
    }

    openPuzzle(targetId, false);
  }

  function findStartPuzzleId(categoryKey) {
    var list = getPuzzlesByCategory(categoryKey);
    if (!list.length) {
      return null;
    }

    var completed = toLookup(app.state.completedPuzzles);
    for (var i = 0; i < list.length; i += 1) {
      if (!completed[list[i].id]) {
        return list[i];
      }
    }

    return list[0];
  }

  function openPuzzle(puzzleId, forceShuffle) {
    cancelDrag();

    var puzzle = getPuzzleById(puzzleId);
    if (!puzzle) {
      setBanner("目标题目不存在。", "warn");
      showView("home");
      return;
    }

    var changedPuzzle = !app.currentPuzzle || app.currentPuzzle.id !== puzzle.id;
    app.currentPuzzle = puzzle;

    if (forceShuffle || changedPuzzle || app.workingOrder.length !== puzzle.correctOrder.length) {
      app.initialOrder = engine.shuffleLines(puzzle.correctOrder);
      app.workingOrder = app.initialOrder.slice();
    }

    app.state.currentPuzzleId = puzzle.id;
    app.state.currentCategory = app.selectedCategory;
    app.state.lastSessionAt = new Date().toISOString();
    persistState();

    renderPuzzle();
    showView("puzzle");
  }

  function renderHome() {
    renderCategoryGrid();

    el.selectedCategoryText.textContent = "当前: " + categoryLabel(app.selectedCategory);
    el.summaryCompleted.textContent = app.state.completedPuzzles.length + " / " + puzzles.length;
    el.summaryCategory.textContent = categoryLabel(app.selectedCategory);
    el.summaryStreak.textContent = app.state.streak + " 题";
    el.summaryBestStreak.textContent = app.state.bestStreak + " 题";

    var hasRecord = !!app.state.lastSessionAt;
    el.continueBtn.disabled = !hasRecord;
    el.continueBtn.textContent = hasRecord ? "继续上次练习" : "继续上次练习（暂无记录）";
  }

  function renderCategoryGrid() {
    var completed = toLookup(app.state.completedPuzzles);
    var html = categories
      .map(function (item) {
        var categoryPuzzles = getPuzzlesByCategory(item.key);
        var doneCount = categoryPuzzles.filter(function (puzzle) {
          return !!completed[puzzle.id];
        }).length;

        var activeClass = item.key === app.selectedCategory ? " is-active" : "";

        return (
          '<button type="button" class="category-card' +
          activeClass +
          '" data-category="' +
          escapeHtml(item.key) +
          '">' +
          "<strong>" +
          escapeHtml(item.label) +
          "</strong>" +
          "<p>" +
          escapeHtml(item.description || "") +
          "</p>" +
          "<small>已完成 " +
          doneCount +
          " / " +
          categoryPuzzles.length +
          "</small>" +
          "</button>"
        );
      })
      .join("");

    el.categoryGrid.innerHTML = html;
  }

  function renderPuzzle() {
    if (!app.currentPuzzle) {
      return;
    }

    var puzzle = app.currentPuzzle;
    var scope = getPuzzlesByCategory(app.selectedCategory);
    var index = scope.findIndex(function (item) {
      return item.id === puzzle.id;
    });

    if (index === -1) {
      scope = puzzles;
      index = scope.findIndex(function (item) {
        return item.id === puzzle.id;
      });
    }

    el.puzzleStage.textContent = categoryLabel(puzzle.category) + " · 第 " + (index + 1) + " 题";
    el.puzzleTitle.textContent = puzzle.title;
    el.puzzleDescription.textContent = puzzle.description;
    el.puzzleProgressText.textContent = "进度：" + (index + 1) + " / " + scope.length;

    setPuzzleHint("按住任意代码卡片拖动排序，完成后点击提交。", "info");
    renderCodeList();
  }

  function renderCodeList(mismatchLookup, draggingIndex) {
    if (!app.currentPuzzle) {
      return;
    }

    var html = app.workingOrder
      .map(function (line, index) {
        var wrongClass = mismatchLookup && mismatchLookup[index] ? " is-wrong" : "";
        var draggingClass = draggingIndex === index ? " is-dragging" : "";

        return (
          '<article class="code-card' +
          wrongClass +
          draggingClass +
          '" data-index="' +
          index +
          '">' +
          '<div class="code-row">' +
          '<span class="line-no">第 ' +
          (index + 1) +
          " 行</span>" +
          '<pre class="code-line">' +
          escapeHtml(line) +
          "</pre>" +
          "</div>" +
          "</article>"
        );
      })
      .join("");

    el.codeList.innerHTML = html;
  }

  function onDragStart(event) {
    if (!app.currentPuzzle) {
      return;
    }

    if (event.pointerType === "mouse" && event.button !== 0) {
      return;
    }

    var blockTarget = event.target.closest("button, a, input, textarea, select");
    if (blockTarget && !blockTarget.classList.contains("code-card")) {
      return;
    }

    var card = event.target.closest(".code-card[data-index]");
    if (!card) {
      return;
    }

    var startIndex = Number(card.getAttribute("data-index"));
    if (!isValidIndex(startIndex, app.workingOrder.length)) {
      return;
    }

    event.preventDefault();

    app.drag.active = true;
    app.drag.pointerId = typeof event.pointerId === "number" ? event.pointerId : null;
    app.drag.startIndex = startIndex;
    app.drag.currentIndex = startIndex;
    app.drag.mismatchLookup = null;

    document.body.classList.add("is-sorting");
    card.classList.add("is-dragging");

    if (card.setPointerCapture && app.drag.pointerId !== null) {
      try {
        card.setPointerCapture(app.drag.pointerId);
      } catch (error) {
        // 部分浏览器对 capture 支持不一致，忽略即可
      }
    }

    document.addEventListener("pointermove", onDragMove);
    document.addEventListener("pointerup", onDragEnd);
    document.addEventListener("pointercancel", onDragEnd);

    setPuzzleHint("拖动到目标位置后松开即可。", "info");
  }

  function onDragMove(event) {
    if (!app.drag.active) {
      return;
    }

    if (app.drag.pointerId !== null && typeof event.pointerId === "number" && event.pointerId !== app.drag.pointerId) {
      return;
    }

    event.preventDefault();

    var target = document.elementFromPoint(event.clientX, event.clientY);
    if (!target) {
      return;
    }

    var card = target.closest(".code-card[data-index]");
    if (!card || !el.codeList.contains(card)) {
      return;
    }

    var toIndex = Number(card.getAttribute("data-index"));
    if (!isValidIndex(toIndex, app.workingOrder.length)) {
      return;
    }

    if (toIndex === app.drag.currentIndex) {
      return;
    }

    app.workingOrder = moveItemInOrder(app.workingOrder, app.drag.currentIndex, toIndex);
    app.drag.currentIndex = toIndex;
    renderCodeList(null, app.drag.currentIndex);
  }

  function onDragEnd(event) {
    if (!app.drag.active) {
      return;
    }

    if (event && app.drag.pointerId !== null && typeof event.pointerId === "number" && event.pointerId !== app.drag.pointerId) {
      return;
    }

    cancelDrag();

    if (el.viewPuzzle.classList.contains("is-active")) {
      renderCodeList();
      setPuzzleHint("顺序已更新，可继续拖拽或直接提交。", "info");
    }
  }

  function cancelDrag() {
    if (!app.drag.active) {
      return;
    }

    document.removeEventListener("pointermove", onDragMove);
    document.removeEventListener("pointerup", onDragEnd);
    document.removeEventListener("pointercancel", onDragEnd);

    document.body.classList.remove("is-sorting");

    app.drag.active = false;
    app.drag.pointerId = null;
    app.drag.startIndex = -1;
    app.drag.currentIndex = -1;
    app.drag.mismatchLookup = null;
  }

  function submitCurrentPuzzle() {
    if (!app.currentPuzzle) {
      return;
    }

    cancelDrag();

    var result = engine.checkOrder(app.workingOrder, app.currentPuzzle.correctOrder);

    app.state.totalAttempts += 1;
    app.state.lastSessionAt = new Date().toISOString();

    if (result.isCorrect) {
      app.state.totalCorrect += 1;
      app.state.streak += 1;
      if (app.state.streak > app.state.bestStreak) {
        app.state.bestStreak = app.state.streak;
      }

      pushUnique(app.state.completedPuzzles, app.currentPuzzle.id);
      removeValue(app.state.wrongPuzzleIds, app.currentPuzzle.id);

      app.pendingNextId = findNextPuzzleId(app.currentPuzzle.id, app.selectedCategory);
      if (app.pendingNextId) {
        app.state.currentPuzzleId = app.pendingNextId;
      }
    } else {
      app.state.streak = 0;
      pushUnique(app.state.wrongPuzzleIds, app.currentPuzzle.id);
      app.pendingNextId = null;
      app.state.currentPuzzleId = app.currentPuzzle.id;
    }

    persistState();
    renderHome();
    renderResult(result);
  }

  function findNextPuzzleId(currentId, categoryKey) {
    var list = getPuzzlesByCategory(categoryKey);
    if (!list.length) {
      return null;
    }

    var index = list.findIndex(function (item) {
      return item.id === currentId;
    });

    if (index !== -1 && index < list.length - 1) {
      return list[index + 1].id;
    }

    var completed = toLookup(app.state.completedPuzzles);
    for (var i = 0; i < list.length; i += 1) {
      if (!completed[list[i].id]) {
        return list[i].id;
      }
    }

    return null;
  }

  function renderResult(result) {
    var isSuccess = result.isCorrect;

    el.resultPanel.classList.toggle("is-success", isSuccess);
    el.resultPanel.classList.toggle("is-fail", !isSuccess);

    el.resultExplanation.textContent = app.currentPuzzle.explanation;

    if (isSuccess) {
      el.resultStatusTag.textContent = "拼图成功";
      el.resultTitle.textContent = "拼图成功！";
      el.resultSubtitle.textContent = "顺序完全正确，你已经掌握了这道题的执行流程。";
      el.resultExtra.textContent = "当前连胜：" + app.state.streak + " 题，最高连胜：" + app.state.bestStreak + " 题";

      renderResultCodeList(app.currentPuzzle.correctOrder, null);

      el.nextBtn.hidden = false;
      el.nextBtn.disabled = !app.pendingNextId;
      el.nextBtn.textContent = app.pendingNextId ? "下一题" : "本分类已完成";
      el.retryBtn.hidden = true;
      el.resultResetBtn.hidden = true;
    } else {
      var wrongLines = result.mismatchIndexes.map(function (index) {
        return index + 1;
      });

      el.resultStatusTag.textContent = "继续加油";
      el.resultTitle.textContent = "顺序不正确";
      el.resultSubtitle.textContent = "第 " + wrongLines.join("、") + " 行位置有问题，调整后再试一次。";
      el.resultExtra.textContent = "连胜已重置，别担心，下一题继续追回来。";

      renderResultCodeList(app.workingOrder, toLookup(result.mismatchIndexes));

      el.nextBtn.hidden = true;
      el.retryBtn.hidden = false;
      el.resultResetBtn.hidden = false;
    }

    showView("result");
  }

  function renderResultCodeList(lines, mismatchLookup) {
    var html = lines
      .map(function (line, index) {
        var wrongClass = mismatchLookup && mismatchLookup[index] ? " is-wrong" : "";
        return '<div class="result-line' + wrongClass + '">' + escapeHtml(line) + "</div>";
      })
      .join("");

    el.resultCodeList.innerHTML = html;
  }

  function goToNextPuzzle() {
    if (!app.pendingNextId) {
      setBanner("当前分类已完成，可切换分类继续练习。", "info");
      showView("home");
      return;
    }

    openPuzzle(app.pendingNextId, true);
  }

  function resetCurrentOrder() {
    cancelDrag();
    app.workingOrder = app.initialOrder.slice();
    renderCodeList();
  }

  function setPuzzleHint(text, type) {
    el.puzzleHint.textContent = text;
    el.puzzleHint.classList.remove("warn");
    if (type === "warn") {
      el.puzzleHint.classList.add("warn");
    }
  }

  function renderStats() {
    var completedCount = app.state.completedPuzzles.length;
    var attempts = app.state.totalAttempts;
    var correct = app.state.totalCorrect;
    var accuracy = attempts ? Math.round((correct / attempts) * 100) : 0;

    var cards = [
      { label: "已完成题数", value: completedCount + " / " + puzzles.length },
      { label: "总提交次数", value: String(attempts) },
      { label: "累计答对", value: String(correct) },
      { label: "正确率", value: accuracy + "%" },
      { label: "当前连胜", value: app.state.streak + " 题" },
      { label: "最高连胜", value: app.state.bestStreak + " 题" }
    ];

    el.statsGrid.innerHTML = cards
      .map(function (item) {
        return '<article class="stat-card"><b>' + escapeHtml(item.value) + "</b><span>" + escapeHtml(item.label) + "</span></article>";
      })
      .join("");

    renderCategoryProgress();
    renderWrongList();
  }

  function renderCategoryProgress() {
    var completed = toLookup(app.state.completedPuzzles);

    var html = categories
      .filter(function (item) {
        return item.key !== "all";
      })
      .map(function (item) {
        var list = getPuzzlesByCategory(item.key);
        var done = list.filter(function (puzzle) {
          return !!completed[puzzle.id];
        }).length;

        var percent = list.length ? Math.round((done / list.length) * 100) : 0;

        return (
          '<article class="category-progress-item">' +
          '<div class="row"><span>' +
          escapeHtml(item.label) +
          "</span><b>" +
          done +
          " / " +
          list.length +
          "</b></div>" +
          '<div class="progress-bar"><span style="width:' +
          percent +
          '%"></span></div>' +
          "</article>"
        );
      })
      .join("");

    el.categoryProgressList.innerHTML = html;
  }

  function renderWrongList() {
    var wrongIds = (app.state.wrongPuzzleIds || []).slice().sort(function (a, b) {
      return a - b;
    });

    if (!wrongIds.length) {
      el.wrongList.innerHTML = '<p class="empty">暂无错题，继续保持。</p>';
      el.clearWrongBtn.disabled = true;
      return;
    }

    el.clearWrongBtn.disabled = false;

    var html = wrongIds
      .map(function (id) {
        var puzzle = getPuzzleById(id);
        if (!puzzle) {
          return "";
        }

        return (
          '<button type="button" class="wrong-item" data-puzzle-id="' +
          id +
          '">' +
          "<strong>#" +
          id +
          " " +
          escapeHtml(puzzle.title) +
          "</strong>" +
          "<span>" +
          escapeHtml(categoryLabel(puzzle.category)) +
          " · 点击重新练习</span>" +
          "</button>"
        );
      })
      .join("");

    el.wrongList.innerHTML = html;
  }

  function onWrongItemClick(event) {
    var button = event.target.closest("button[data-puzzle-id]");
    if (!button) {
      return;
    }

    var puzzleId = Number(button.getAttribute("data-puzzle-id"));
    var puzzle = getPuzzleById(puzzleId);
    if (!puzzle) {
      return;
    }

    applyCategory(puzzle.category, false);
    openPuzzle(puzzle.id, true);
  }

  function setBanner(text, type) {
    el.homeBanner.textContent = text;
    el.homeBanner.className = "banner " + (type || "info");
    el.homeBanner.hidden = false;
  }

  function moveItemInOrder(order, fromIndex, toIndex) {
    if (engine && typeof engine.moveItem === "function") {
      return engine.moveItem(order, fromIndex, toIndex);
    }

    var next = order.slice();
    if (!isValidIndex(fromIndex, next.length) || !isValidIndex(toIndex, next.length) || fromIndex === toIndex) {
      return next;
    }

    var moved = next.splice(fromIndex, 1)[0];
    next.splice(toIndex, 0, moved);
    return next;
  }

  function isValidIndex(index, length) {
    return Number.isInteger(index) && index >= 0 && index < length;
  }

  function toLookup(list) {
    var output = {};
    if (!Array.isArray(list)) {
      return output;
    }
    for (var i = 0; i < list.length; i += 1) {
      output[list[i]] = true;
    }
    return output;
  }

  function pushUnique(list, value) {
    if (!Array.isArray(list)) {
      return;
    }
    if (list.indexOf(value) === -1) {
      list.push(value);
    }
  }

  function removeValue(list, value) {
    if (!Array.isArray(list)) {
      return;
    }
    var index = list.indexOf(value);
    if (index !== -1) {
      list.splice(index, 1);
    }
  }

  function escapeHtml(text) {
    return String(text)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/\"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }
})(window);
