const typingText = document.querySelector(".typing-text");
const inputText = document.querySelector(".overlay-input");
const timer = document.querySelector(".timer");

let wlRadios = document.getElementsByName("wl");
let difficultyRadios = document.getElementsByName("diff");
let timeRadios = document.getElementsByName("time");
let input = "";

let scrollAmount = 0;
const lineHeight = parseInt(getComputedStyle(typingText).lineHeight, 10);
let wordList = "";

let started = false;
let time = 0;
let timerVar = null;
let errors = 0;

function selectNStrings(stringsArray, n) {
  if (!Array.isArray(stringsArray)) {
    throw new Error('Input must be an array of strings');
  }
  if (n <= 0 || n > stringsArray.length) {
    throw new Error('Invalid value of n');
  }
  const selectedStrings = [];
  const shuffledArray = stringsArray.slice().sort(() => Math.random() - 0.5);
  for (let i = 0; i < n; i++) {
    selectedStrings.push(shuffledArray[i]);
  }
  return selectedStrings;
}

function getRadioValue(radios) {
  for (var i = 0; i < radios.length; i++) {
    if (radios[i].checked) {
      return radios[i].value;
    }
  }
  return "";
}

function addEvents(radios) {
  for(let radio of radios) {
    radio.addEventListener("change", shuffleWords);
  }
}

async function fetchFile(file) {
  return fetch(`/static/dict/${file}.txt`)
  .then(response => {
    if (response.ok) {
      return response.text();
    } else {
      throw new Error('Failed to fetch file');
    }
  })
  .then(data => {
    return data;
  })
  .catch(error => {
    console.error(error);
    return "";
  });
}

async function shuffleWords() {
  let diff = getRadioValue(difficultyRadios);
  let wl = getRadioValue(wlRadios);
  input = "";
  inputText.value = "";
  started = false;
  clearInterval(timerVar);
  timer.innerHTML = "";
  errors = 0;
  switch(diff) {
    case "easy":
      var limit = 200;
      break;
    case "normal":
      var limit = 1000;
      break;
    case "hard":
      var limit = 5000;
      break;
    case "harder":
      var limit = 10000;
      break;
    default:
      var limit = 10;
      break;
  }
  words = (await fetchFile(wl)).split("\n").slice(0,limit);
  selected_words = selectNStrings(words,100);
  typingText.innerHTML = selected_words.join(" ");
}

async function regenWords() {
  let diff = getRadioValue(difficultyRadios);
  let wl = getRadioValue(wlRadios);
  switch(diff) {
    case "easy":
      var limit = 200;
      break;
    case "normal":
      var limit = 1000;
      break;
    case "hard":
      var limit = 5000;
      break;
    case "harder":
      var limit = 10000;
      break;
    default:
      var limit = 10;
      break;
  }
  words = (await fetchFile(wl)).split("\n").slice(0,limit);
  selected_words = selectNStrings(words,100);
  typingText.innerHTML = selected_words.join(" ");
}

function advanceText() {
  scrollAmount += lineHeight;
  typingText.style.transform = "translateY(-" + scrollAmount + "px)";
}

function tick() {
  time -= 0.1;
  if(time <= 0) {
    clearInterval(timerVar);
    endTest();
  }
  timer.textContent = time.toFixed(1);
}

function startTest() {
  timeLimit = Number(getRadioValue(timeRadios));
  started = true;
  time = timeLimit;
  timer.textContent = time.toFixed(1);
  timerVar = setInterval(tick,100);
}

function endTest() {
  let score = 0;
  input += inputText.value;
  switch(getRadioValue(difficultyRadios)) {
    case "easy":
      var diff = 1;
      break;
    case "normal":
      var diff = 2;
      break;
    case "hard":
      var diff = 2.5;
      break;
    case "harder":
      var diff = 3;
      break;
  }
  const data = {
    words: input.split(' ').length,
    chars: input.length,
    kpm: input.length/(timeLimit/60),
    errors: errors,
    time: timeLimit,
    difficulty: getRadioValue(difficultyRadios),
    wpm: (input.length/5) / (timeLimit/60),
    accuracy: (1 - (errors/input.length))*100,
  };
  let awl = input.split(' ').reduce((sum, n) => sum + n.length , 0) / data.words;
  data.raw = (input.length/awl) / (timeLimit/60),
  score += data.wpm * 0.2;
  score += data.kpm * 0.1;
  score *= (data.time/60) * 0.15 + 1;
  score *= diff * 0.1 + 1;
  score *= data.accuracy/100;
  score *= awl * 0.15 + 1;
  data.score = score;
  data.awl = awl;
  const options = {
    method: "POST",
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  };
  fetch("/api/submit", options)
    .then(res => {
      if(res.status == 200) {
        res.json().then(data => {
          window.location = `/results/${data.id}`;
        })
      } else {
        console.error(`Error submitting test: ${res}`)
      }
    })
    .catch(err => {
      console.error(`Error: ${err}`)
    });
}

inputText.addEventListener("input", () => {
  if(!started) startTest();
  const typedText = inputText.value;
  const expectedText = typingText.textContent;
  for (let i = 0; i < typedText.length; i++) {
    if(expectedText[i] != typedText[i]) {
      errors++;
      inputText.setRangeText(expectedText[i], i, i + 1, "end");
      inputText.setSelectionRange(i, i + 1);
      inputText.classList.add("incorrect");
    } else {
      inputText.classList.remove("incorrect");
    }
  }
});

inputText.addEventListener("cut", function (e) {
  e.preventDefault();
});

inputText.addEventListener("copy", function (e) {
  e.preventDefault();
});

inputText.addEventListener("paste", function (e) {
  e.preventDefault();
});

inputText.onselectstart = function() {
  return false;
};
inputText.addEventListener("scroll", () => {
  input += inputText.value;
  inputText.value = "";
  regenWords();
});

addEvents(wlRadios);
addEvents(difficultyRadios);
addEvents(timeRadios);
shuffleWords();

