// FORM SUBMIT
document.getElementById("matchForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const resumeFile = document.getElementById("resumeFile").files[0];
const job_description = document.getElementById("job_description").value;
const resultDiv = document.getElementById("result");

resultDiv.innerHTML = "Analyzing...";

if (!resumeFile) {
  alert("Please upload your CV first");
  return;
}

try {
  const formData = new FormData();
  formData.append("file", resumeFile);
  formData.append("job_description", job_description);

  const res = await fetch("/api/match", {
    method: "POST",
    body: formData
  });

  const data = await res.json();

  resultDiv.innerHTML = `
    <h2>Match Result</h2>
    <p><strong>Score:</strong> ${data.score}%</p>

    <h3>Matched Skills</h3>
    <p>${data.matched.join(", ")}</p>

    <h3>Missing Skills</h3>
    <p>${data.missing.join(", ")}</p>

    <h3>AI Insight</h3>
    <p>${data.explanation}</p>
  `;

} catch (err) {
  console.error(err);
  resultDiv.innerHTML = "Error processing file.";
}
});

function showMatch() {
  document.getElementById("matchForm").style.display = "block";
  document.getElementById("result").innerHTML = "";
}

function showHistory() {
  document.getElementById("result").innerHTML = "<h3>History coming soon...</h3>";
}
