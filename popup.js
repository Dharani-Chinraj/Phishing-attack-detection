document.addEventListener("DOMContentLoaded", function () {
  const statusEl = document.getElementById("status");
  const button = document.getElementById("checkBtn");

  button.addEventListener("click", function () {
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
      if (!tabs || !tabs[0]) {
        statusEl.textContent = "No active tab found.";
        return;
      }

      const url = tabs[0].url;

      fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ url: url })
      })
      .then(res => res.json())
      .then(data => {
        statusEl.textContent = `Result: ${data.result}`;
      })
      .catch(err => {
        console.error("Error connecting to API:", err);
        statusEl.textContent = "Error connecting to API.";
      });
    });
  });
});
