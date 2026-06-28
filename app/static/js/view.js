
async function loadResume(resumeId) {
    const response = await fetch(`/api/resume/${resumeId}`);

    const data = await response.json();

    document.getElementById("raw-text").textContent =
        data.raw_text || "No raw text available.";

    document.getElementById("parsed-json").textContent =
        JSON.stringify(data.parsed_json, null, 4);
}