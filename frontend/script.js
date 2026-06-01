// 1. EVENT LISTENER FOR HANDLING THE MATCH FORM SUBMISSION
document.getElementById("matchForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const resume = document.getElementById("resume").value;
  const job_description = document.getElementById("job_description").value;
  const resultDiv = document.getElementById("result");

  // Visual loading feedback state
  resultDiv.innerHTML = `<div class="result-card"><p>Analyzing match... Please wait.</p></div>`;

  try {
    const res = await fetch("/api/match", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        resume: resume,
        job_description: job_description
      })
    });

    if (!res.ok) {
      throw new Error(`Server error: ${res.status}`);
    }

    const data = await res.json();
    console.log("Match response:", data); // Important debug line

    // Render results dynamically
    resultDiv.innerHTML = `
      <div class="result-card">
        <h2>ATS Match Results</h2>

        <progress value="${Number(data.score || 0)}" max="100"></progress>

        <div class="score">
          Match Score: ${Number(data.score || 0).toFixed(1)}%
        </div>

        <h3>Matched Skills</h3>
        <p>${Array.isArray(data.matched) ? data.matched.join(", ") : (data.matched || "None identified")}</p>

        <h3>Missing Skills</h3>
        <p>${Array.isArray(data.missing) ? data.missing.join(", ") : (data.missing || "None identified")}</p>
      </div>
    `;

  } catch (error) {
    console.error("Error matching resume:", error);
    resultDiv.innerHTML = `
      <div class="result-card" style="border-left: 5px solid #ff4d4d;">
        <h2>Error</h2>
        <p>Failed to fetch match results. Please try again later.</p>
      </div>
    `;
  }
});

// 2. NAVIGATION HELPER: SHOW THE MATCH FORM
function runMatch() {
  // Ensure the main form layout is visible, and clear old history lists if present
  document.getElementById("matchForm").style.display = "flex";
  document.getElementById("result").innerHTML = "";
}

// 3. FETCH AND RENDER DB MATCH HISTORY LOGS
async function loadHistory() {
  const resultDiv = document.getElementById("result");
  
  // Hide the core input form visually to make space for our clean data table logs
  document.getElementById("matchForm").style.display = "none";
  resultDiv.innerHTML = `<h3>Loading Historical Match Records...</h3>`;

  try {
    const res = await fetch("/api/history");
    if (!res.ok) throw new Error("Failed to pull match logs from server.");

    const historyData = await res.json();
    console.log("History records received:", historyData);

    if (historyData.length === 0) {
      resultDiv.innerHTML = `
        <div class="result-card">
          <h2>Database Empty</h2>
          <p>No historical scans found. Run your first resume match scan above to populate logs!</p>
        </div>`;
      return;
    }

    // Build responsive HTML table template to house data loops cleanly
    let tableRows = historyData.map(record => {
      const formattedDate = new Date(record.timestamp).toLocaleString();
      return `
        <tr>
          <td>${formattedDate}</td>
          <td><strong>${record.score.toFixed(1)}%</strong></td>
          <td>${record.matched_skills}</td>
          <td>${record.missing_skills}</td>
        </tr>
      `;
    }).join("");

    resultDiv.innerHTML = `
      <div class="result-card" style="max-width: 100%; overflow-x: auto;">
        <h2>Saved Database Scans Log</h2>
        <table border="1" style="width: 100%; border-collapse: collapse; text-align: left; margin-top: 15px;">
          <thead>
            <tr style="background-color: #f2f2f2; color: #333;">
              <th style="padding: 10px;">Date & Time</th>
              <th style="padding: 10px;">Score</th>
              <th style="padding: 10px;">Matched Skills</th>
              <th style="padding: 10px;">Missing Skills</th>
            </tr>
          </thead>
          <tbody>
            ${tableRows}
          </tbody>
        </table>
      </div>
    `;

  } catch (error) {
    console.error("Error loading history logs:", error);
    resultDiv.innerHTML = `<p style="color: #ff4d4d;">Could not process database history logs.</p>`;
  }
}

// Placeholder for future optimization roadmap features
function runOptimize() {
  alert("AI Optimization feature module coming soon!");
}
