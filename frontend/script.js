const ticketText = document.querySelector("#ticketText");
const classifyBtn = document.querySelector("#classifyBtn");
const sampleBtn = document.querySelector("#sampleBtn");
const categoryEl = document.querySelector("#category");
const priorityEl = document.querySelector("#priority");
const confidenceList = document.querySelector("#confidenceList");
const statusEl = document.querySelector("#status");

const samples = [
  "My payment failed twice but the amount was deducted from my bank account.",
  "I received a suspicious login alert from another country.",
  "The exported CSV file has missing columns and incorrect totals.",
  "Can I change the delivery address before the package ships?"
];

function setStatus(message, isError = false) {
  statusEl.textContent = message;
  statusEl.classList.toggle("error", isError);
}

function renderConfidence(confidence) {
  confidenceList.innerHTML = "";
  Object.entries(confidence || {}).forEach(([label, score]) => {
    const row = document.createElement("div");
    row.className = "confidence-row";
    row.innerHTML = `
      <div class="confidence-label">
        <span>${label}</span>
        <span>${Math.round(score * 100)}%</span>
      </div>
      <div class="bar"><span style="width: ${Math.round(score * 100)}%"></span></div>
    `;
    confidenceList.appendChild(row);
  });
}

async function classifyTicket() {
  const text = ticketText.value.trim();
  if (!text) {
    setStatus("Please enter a ticket message first.", true);
    return;
  }

  classifyBtn.disabled = true;
  setStatus("Classifying ticket...");

  try {
    const response = await fetch("/api/classify", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ticket_text: text })
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || "Classification failed.");
    }

    categoryEl.textContent = data.category;
    priorityEl.textContent = data.priority;
    renderConfidence(data.category_confidence);
    setStatus("Ticket classified successfully.");
  } catch (error) {
    setStatus(error.message, true);
  } finally {
    classifyBtn.disabled = false;
  }
}

classifyBtn.addEventListener("click", classifyTicket);
sampleBtn.addEventListener("click", () => {
  const next = samples[Math.floor(Math.random() * samples.length)];
  ticketText.value = next;
  setStatus("Sample ticket loaded.");
});

