// File: extension.js

const vscode = require("vscode");
const path = require("path");
const fs = require("fs");
const { spawn } = require("child_process");
const MessageHandler = require("./src/messageHandler"); // Adjust path if necessary
// const { getWebviewContent } = require("./src/webview/webview");
const SidebarProvider = require("./src/sideBar/SidebarProvider");
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

  // --- Create an instance of our new SidebarProvider ---
  const provider = new SidebarProvider(context);

  // --- Register the provider for the sidebar view ---
  // The view ID 'cursorclone-sidebar-view' MUST match the ID in package.json
  context.subscriptions.push(
    vscode.window.registerWebviewViewProvider(
      "cursorclone-sidebar-view",
      provider
    )
  );
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
