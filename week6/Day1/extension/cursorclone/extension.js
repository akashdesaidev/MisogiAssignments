// File: extension.js

const vscode = require("vscode");
const path = require("path");
const fs = require("fs");
const { spawn } = require("child_process");
const MessageHandler = require("./src/messageHandler"); // Adjust path if necessary
const { getWebviewContent } = require("./src/webview/webview");

// --- Global variable to hold the server process ---
let pythonServerProcess = null;

/**
 * Starts the Python FastAPI server.
 * This function will be called once when the extension is activated.
 * @param {vscode.ExtensionContext} context The extension context.
 */
function startPythonServer(context) {
  // Find the python executable from the .venv
  const venvPath = path.join(context.extensionPath, "venv");
  const isWindows = process.platform === "win32";
  const pythonExecutable = isWindows
    ? path.join(venvPath, "Scripts", "python.exe")
    : path.join(venvPath, "bin", "python");

  if (!fs.existsSync(pythonExecutable)) {
    vscode.window.showErrorMessage(
      "Python executable not found in root 'venv'. Cannot start server."
    );
    return;
  }

  const serverScriptPath = path.join(
    context.extensionPath,
    "python",
    "run_server.py"
  );

  // Spawn the server process
  pythonServerProcess = spawn(pythonExecutable, [serverScriptPath]);

  pythonServerProcess.stdout.on("data", (data) => {
    console.log(`[PythonServer STDOUT]: ${data.toString()}`);
  });

  pythonServerProcess.stderr.on("data", (data) => {
    console.error(`[PythonServer STDERR]: ${data.toString()}`);
    // Optionally show an error to the user if the server fails to start
    vscode.window.showErrorMessage(`Python Server Error: ${data.toString()}`);
  });

  pythonServerProcess.on("close", (code) => {
    console.log(`Python server process exited with code ${code}`);
    pythonServerProcess = null; // Mark that the server is no longer running
  });

  console.log("Python server started.");
}

/**
 * Stops the Python FastAPI server.
 * This function will be called once when the extension is deactivated.
 */
function stopPythonServer() {
  if (pythonServerProcess) {
    console.log("Shutting down Python server...");
    pythonServerProcess.kill(); // This is crucial to prevent zombie processes
    pythonServerProcess = null;
  }
}

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
  console.log('Congratulations, your extension "cursorclone" is now active!');

  // --- Start the server as soon as the extension activates ---
  startPythonServer(context);

  // The command to open your webview panel
  let disposable = vscode.commands.registerCommand(
    "cursorclone.myExtension.start",
    () => {
      vscode.window.showInformationMessage("Hello World from CursorClone!");
      const panel = vscode.window.createWebviewPanel(
        "cursorcloneWebview", // Identifies the type of the webview. Used internally
        "CursorClone", // Title of the panel displayed to the user
        vscode.ViewColumn.One, // Editor column to show the new webview panel in.
        {
          enableScripts: true,
          // Restrict the webview to only loading content from our extension's `media` directory.
          localResourceRoots: [context.extensionUri],
        }
      );

      // Set up the message handler for the panel.
      // It no longer needs to manage the server's lifecycle.
      const messageHandler = new MessageHandler(panel, context);
      panel.webview.onDidReceiveMessage(
        (message) => messageHandler.handleMessage(message),
        undefined,
        context.subscriptions
      );

      // The panel's dispose is now simpler, it doesn't need to kill the server.
      panel.onDidDispose(
        () => {
          // Handle any panel-specific cleanup here if needed
          console.log("Webview panel closed.");
        },
        null,
        context.subscriptions
      );

      // Set the webview's initial HTML content (you'll have your own function for this)
      panel.webview.html = getWebviewContent(
        panel.webview,
        context.extensionUri,
        vscode
      );
    }
  );

  context.subscriptions.push(disposable);

  // Register the server stop function to be called on deactivation
  context.subscriptions.push({
    dispose: stopPythonServer,
  });
}

// This method is called when your extension is deactivated
function deactivate() {
  stopPythonServer();
}

module.exports = {
  activate,
  deactivate,
};
