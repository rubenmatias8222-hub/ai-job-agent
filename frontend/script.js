document.getElementById("matchForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const resume = document.getElementById("resume").value;
  const job_description = document.getElementById("job_description").value;
  const resultDiv = document.getElementById("result");

  // Show a loading state to the user
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

    console.log(data); // IMPORTANT DEBUG LINE

    // Safely render the results
    resultDiv.innerHTML = `
      <div class="result-card">
        <h2>ATS Match Results</h2>

        <progress value="${Number(data.score || 0)}" max="100"></progress>

        <div class="score">
          Match Score: ${Number(data.score || 0).toFixed(1)}%
        </div>

        <h3>Matched Skills</h3>
        <p>${Array.isArray(data.matched) 
          ? data.matched.join(", ") 
          : (data.matched || "None identified")}</p>

        <h3>Missing Skills</h3>
        <p>${Array.isArray(data.missing) 
          ? data.missing.join(", ") 
          : (data.missing || "None identified")}</p>
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
