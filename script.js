"use strict";

/* ===== Общий список отмазок =====
   Один список без категорий. */
const EXCUSES = [
  "Я в лесу",
  "Мне гулять с собакой",
  "Завтра рано вставать, поэтому сегодня нельзя веселиться",
  "Рубрика рандомный слив",
  "Послезавтра надо работать, вдруг опоздаю",
  "Нечего надеть",
  "Рубрика молчаливый слив",
  "Кот в мешке - сгенерируй сам",
  "Нужно немного насилия",
  "Татарские посиделки",
];

/* Легендарная отмазка — выпадает примерно в 5% случаев */
const LEGENDARY_EXCUSE =
  "Я не пришёл, потому что в этот момент спасал котёнка, доставлял пиццу бабушке и одновременно изобретал лекарство от понедельников.";

/* ===== Ссылки на элементы страницы ===== */
const card = document.getElementById("card");
const excuseEl = document.getElementById("excuse");
const generateBtn = document.getElementById("generateBtn");
const copyBtn = document.getElementById("copyBtn");
const toast = document.getElementById("toast");

/* Возвращает случайный элемент массива */
function pickRandom(list) {
  return list[Math.floor(Math.random() * list.length)];
}

/* Показывает короткое уведомление */
function showToast(message) {
  toast.textContent = message;
  setTimeout(() => {
    toast.textContent = "";
  }, 2000);
}

/* Генерация и показ отмазки */
function generateExcuse() {
  const isLegendary = Math.random() < 0.05; // 5% шанс на легендарную отмазку

  let text;
  if (isLegendary) {
    text = LEGENDARY_EXCUSE;
    card.classList.add("legendary");
    excuseEl.classList.add("legendary");
    // Бейдж с пометкой о редкой отмазке
    excuseEl.innerHTML =
      '<span class="legendary-badge">★ Легендарная отмазка ★</span>' + text;
  } else {
    text = pickRandom(EXCUSES);
    card.classList.remove("legendary");
    excuseEl.classList.remove("legendary");
    excuseEl.textContent = text;
  }

  // Перезапуск анимации появления
  excuseEl.classList.remove("fade-in");
  void excuseEl.offsetWidth; // принудительный reflow для рестарта анимации
  excuseEl.classList.add("fade-in");
}

/* Копирование текущей отмазки в буфер обмена */
function copyExcuse() {
  const text = excuseEl.textContent.replace("★ Легендарная отмазка ★", "").trim();

  if (!text || text === "Здесь появится твоя отмазка...") {
    showToast("Сначала сгенерируй отмазку!");
    return;
  }

  navigator.clipboard
    .writeText(text)
    .then(() => showToast("Отмазка скопирована! ✅"))
    .catch(() => showToast("Не удалось скопировать 😕"));
}

/* ===== Обработчики событий ===== */
generateBtn.addEventListener("click", generateExcuse);
copyBtn.addEventListener("click", copyExcuse);
