function getWebviewContent(webview, extensionUri, vscode) {
  // Get the URIs for our local resources
  const scriptUri = webview.asWebviewUri(
    vscode.Uri.joinPath(extensionUri, "src/webview", "main.js")
  );
  const styleUri = webview.asWebviewUri(
    vscode.Uri.joinPath(extensionUri, "src/webview", "webview.css")
  );

  return `
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <link rel="stylesheet" href="${styleUri}">
      <title>CursorClone Chat</title>
    </head>
    <body>
      <div id="chat-container">
        <!-- Chat messages will be appended here -->
      </div>

      <div id="loading-indicator" class="hidden">
        <div class="dot"></div>
        <div class="dot"></div>
        <div class="dot"></div>
      </div>

      <div id="input-area">
        <form id="chat-form">
          <input type="text" id="chat-input" placeholder="Ask a question or type a command..." autocomplete="off">
          <button type="submit" id="send-button" title="Send Message">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="18" height="18">
              <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
            </svg>
          </button>
        </form>
      </div>
      
      <script src="${scriptUri}"></script>
    </body>
    </html>
  `;
}

module.exports = {
  getWebviewContent,
};
