function generateUrlInputs() {
  document.getElementById("urlForm").style.display = "block";

  const numberOfInputs = document.getElementById("numberOfInputs").value;
  const urlInputsContainer = document.getElementById("urlInputsContainer");
  const mediaSelect = document.getElementById("mediaSelect");

  urlInputsContainer.innerHTML = "";

  if (!document.getElementById("nameInput")) {
    const nameInput = document.createElement("input");
    nameInput.setAttribute("type", "text");
    nameInput.setAttribute("name", "name");
    nameInput.setAttribute("id", "nameInput");
    nameInput.setAttribute("placeholder", "Name");
    nameInput.classList.add("input-field");
    urlInputsContainer.appendChild(nameInput);
  }

  if (!document.getElementById("titleInput")) {
    const titleInput = document.createElement("input");
    titleInput.setAttribute("type", "text");
    titleInput.setAttribute("name", "title");
    titleInput.setAttribute("id", "titleInput");
    titleInput.setAttribute("placeholder", "Title");
    titleInput.classList.add("input-field");
    urlInputsContainer.appendChild(titleInput);
  }

  if (!document.getElementById("mediaInput")) {
    const mediaInput = document.createElement("input");
    mediaInput.setAttribute("type", "text");
    mediaInput.setAttribute("name", "media");
    mediaInput.setAttribute("id", "mediaInput");
    mediaInput.setAttribute("placeholder", "Media type");
    mediaInput.classList.add("input-field");
    urlInputsContainer.appendChild(mediaInput);
    mediaInput.style.display = "none";
    mediaInput.value = mediaSelect.value;
  }

  if (mediaSelect.value === "vid") {
    if (!document.getElementById("mediaLength")) {
      const mediaLength = document.createElement("select");
      mediaLength.setAttribute("name", "length");
      mediaLength.setAttribute("id", "mediaLength");
      mediaLength.classList.add("custom-select");

      const optionShort = document.createElement("option");
      optionShort.value = "short";
      optionShort.textContent = "Short";

      const optionLong = document.createElement("option");
      optionLong.value = "long";
      optionLong.textContent = "Long";

      mediaLength.appendChild(optionShort);
      mediaLength.appendChild(optionLong);

      urlInputsContainer.appendChild(mediaLength);
    }
  }

  if (!document.getElementById("url-grid")) {
    const urlInput = document.createElement("div");
    urlInput.setAttribute("id", "url-grid");
    urlInputsContainer.appendChild(urlInput);
  }

  const urlInput = document.getElementById("url-grid");

  for (let i = 0; i < numberOfInputs; i++) {
    const inputElement = document.createElement("input");
    inputElement.setAttribute("type", "text");
    inputElement.setAttribute("name", "urls");
    inputElement.classList.add("input-url");
    inputElement.setAttribute("placeholder", `URL ${i + 1}`);
    urlInput.appendChild(inputElement);
  }

  urlInputsContainer.appendChild(urlInput);

  if (!document.getElementById("submitButton")) {
    const submitButton = document.createElement("button");
    submitButton.setAttribute("type", "submit");
    submitButton.setAttribute("id", "submitButton");
    submitButton.innerText = "Submit";
    submitButton.classList.add("btn", "btn-primary");
    urlInputsContainer.appendChild(submitButton);
  }
}
