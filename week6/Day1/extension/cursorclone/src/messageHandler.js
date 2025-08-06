const axios = require("axios");
const path = require("path");
const vscode = require("vscode");
const crypto = require("crypto"); // Built-in Node.js module for unique IDs

class MessageHandler {
  constructor(panel, context) {
    this.panel = panel;
    this.context = context;
    // --- Generate a unique ID for this conversation session ---
    this.conversationId = crypto.randomUUID();
    console.log(`New chat session started with ID: ${this.conversationId}`);
  }

  async handleMessage(message) {
    const { command, text } = message;

    if (command === "user-message") {
      console.log(
        `Sending to FastAPI server (ID: ${this.conversationId}): ${text}`
      );

      try {
        const response = await axios({
          method: "post",
          url: "http://127.0.0.1:8000/invoke",
          // --- Send both the input and the conversation ID ---
          data: {
            input: text,
            conversation_id: this.conversationId,
          },
          responseType: "stream",
        });

        const stream = response.data;

        stream.on("data", (chunk) => {
          const chunkStr = chunk.toString();
          const jsonObjects = chunkStr.split("\n").filter(Boolean);

          for (const jsonObjStr of jsonObjects) {
            try {
              const parsed = JSON.parse(jsonObjStr);
              this.panel.webview.postMessage({
                command: "agent-response",
                data: parsed.data,
              });
            } catch (e) {
              console.error("Error parsing JSON chunk:", jsonObjStr);
            }
          }
        });

        stream.on("end", () => console.log("Stream finished."));
        stream.on("error", (err) => console.error("Stream Error:", err));
      } catch (error) {
        console.error("Error communicating with Python server:", error.message);
        vscode.window.showErrorMessage(
          `Could not connect to Python server. ${error.message}`
        );
      }
    }

    // You could add a new command to clear history
    if (command === "clear-chat") {
      console.log(`Clearing history for ID: ${this.conversationId}`);
      await axios.post("http://127.0.0.1:8000/clear_history", {
        conversation_id: this.conversationId,
      });
      // You might want to send a message back to the UI to confirm
      this.panel.webview.postMessage({ command: "history-cleared" });
    }
  }
}

module.exports = MessageHandler;
