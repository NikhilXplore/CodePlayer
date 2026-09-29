// The module 'vscode' contains the VS Code extensibility API



// Import the module and reference it with the alias vscode in your code below
const vscode = require('vscode');
const { spawn } = require('child_process');
const path = require('path');

/** @type {import('child_process').ChildProcess | undefined} */
let runningProcess;
const stoppedProcesses = new WeakSet();

// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {

	// Use the console to output diagnostic information (console.log) and errors (console.error)
	// This line of code will only be executed once when your extension is activated
	console.log('Congratulations, your extension "codeplayer" is now active!');

	// The command has been defined in the package.json file
	// Now provide the implementation of the command with  registerCommand
	// The commandId parameter must match the command field in package.json
	const disposable = vscode.commands.registerCommand('codeplayer.helloWorld', function () {
		// The code you place here will be executed every time your command is executed
		const editor = vscode.window.activeTextEditor;
		if(!editor){
			vscode.window.showErrorMessage("Open a file first");
			return;
		}

		const extensionPath = context.extensionPath;

		const pythonExe = path.join(extensionPath, 'myenv', 'Scripts', 'python.exe');
		const scriptPath = path.join(extensionPath, 'frame.py');

		if (runningProcess) {
			stoppedProcesses.add(runningProcess);
			runningProcess.kill();
			runningProcess = undefined;
		}

		const python = spawn(pythonExe, [scriptPath, editor.document.uri.fsPath], {
			cwd: extensionPath,
			windowsHide: true,
		});
		runningProcess = python;

		python.stdout.on("data", (data)=>{
			const fullRange = new vscode.Range(
				editor.document.positionAt(0),
				editor.document.positionAt(editor.document.getText().length)
			);
			const frame = data.toString();
			editor.edit(editBuilder=>{
				editBuilder.replace(fullRange, frame);
			});
		});

		python.stderr.on("data", (err)=>{
			console.error(`CodePlayer: ${err.toString()}`);
		});
		python.on("error", (error) => {
			runningProcess = undefined;
			vscode.window.showErrorMessage(`CodePlayer could not start Python: ${error.message}`);
		});
		python.on("close", (code) => {
			if (runningProcess === python) {
				runningProcess = undefined;
			}
			if (code !== 0 && !stoppedProcesses.has(python)) {
				vscode.window.showErrorMessage(`CodePlayer stopped with exit code ${code}. Check the Python output.`);
			}
		});
		// Display a message box to the user
		vscode.window.showInformationMessage('Hello World from CodePlayer!');
	});

	context.subscriptions.push(disposable);
}

// This method is called when your extension is deactivated
function deactivate() {
	if (runningProcess) {
		stoppedProcesses.add(runningProcess);
		runningProcess.kill();
		runningProcess = undefined;
	}
}

module.exports = {
	activate,
	deactivate
}
