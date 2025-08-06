const { spawn } = require("child_process");
const path = require("path");
const fs = require("fs"); // Import the file system module
const vscode = require("vscode");

class MessageHandler {
  /**
   * The constructor now also accepts the extension's context object.
   * This is crucial for finding the absolute path to your Python script.
   * @param {vscode.WebviewPanel} panel The webview panel.
   * @param {vscode.ExtensionContext} context The extension context.
   */
  constructor(panel, context) {
    this.panel = panel;
    this.context = context;
  }

  // In MessageHandler.js

  /**
   * Determines the correct Python executable path.
   * Priority:
   * 1. A virtual environment (.venv) inside the extension's directory.
   * 2. The path specified in the user's VS Code settings.
   * @returns {string|null} The path to the Python executable or null if not found.
   */
  getPythonExecutable() {
    // --- START OF DIAGNOSTIC CODE ---
    console.log("--- Running Python Path Check ---");

    // 1. Log the extension's root path to see where it's looking.
    const extensionRoot = this.context.extensionPath;
    console.log(
      `[DEBUG] Extension Root Path (this.context.extensionPath): ${extensionRoot}`
    );

    // --- Check 1: The Virtual Environment ---
    const isWindows = process.platform === "win32";
    const venvPath = path.join(extensionRoot, "venv");
    const venvPython = isWindows
      ? path.join(venvPath, "Scripts", "python.exe")
      : path.join(venvPath, "bin", "python");

    if (fs.existsSync(venvPython)) {
      return venvPython;
    } else {
      console.log(
        "[INFO] Virtual environment Python not found at the expected location."
      );
    }

    // --- Check 2: The User Settings ---
    const userDefinedPath = vscode.workspace
      .getConfiguration("cursorclone")
      .get("pythonPath");

    if (userDefinedPath && fs.existsSync(userDefinedPath)) {
      return userDefinedPath;
    } else {
      console.log(
        "[INFO] User-defined path is either not set or does not exist."
      );
    }

    console.log("--- Python Path Check Failed ---");
    // Return null if no valid path is found.
    return null;
  }

  /**
   * Handles messages from the webview. When a 'user-message' is received,
   * it spawns the Python script and streams its output back to the webview.
   * @param {{command: string, text: string}} message The message from the webview.
   */
  async handleMessage(message) {
    const { command, text } = message;
    console.log("[DEBUG] Received message from webview:", message); // Debug input

    if (command === "user-message") {
      // 1. DETERMINE THE PYTHON EXECUTABLE PATH
      const pythonExecutable = this.getPythonExecutable();

      // 2. VALIDATE THE PATH
      // If no valid path is found, show an error and guide the user.
      if (!pythonExecutable) {
        vscode.window
          .showErrorMessage(
            "Python executable not found. Please create a .venv virtual environment in your project, or set the path in settings.",
            "Open Settings"
          )
          .then((selection) => {
            if (selection === "Open Settings") {
              vscode.commands.executeCommand(
                "workbench.action.openSettings",
                "cursorclone.pythonPath"
              );
            }
          });
        return; // Stop execution
      }

      // 3. DEFINE THE SCRIPT PATH
      const pythonScriptPath = path.join(
        this.context.extensionPath,
        "python",
        "run_graph.py"
      );

      // 4. SPAWN THE CHILD PROCESS with the determined executable
      const pythonProcess = spawn(pythonExecutable, [pythonScriptPath, text]);

      // 5. LISTEN FOR DATA from the Python script's standard output.
      pythonProcess.stdout.on("data", (data) => {
        try {
          console.log("[DEBUG] Received data from python:", data);
          const chunk = JSON.parse(data.toString());
          this.panel.webview.postMessage({
            command: "agent-response",
            data: chunk.data,
          });
        } catch (e) {
          console.error(
            "Error parsing JSON from Python script:",
            data.toString()
          );
        }
      });

      // 6. LISTEN FOR ERRORS from the Python script. Essential for debugging.
      pythonProcess.stderr.on("data", (data) => {
        const errorMessage = data.toString();
        console.error(`Python Script Error: ${errorMessage}`);
        this.panel.webview.postMessage({
          command: "agent-response",
          data: `[PYTHON ERROR] ${errorMessage}`,
        });
      });

      // 7. LOG WHEN the Python process finishes.
      pythonProcess.on("close", (code) => {
        console.log(`Python process exited with code ${code}`);
      });
    }
  }
}

module.exports = MessageHandler;
