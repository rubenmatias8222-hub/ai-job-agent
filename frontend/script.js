const API = "http://127.0.0.1:8000";

async function runMatch() {

    const resume = document.getElementById("resume").value;
    const job = document.getElementById("job").value;

    const response = await fetch(
        `${API}/match?resume=${encodeURIComponent(resume)}&job_description=${encodeURIComponent(job)}`,
        { method: "POST" }
    );

    const data = await response.json();

    document.getElementById("results").innerHTML = `
        <h2>📊 Match Report</h2>
        <p><strong>Score:</strong> ${data.match_score}%</p>
        <p><strong>Matched:</strong> ${data.matched_skills.join(", ")}</p>
        <p><strong>Missing:</strong> ${data.missing_skills.join(", ")}</p>
    `;
}

async function runOptimize() {

    const resume = document.getElementById("resume").value;
    const job = document.getElementById("job").value;

    const response = await fetch(
        `${API}/ai-optimize?resume=${encodeURIComponent(resume)}&job_description=${encodeURIComponent(job)}`,
        { method: "POST" }
    );

    const data = await response.json();

    document.getElementById("results").innerHTML = `
        <h2>🧠 AI Optimized Resume</h2>
        <p>${data.rewritten_resume || data.raw_output}</p>

        <hr>

        <h3>📈 ATS Score</h3>
        <p>${data.ats_score_estimate || "N/A"}%</p>

        <h3>✨ Improvements</h3>
        <p>${(data.added_skills || []).join(", ")}</p>
    `;
}

async function loadHistory() {

    const res = await fetch("http://127.0.0.1:8000/history");
    const data = await res.json();

    let html = "<h2>📚 History</h2>";

    data.forEach(item => {
        html += `
            <div style="
                background:#0b1220;
                padding:10px;
                margin-bottom:10px;
                border-radius:8px;
                color:white;
            ">
                <p><strong>Score:</strong> ${item.match_score}%</p>
                <p>${item.resume}</p>
            </div>
        `;
    });

    document.getElementById("results").innerHTML = html;
}
