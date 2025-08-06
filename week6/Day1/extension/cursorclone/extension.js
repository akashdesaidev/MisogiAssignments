// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
const vscode = require("vscode");
// require("dotenv").config({
//   path: require("path").resolve(__dirname, "./.env"),
// });
// console.log("extension.js: File loaded");

const MessageHandler = require("./src/messageHandler");
const { getWebviewContent } = require("./src/webview/webview");
// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
  // Use the console to output diagnostic information (console.log) and errors (console.error)
  // This line of code will only be executed once when your extension is activated
  console.log('Congratulations, your extension "cursorclone" is now active!');

  // The command has been defined in the package.json file
  // Now provide the implementation of the command with  registerCommand
  // The commandId parameter must match the command field in package.json
  const disposable = vscode.commands.registerCommand(
    "cursorclone.myExtension.start",
    function () {
      // The code you place here will be executed every time your command is executed

      // Display a message box to the user
      vscode.window.showInformationMessage("Hello World from CursorClone!");
      const panel = vscode.window.createWebviewPanel(
        "chatPanel",
        "Chat Panel",
        vscode.ViewColumn.Two,
        {
          enableScripts: true,
          localResourceRoots: [context.extensionUri],
        }
      );

      panel.webview.html = getWebviewContent(
        panel.webview,
        context.extensionUri,
        vscode
      );

      const messageHandler = new MessageHandler(panel, context);

      panel.webview.onDidReceiveMessage(
        (message) => {
          // console.log(message);
          return messageHandler.handleMessage(message);
        },
        undefined,
        context.subscriptions
      );
    }
  );

  context.subscriptions.push(disposable);
}

// This method is called when your extension is deactivated
function deactivate() {}

module.exports = {
  activate,
  deactivate,
};
