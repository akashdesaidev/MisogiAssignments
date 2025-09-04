const vscode = require("vscode");
const axios = require("axios");
const crypto = require("crypto");
const fs = require("fs");

const API_KEY_SECRET_KEY = "myExtensionApiKey";
const CHAT_HISTORY_KEY = "chatHistory"; // legacy single-session storage
const CONVERSATION_ID_KEY = "conversationId";
const SESSIONS_KEY = "chatSessions"; // Array of { id, name }
const SESSIONS_HISTORY_KEY = "chatSessionsHistory"; // Map of id -> history array

class SidebarProvider {
  constructor(context) {
    this._context = context;
    this._view = null;
    this.conversationId = null;
    this.sessions = [];
  }

  resolveWebviewView(webviewView, context, token) {
    this._view = webviewView;

    webviewView.webview.options = {
      enableScripts: true,
      localResourceRoots: [this._context.extensionUri],
    };

    // FIX 2: Set the HTML content for the webview
    webviewView.webview.html = this._getHtmlForWebview(webviewView.webview);

    webviewView.webview.onDidReceiveMessage(async (message) => {
      const { command, text } = message;

      switch (message.command) {
        case "webview-ready":
          // Webview is ready, load the session list and restore active session
          await this.loadSessionsFromState();
          await this.loadSession();
          // Notify UI which session is active after load
          this._view?.webview.postMessage({
            command: "sessions-updated",
            data: this.sessions,
            activeId: this.conversationId,
          });
          break;

        case "user-message":
          // Ensure a session is active before processing a message.
          if (!this.conversationId) await this.loadSession();

          this.saveMessageToHistory({ sender: "user", content: message.text });
          await this.handleUserMessage(message.text);
          break;

        case "clear-chat":
          // Clear only current session history
          await this.clearCurrentSessionHistory();
          break;

        case "new-session":
          await this.startNewSession(message.name);
          break;

        case "switch-session":
          await this.switchSession(message.id);
          break;

        case "reset-api-key":
          await this.promptForApiKey(true);
          break;
      }
    });
  }

  _getHtmlForWebview(webview) {
    // 1. Get paths to resources on disk
    const htmlPathOnDisk = vscode.Uri.joinPath(
      this._context.extensionUri,
      "src",
      "sideBar",
      "view.html"
    );
    let htmlContent = fs.readFileSync(htmlPathOnDisk.fsPath, "utf8");

    // 2. Get URIs for the webview
    const styleUri = webview.asWebviewUri(
      vscode.Uri.joinPath(
        this._context.extensionUri,
        "src",
        "sideBar",
        "style.css"
      )
    );
    const scriptUri = webview.asWebviewUri(
      vscode.Uri.joinPath(
        this._context.extensionUri,
        "src",
        "sideBar",
        "main.js"
      )
    );
    const markedUri = webview.asWebviewUri(
      vscode.Uri.joinPath(
        this._context.extensionUri,
        "src",
        "sideBar",
        "marked.min.js"
      )
    );

    function getNonce() {
      let text = "";
      const possible =
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
      for (let i = 0; i < 32; i++) {
        text += possible.charAt(Math.floor(Math.random() * possible.length));
      }
      return text;
    }
    const nonce = getNonce();

    // 3. Replace placeholders
    htmlContent = htmlContent.replace(/{{cspSource}}/g, webview.cspSource);
    htmlContent = htmlContent.replace(/{{nonce}}/g, nonce);
    htmlContent = htmlContent.replace(/{{styleUri}}/g, styleUri);
    htmlContent = htmlContent.replace(/{{scriptUri}}/g, scriptUri);
    htmlContent = htmlContent.replace(/{{markedUri}}/g, markedUri);

    return htmlContent;
  }

  async loadSession() {
    let storedId = this._context.globalState.get(CONVERSATION_ID_KEY);
    if (!storedId) {
      // If there's no stored ID, it's a fresh start.
      await this.startNewSession();
    } else {
      this.conversationId = storedId;
      const allHistories = this._context.globalState.get(
        SESSIONS_HISTORY_KEY,
        {}
      );
      const history = allHistories[storedId] || [];
      this._view.webview.postMessage({
        command: "restore-history",
        data: history,
      });
      console.log(`Chat session loaded. ID: ${this.conversationId}`);
    }
  }

  async startNewSession(name) {
    const id = crypto.randomUUID();
    this.conversationId = id;
    const sessionName = name || `Session ${new Date().toLocaleString()}`;
    console.log(`New chat session created. ID: ${id}`);

    // Persist new active session and empty history
    await this._context.globalState.update(CONVERSATION_ID_KEY, id);
    // Persist per-session history map
    const allHistories = this._context.globalState.get(
      SESSIONS_HISTORY_KEY,
      {}
    );
    allHistories[id] = [];
    await this._context.globalState.update(SESSIONS_HISTORY_KEY, allHistories);

    // Maintain sessions list metadata
    const sessions = await this.loadSessionsFromState();
    sessions.push({ id, name: sessionName });
    await this._context.globalState.update(SESSIONS_KEY, sessions);

    this._view?.webview.postMessage({ command: "restore-history", data: [] });
    this._view?.webview.postMessage({
      command: "sessions-updated",
      data: sessions,
      activeId: id,
    });
  }

  saveMessageToHistory(message) {
    const allHistories = this._context.globalState.get(
      SESSIONS_HISTORY_KEY,
      {}
    );
    const id = this.conversationId;
    const history = allHistories[id] || [];
    history.push(message);
    allHistories[id] = history;
    this._context.globalState.update(SESSIONS_HISTORY_KEY, allHistories);
    // Maintain legacy key for backward compatibility for the current session only
    this._context.globalState.update(CHAT_HISTORY_KEY, history);
  }

  async clearCurrentSessionHistory() {
    const allHistories = this._context.globalState.get(
      SESSIONS_HISTORY_KEY,
      {}
    );
    if (this.conversationId) {
      allHistories[this.conversationId] = [];
      await this._context.globalState.update(
        SESSIONS_HISTORY_KEY,
        allHistories
      );
      this._context.globalState.update(CHAT_HISTORY_KEY, []);
    }
    this._view?.webview.postMessage({ command: "restore-history", data: [] });
    if (this.conversationId) {
      try {
        await axios.post("http://127.0.0.1:8000/clear_history", {
          conversation_id: this.conversationId,
        });
      } catch (e) {
        // ignore server errors on clear
      }
    }
  }

  async switchSession(id) {
    if (!id) return;
    this.conversationId = id;
    await this._context.globalState.update(CONVERSATION_ID_KEY, id);
    const allHistories = this._context.globalState.get(
      SESSIONS_HISTORY_KEY,
      {}
    );
    const history = allHistories[id] || [];
    await this._context.globalState.update(CHAT_HISTORY_KEY, history);
    this._view?.webview.postMessage({
      command: "restore-history",
      data: history,
    });
    this._view?.webview.postMessage({
      command: "sessions-updated",
      data: this.sessions,
      activeId: id,
    });
  }

  async loadSessionsFromState() {
    const sessions = this._context.globalState.get(SESSIONS_KEY, []);
    this.sessions = sessions;
    this._view?.webview.postMessage({
      command: "sessions-updated",
      data: sessions,
      activeId: this.conversationId,
    });
    return sessions;
  }

  async handleUserMessage(text) {
    const apiKey = await this.getApiKey();
    if (!apiKey) return;

    console.log(
      `Sending to FastAPI server (ID: ${this.conversationId}): ${text}`
    );

    try {
      const response = await axios({
        method: "post",
        url: "http://127.0.0.1:8000/invoke",
        data: {
          input: text,
          conversation_id: this.conversationId, // Use the persistent ID
        },
        headers: {
          Authorization: `Bearer ${apiKey}`,
        },
        responseType: "stream",
      });

      let buffer = "";
      const stream = response.data;

      stream.on("data", (chunk) => {
        buffer += chunk.toString();
        let boundary;
        while ((boundary = buffer.indexOf("\n")) !== -1) {
          const jsonStr = buffer.substring(0, boundary);
          buffer = buffer.substring(boundary + 1);
          if (jsonStr) {
            try {
              const parsed = JSON.parse(jsonStr);
              this._view.webview.postMessage({
                command: "agent-response",
                data: parsed.data,
              });
              // Save agent message to history
              this.saveMessageToHistory({
                sender: "agent",
                content: parsed.data,
              });
            } catch (e) {
              console.error("Error parsing JSON chunk:", jsonStr);
            }
          }
        }
      });
      stream.on("end", () => {
        // Process any remaining data in the buffer when the stream ends
        if (buffer.length > 0) {
          try {
            this._view.webview.postMessage({
              command: "agent-response",
              data: JSON.parse(buffer).data,
            });
          } catch (e) {
            console.error("Error parsing final JSON chunk:", buffer);
          }
        }
        console.log("Stream finished.");
      });

      stream.on("error", (err) => console.error("Stream Error:", err));
    } catch (error) {
      console.error("Error communicating with Python server:", error.message);
      vscode.window.showErrorMessage(
        `Could not connect to Python server. ${error.message}`
      );
    }
  }

  async getApiKey() {
    // First, try to retrieve the key from secret storage
    let apiKey = await this._context.secrets.get(API_KEY_SECRET_KEY);

    if (!apiKey) {
      // If not found, prompt the user for it
      apiKey = await this.promptForApiKey();
    }

    return apiKey;
  }

  async promptForApiKey(force = false) {
    if (!force) {
      const storedKey = await this._context.secrets.get(API_KEY_SECRET_KEY);
      if (storedKey) return storedKey;
    }

    const newApiKey = await vscode.window.showInputBox({
      prompt: "Please enter your API Key",
      password: true, // Hides the input
      ignoreFocusOut: true, // Keeps the input box open
    });

    if (newApiKey) {
      // Store the new key securely
      await this._context.secrets.store(API_KEY_SECRET_KEY, newApiKey);
      vscode.window.showInformationMessage("API Key stored successfully.");
      return newApiKey;
    } else {
      vscode.window.showErrorMessage(
        "API Key is required to use this extension."
      );
      return undefined;
    }
  }
}

module.exports = SidebarProvider;
