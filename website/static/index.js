const dropdownButton = document.querySelector(".dropdown-button");
const dropdownButton2 = document.querySelector(".dropdown-button2");
const allNews = document.querySelector(".mb-1");
const politicalNews = document.querySelector(".mb-2");
const customFilter = document.querySelector(".mb-3");
const customInput = document.querySelector(".custom-input");
const getButton = document.querySelector(".get-button");

let selectedFilter = "";
let selectedCount = 5;

allNews?.addEventListener("click", (e) => {
  dropdownButton.innerHTML = "All";
  customInput.classList.add("hidden");
  selectedFilter = "";
});
politicalNews?.addEventListener("click", (e) => {
  dropdownButton.innerHTML = "Politics";
  customInput.classList.add("hidden");
  selectedFilter = "politic";
});
customFilter?.addEventListener("click", (e) => {
  dropdownButton.innerHTML = "Custom";
  selectedFilter = customInput.value;
  customInput.classList.remove("hidden");
});

getButton?.addEventListener("click", async (e) => {
  getButton.disabled = true;
  document.querySelector(".loader").classList.remove("hidden");
  try {
    const response = await fetch("/generate-news", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        count: selectedCount,
        filter: selectedFilter.trim(),
      }),
    });
    const data = await response.json();
    if (response.ok) {
      window.location.reload();
    } else {
      alert("Error: " + data.error);
    }
  } catch (error) {
    console.error("Request failed", error);
    alert("Failed to generate news");
  } finally {
    getButton.disabled = false;
    document.querySelector(".loader").classList.add("hidden");
  }
});

document.querySelector(".mbt-1")?.addEventListener("click", (e) => {
  const value = e.target.innerText;
  dropdownButton2.innerHTML = value;
  selectedCount = parseInt(value);
});

document.querySelector(".mbt-2")?.addEventListener("click", (e) => {
  const value = e.target.innerText;
  dropdownButton2.innerHTML = value;
  selectedCount = parseInt(value);
});

document.querySelector(".mbt-3")?.addEventListener("click", (e) => {
  const value = e.target.innerText;
  dropdownButton2.innerHTML = value;
  selectedCount = parseInt(value);
});

document.querySelector(".mbt-4")?.addEventListener("click", (e) => {
  const value = e.target.innerText;
  dropdownButton2.innerHTML = value;
  selectedCount = parseInt(value);
});
