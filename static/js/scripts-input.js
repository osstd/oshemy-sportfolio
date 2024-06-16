function generateUrlInputs() {
  const numberOfInputs = document.getElementById("numberOfInputs").value;
  const urlInputsContainer = document.getElementById("urlInputsContainer");

  urlInputsContainer.innerHTML = "";

  if (!document.getElementById("nameInput")) {
    const nameInput = document.createElement("input");
    nameInput.setAttribute("type", "text");
    nameInput.setAttribute("name", "name");
    nameInput.setAttribute("id", "nameInput");
    nameInput.setAttribute("placeholder", "Name");
    nameInput.classList.add("input-field");
    urlInputsContainer.appendChild(nameInput);
    urlInputsContainer.appendChild(document.createElement("br"));
  }

  if (!document.getElementById("titleInput")) {
    const titleInput = document.createElement("input");
    titleInput.setAttribute("type", "text");
    titleInput.setAttribute("name", "title");
    titleInput.setAttribute("id", "titleInput");
    titleInput.setAttribute("placeholder", "Title");
    titleInput.classList.add("input-field");
    urlInputsContainer.appendChild(titleInput);
    urlInputsContainer.appendChild(document.createElement("br"));
  }
  for (let i = 0; i < numberOfInputs; i++) {
    const inputElement = document.createElement("input");
    inputElement.setAttribute("type", "text");
    inputElement.setAttribute("name", "urls");
    inputElement.classList.add("input-field");
    inputElement.setAttribute("placeholder", `URL ${i + 1}`);
    urlInputsContainer.appendChild(inputElement);
    urlInputsContainer.appendChild(document.createElement("br"));
  }

  if (!document.getElementById("submitButton")) {
    const submitButton = document.createElement("button");
    submitButton.setAttribute("type", "submit");
    submitButton.setAttribute("id", "submitButton");
    submitButton.innerText = "Submit";
    submitButton.classList.add("btn", "btn-primary");
    urlInputsContainer.appendChild(submitButton);
  }
}
