const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");
canvas.width = 400;
canvas.height = 600;

// ===== FIREBASE (ISI SENDIRI) =====
const firebaseConfig = {
  apiKey: "API_KEY_KAMU",
  authDomain: "PROJECT.firebaseapp.com",
  databaseURL: "https://PROJECT.firebaseio.com",
  projectId: "PROJECT"
};
firebase.initializeApp(firebaseConfig);
const db = firebase.database();

// ===== AUDIO =====
const bgm = document.getElementById("bgm");
let musicStarted = false;
bgm.addEventListener("ended", () => {
  bgm.currentTime = 0;
  bgm.play();
});

// ===== UI =====
const scoreEl = document.getElementById("score");
const highScoreEl = document.getElementById("highScore");
const gameOverEl = document.getElementById("gameOver");
const finalScoreEl = document.getElementById("finalScore");

// ===== PLAYER =====
const player = {
  x: 200,
  y: 500,
  radius: 15,
  vx: 0,
  vy: 0,
  speed: 0.12,
  jump: -11
};

let gravity = 0.45;
let mouseX = canvas.width / 2;
let score = 0;
let gameOver = false;
let difficulty = "easy";
let scoreMultiplier = 1;

// ===== PLATFORM =====
let platforms = [];
let platformCount = 8;
let platformGap = 90;

function createPlatform(y) {
  return {
    x: Math.random() * 260 + 20,
    y,
    width: 100,
    height: 15
  };
}

function createPlatforms() {
  platforms = [];
  let y = 550;
  for (let i = 0; i < platformCount; i++) {
    platforms.push(createPlatform(y));
    y -= platformGap;
  }
}

// ===== MODE =====
function setMode(mode) {
  difficulty = mode;

  if (mode === "easy") {
    gravity = 0.4;
    player.jump = -11;
    platformGap = 95;
    platformCount = 9;
    scoreMultiplier = 1;
  }

  if (mode === "hard") {
    gravity = 0.65;
    player.jump = -9;
    platformGap = 130;
    platformCount = 6;
    scoreMultiplier = 2;
  }

  document.getElementById("modeSelect").style.display = "none";
  restartGame();
}

function showMode() {
  gameOverEl.style.display = "none";
  document.getElementById("modeSelect").style.display = "flex";
}

// ===== LEADERBOARD LOCAL =====
let leaderboard = JSON.parse(localStorage.getItem("leaderboard")) || [];
let highScore = localStorage.getItem("highScore") || 0;
highScoreEl.textContent = "High Score: " + highScore;

function renderLeaderboard() {
  const list = document.getElementById("leaderboard");
  list.innerHTML = "";
  leaderboard.forEach(p => {
    const li = document.createElement("li");
    li.textContent = `${p.name} - ${p.score}`;
    list.appendChild(li);
  });
}
renderLeaderboard();

// ===== ONLINE LEADERBOARD =====
db.ref("leaderboard")
  .orderByChild("score")
  .limitToLast(5)
  .on("value", snap => {
    const list = document.getElementById("onlineLeaderboard");
    list.innerHTML = "";
    const data = [];
    snap.forEach(s => data.push(s.val()));
    data.reverse();
    data.forEach(p => {
      const li = document.createElement("li");
      li.textContent = `${p.name} - ${p.score}`;
      list.appendChild(li);
    });
  });

// ===== CONTROL =====
canvas.addEventListener("mousemove", e => {
  const rect = canvas.getBoundingClientRect();
  mouseX = e.clientX - rect.left;

  if (!musicStarted) {
    bgm.volume = 0.4;
    bgm.play().catch(()=>{});
    musicStarted = true;
  }
});

// ===== UPDATE =====
function update() {
  if (gameOver) return;

  player.vx = (mouseX - player.x) * player.speed;
  player.vy += gravity;
  player.x += player.vx;
  player.y += player.vy;

  if (player.x < player.radius) player.x = player.radius;
  if (player.x > canvas.width - player.radius)
    player.x = canvas.width - player.radius;

  platforms.forEach(p => {
    if (
      player.vy > 0 &&
      player.x + player.radius > p.x &&
      player.x - player.radius < p.x + p.width &&
      player.y + player.radius >= p.y &&
      player.y + player.radius <= p.y + p.height + 10
    ) {
      player.y = p.y - player.radius;
      player.vy = player.jump;
    }
  });

  if (player.y < canvas.height / 2) {
    const diff = canvas.height / 2 - player.y;
    player.y = canvas.height / 2;
    platforms.forEach(p => p.y += diff);
    score += Math.floor(diff * scoreMultiplier);
    scoreEl.textContent = "Skor: " + score;
  }

  platforms = platforms.filter(p => p.y < canvas.height + 50);
  while (platforms.length < platformCount) {
    const top = Math.min(...platforms.map(p => p.y));
    platforms.push(createPlatform(top - platformGap));
  }

  if (player.y - player.radius > canvas.height) endGame();
}

// ===== DRAW =====
function draw() {
  ctx.clearRect(0,0,canvas.width,canvas.height);

  ctx.fillStyle = "#ff4757";
  ctx.beginPath();
  ctx.arc(player.x, player.y, player.radius, 0, Math.PI * 2);
  ctx.fill();

  ctx.fillStyle = "#2ed573";
  platforms.forEach(p => ctx.fillRect(p.x, p.y, p.width, p.height));
}

// ===== GAME STATE =====
function endGame() {
  gameOver = true;
  bgm.pause();
  finalScoreEl.textContent = `Skor: ${score} (${difficulty.toUpperCase()})`;
  gameOverEl.style.display = "block";
}

function saveScore() {
  const name = document.getElementById("playerName").value || "Player";
  leaderboard.push({ name, score });
  leaderboard.sort((a,b)=>b.score-a.score);
  leaderboard = leaderboard.slice(0,5);
  localStorage.setItem("leaderboard", JSON.stringify(leaderboard));
  renderLeaderboard();

  if (score > highScore) {
    highScore = score;
    localStorage.setItem("highScore", highScore);
    highScoreEl.textContent = "High Score: " + highScore;
  }

  db.ref("leaderboard").push({ name, score });
  document.getElementById("playerName").value = "";
}

function restartGame() {
  score = 0;
  gameOver = false;
  player.x = 200;
  player.y = 500;
  player.vy = 0;
  createPlatforms();
  scoreEl.textContent = "Skor: 0";
  bgm.currentTime = 0;
  bgm.play();
}

// ===== LOOP =====
function loop() {
  update();
  draw();
  requestAnimationFrame(loop);
}
loop();
