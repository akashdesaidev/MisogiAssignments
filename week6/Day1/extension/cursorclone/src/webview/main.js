(function () {
  // A reference to the VS Code API, used to post messages back to the extension
  const vscode = acquireVsCodeApi();

  // Get references to the DOM elements
  const chatContainer = document.getElementById("chat-container");
  const chatForm = document.getElementById("chat-form");
  const chatInput = document.getElementById("chat-input");
  const loadingIndicator = document.getElementById("loading-indicator");

  // --- THIS IS THE FIX ---
  // The variable must be declared here, in the outer scope, so that
  // both event listeners below can access and modify it.
  let currentBotMessageElement = null;

  // Handle form submission (when the user sends a message)
  chatForm.addEventListener("submit", (event) => {
    event.preventDefault(); // Prevent page reload
    const messageText = chatInput.value.trim();

    if (messageText) {
      // Now this line can correctly access the variable to reset it
      currentBotMessageElement = null;

      vscode.postMessage({
        command: "user-message",
        text: messageText,
      });

      displayMessage(messageText, "user");
      chatInput.value = "";
      loadingIndicator.classList.remove("hidden");
    }
  });

  // Listen for messages (chunks) sent from the extension
  window.addEventListener("message", (event) => {
    const message = event.data;

    if (message.command === "agent-response") {
      loadingIndicator.classList.add("hidden");

      const chunkText = message.data;

      // This block can now correctly access the variable
      if (currentBotMessageElement) {
        currentBotMessageElement.textContent += chunkText;
      } else {
        currentBotMessageElement = displayMessage(chunkText, "bot");
      }
      chatContainer.scrollTop = chatContainer.scrollHeight;
    }
  });

  /**
   * Creates and displays a new message element in the chat.
   * @param {string} text - The content of the message.
   * @param {'user' | 'bot'} type - The sender, for styling.
   * @returns {HTMLElement} The newly created message div.
   */
  function displayMessage(text, type) {
    const messageElement = document.createElement("div");
    messageElement.classList.add("message", type);
    messageElement.textContent = text;
    chatContainer.appendChild(messageElement);
    chatContainer.scrollTop = chatContainer.scrollHeight;
    return messageElement;
  }
})();
