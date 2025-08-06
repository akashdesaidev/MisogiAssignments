(function () {
  const vscode = acquireVsCodeApi();

  const chatContainer = document.getElementById("chat-container");
  const inputElement = document.getElementById("user-input");
  const sendButton = document.getElementById("send-button");
  const thinkingIndicator = document.getElementById("thinking-indicator");

  document.getElementById("reset-key-button").addEventListener("click", () => {
    vscode.postMessage({
      command: "reset-api-key",
    });
  });
  // Function to send a message to the extension
  function sendMessage() {
    const text = inputElement.value.trim();
    if (text) {
      // Display user message immediately
      appendMessage("user", text);
      inputElement.value = "";
      inputElement.style.height = "auto"; // Reset height

      // Show thinking indicator and post message
      thinkingIndicator.classList.remove("hidden");
      vscode.postMessage({
        command: "user-message",
        text: text,
      });
    }
  }

  // Function to append a message to the chat container
  function appendMessage(sender, text) {
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${sender}-message`;
    messageDiv.innerHTML = marked.parse(text); // Use marked to parse markdown
    chatContainer.appendChild(messageDiv);
    scrollToBottom();
    // After appending, find and add copy buttons to new code blocks
    addCopyButtonsToCodeBlocks();
  }

  // Function to handle streaming agent responses
  function handleAgentResponse(data) {
    thinkingIndicator.classList.add("hidden");

    let lastMessage = chatContainer.lastElementChild;
    // If the last message is not from the agent, or doesn't exist, create a new one
    if (!lastMessage || !lastMessage.classList.contains("agent-message")) {
      lastMessage = document.createElement("div");
      lastMessage.className = "message agent-message";
      chatContainer.appendChild(lastMessage);
    }

    // Append the new text and re-render markdown
    const currentText = lastMessage.getAttribute("data-raw-text") || "";
    const newText = currentText + data;
    lastMessage.setAttribute("data-raw-text", newText);
    lastMessage.innerHTML = marked.parse(newText);

    scrollToBottom();
    addCopyButtonsToCodeBlocks();
  }

  // Auto-resize textarea
  inputElement.addEventListener("input", () => {
    inputElement.style.height = "auto";
    inputElement.style.height = inputElement.scrollHeight + "px";
  });

  // Send on button click
  sendButton.addEventListener("click", sendMessage);

  // Send on Enter key, but allow Shift+Enter for new lines
  inputElement.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  });

  // Listen for messages from the extension
  window.addEventListener("message", (event) => {
    const message = event.data;
    switch (message.command) {
      case "agent-response":
        handleAgentResponse(message.data);
        break;

      // ---> THIS IS THE CORE RESTORE LOGIC <---
      case "restore-history":
        // Clear existing messages before restoring
        chatContainer.innerHTML = "";
        // Loop through the history array sent from the backend
        for (const msg of message.data) {
          // Use the existing function to add each message to the view
          appendMessage(msg.sender, msg.content);
        }
        break;
    }
    // if (message.command === "agent-response") {
    //
    // }
  });

  // Function to scroll to the bottom of the chat
  function scrollToBottom() {
    chatContainer.scrollTop = chatContainer.scrollHeight;
  }

  // Function to add copy buttons to all code blocks
  function addCopyButtonsToCodeBlocks() {
    const codeBlocks = chatContainer.querySelectorAll("pre");
    codeBlocks.forEach((block) => {
      if (block.querySelector(".copy-button")) return; // Don't add if one already exists

      const copyButton = document.createElement("button");
      copyButton.className = "copy-button";
      copyButton.textContent = "Copy";
      block.appendChild(copyButton);

      copyButton.addEventListener("click", () => {
        const code = block.querySelector("code").innerText;
        navigator.clipboard.writeText(code).then(() => {
          copyButton.textContent = "Copied!";
          setTimeout(() => {
            copyButton.textContent = "Copy";
          }, 2000);
        });
      });
    });
  }
  vscode.postMessage({ command: "webview-ready" });
})();
