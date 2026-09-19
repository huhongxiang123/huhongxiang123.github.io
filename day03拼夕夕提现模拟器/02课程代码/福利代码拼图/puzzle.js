(function (global) {
  "use strict";

  function areSameOrder(a, b) {
    if (!Array.isArray(a) || !Array.isArray(b) || a.length !== b.length) {
      return false;
    }
    for (var i = 0; i < a.length; i += 1) {
      if (a[i] !== b[i]) {
        return false;
      }
    }
    return true;
  }

  function fisherYates(items) {
    for (var i = items.length - 1; i > 0; i -= 1) {
      var j = Math.floor(Math.random() * (i + 1));
      var temp = items[i];
      items[i] = items[j];
      items[j] = temp;
    }
  }

  function shuffleLines(lines) {
    var base = Array.isArray(lines) ? lines.slice() : [];
    if (base.length < 2) {
      return base;
    }

    var shuffled = base.slice();
    var attempts = 0;
    while (areSameOrder(base, shuffled) && attempts < 8) {
      fisherYates(shuffled);
      attempts += 1;
    }

    return shuffled;
  }

  function moveItem(order, fromIndex, toIndex) {
    if (!Array.isArray(order)) {
      return [];
    }

    var next = order.slice();
    if (
      fromIndex < 0 ||
      fromIndex >= next.length ||
      toIndex < 0 ||
      toIndex >= next.length ||
      fromIndex === toIndex
    ) {
      return next;
    }

    var moved = next.splice(fromIndex, 1)[0];
    next.splice(toIndex, 0, moved);

    return next;
  }

  function moveLine(order, index, direction) {
    var target = direction === "up" ? index - 1 : index + 1;
    return moveItem(order, index, target);
  }

  function checkOrder(currentOrder, correctOrder) {
    var mismatchIndexes = [];
    var maxLength = Math.max(currentOrder.length, correctOrder.length);

    for (var i = 0; i < maxLength; i += 1) {
      if (currentOrder[i] !== correctOrder[i]) {
        mismatchIndexes.push(i);
      }
    }

    return {
      isCorrect: mismatchIndexes.length === 0,
      mismatchIndexes: mismatchIndexes
    };
  }

  global.PyPuzzleEngine = {
    shuffleLines: shuffleLines,
    moveItem: moveItem,
    moveLine: moveLine,
    checkOrder: checkOrder,
    areSameOrder: areSameOrder
  };
})(window);
