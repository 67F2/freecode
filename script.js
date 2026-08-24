const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

const AGENT_COUNT = document.querySelectorAll(".card-grid .card").length;
const agentCountEl = document.getElementById("agent-count");
if (agentCountEl) agentCountEl.textContent = AGENT_COUNT;

const phrases = [
  "AI agents that cost $0. Unlike your therapist.",
  `${AGENT_COUNT} interns who never sleep and haven't asked for equity. Yet.`,
  "Free as in beer and free as in speech, sometimes.",
  "Your code, written by something that never sighs at you.",
  "Now with 100% more free. Terms apply. There are no terms.",
  "Cheaper than your coffee habit. Worse at small talk. Same hours.",
  "It reads the error messages you've been pretending not to see.",
  "Zero dollars. Zero judgment. Mild sass.",
  "Side effects may include shipping on weekends.",
  "Funded by free AI coding, Aussie electricity and one very patient support button.",
  "Open source tools and the warm fuzzy feeling of creating something.",
  "Imposter syndrome still costs extra. Nothing's perfect.",
  "git commit -m 'the agents did it'",
  "This line loops forever. Like your debugging."
];

const typedEl = document.getElementById("typed");

if (prefersReducedMotion) {
  typedEl.textContent = phrases[0];
} else {
  let phraseIndex = 0;
  let charIndex = 0;
  let deleting = false;

  function typeLoop() {
    const current = phrases[phraseIndex];
    if (!deleting) {
      charIndex++;
      typedEl.textContent = current.slice(0, charIndex);
      if (charIndex === current.length) {
        deleting = true;
        setTimeout(typeLoop, 2400);
        return;
      }
      setTimeout(typeLoop, 45 + Math.random() * 45);
    } else {
      charIndex--;
      typedEl.textContent = current.slice(0, charIndex);
      if (charIndex === 0) {
        deleting = false;
        phraseIndex = (phraseIndex + 1) % phrases.length;
      }
      setTimeout(typeLoop, deleting ? 18 : 300);
    }
  }
  typeLoop();
}

document.querySelectorAll(".copy-btn").forEach((btn) => {
  btn.addEventListener("click", async () => {
    const text = btn.parentElement.querySelector("code").textContent.trim();
    try {
      await navigator.clipboard.writeText(text);
    } catch {
      const ta = document.createElement("textarea");
      ta.value = text;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand("copy");
      ta.remove();
    }
    const original = btn.textContent;
    btn.textContent = "copied!";
    btn.classList.add("copied");
    setTimeout(() => {
      btn.textContent = original;
      btn.classList.remove("copied");
    }, 1500);
  });
});

const results = {
  gemini: {
    name: "Antigravity",
    persona: "The Trust-Fund Kid",
    blurb: "Google pays its rent, so yours stays intact. A genuinely generous free tier plus a 1M-token context window — it remembers your whole repo and your 3am commit messages. Terminal CLI or VS Code extension.",
    anchor: "#gemini"
  },
  aider: {
    name: "Aider",
    persona: "The Git Purist",
    blurb: "Every edit becomes a commit. When prod breaks, git blame points at the AI — accountability, finally. Terminal-native, open source, any model via your API key.",
    anchor: "#aider"
  },
  cline: {
    name: "Cline",
    persona: "The IDE Squatter",
    blurb: "Lives in your VS Code rent-free, editing across files with your approval at every step. Runs fully local with Ollama if you're the paranoid type.",
    anchor: "#cline"
  },
  opencode: {
    name: "OpenCode",
    persona: "The Model Polygamist",
    blurb: "Works with any model — Claude, GPT, Gemini, or local Ollama — plus its own Zen gateway serving free hosted models. Yes, one is called Big Pickle.",
    anchor: "#opencode"
  },
  codex: {
    name: "OpenAI Codex CLI",
    persona: "The Sandbox Kid",
    blurb: "Plays strictly inside its sandbox and can't rm -rf your life without asking. Free tier to start; paid plans once you're emotionally attached.",
    anchor: "#codex"
  },
  copilot: {
    name: "GitHub Copilot Free",
    persona: "The Gateway Drug",
    blurb: "2,000 completions and 50 chats per month, free forever — running out exactly when you hit flow state. Easiest setup of the bunch.",
    anchor: "#copilot"
  },
  freebuff: {
    name: "Freebuff",
    persona: "The One With Commercials",
    blurb: "No subscription, no API key, no credit card — tiny text ads pay for your inference instead. You're not the product; you're the audience.",
    anchor: "#freebuff"
  }
};

const quizForm = document.getElementById("quiz-form");
const quizError = document.getElementById("quiz-error");
const quizResult = document.getElementById("quiz-result");

quizForm.addEventListener("submit", (e) => {
  e.preventDefault();
  const answered = ["q1", "q2", "q3"].every(
    (name) => quizForm.querySelector(`input[name="${name}"]:checked`)
  );
  if (!answered) {
    quizError.hidden = false;
    quizError.classList.remove("shake");
    void quizError.offsetWidth;
    quizError.classList.add("shake");
    return;
  }
  quizError.hidden = true;

  const scores = { gemini: 0, aider: 0, cline: 0, opencode: 0, codex: 0, copilot: 0, freebuff: 0 };
  quizForm.querySelectorAll('input[type="radio"]:checked').forEach((input) => {
    input.value.split(",").forEach((pair) => {
      const [agent, points] = pair.split(":");
      scores[agent] += Number(points);
    });
  });

  const priority = ["gemini", "aider", "cline", "codex", "opencode", "copilot", "freebuff"];
  const winner = priority.reduce((best, key) =>
    scores[key] > scores[best] ? key : best
  , priority[0]);
  const r = results[winner];

  quizResult.innerHTML = `
    <h3># diagnosis complete → ${r.name}</h3>
    <p class="result-persona">${r.persona}</p>
    <p>${r.blurb}</p>
    <a href="${r.anchor}">scroll to their card ↑</a>
  `;
  quizResult.hidden = false;
  quizResult.scrollIntoView({ behavior: prefersReducedMotion ? "auto" : "smooth", block: "nearest" });
});

document.querySelectorAll(".faq-item button").forEach((btn) => {
  btn.addEventListener("click", () => {
    const item = btn.closest(".faq-item");
    const open = item.classList.toggle("open");
    btn.setAttribute("aria-expanded", String(open));
  });
});

console.log(
  "%c>_ free_ai_agents %c nice devtools. while you're here: all six of these cost $0. your move.",
  "color:#00ff66;font-weight:bold;font-family:monospace;font-size:14px;",
  "color:#7dffa8;font-family:monospace;"
);
