# CodePlayer

CodePlayer is a VS Code extension that reads the current file, processes it through a Python-based visualization pipeline, and displays the result as an animated ASCII-style stream using OpenCV, Pygame, and MoviePy.

## Features

- Reads the active editor file
- Extracts tokens and renders them as ASCII output
- Uses local media assets for the playback background
- Runs a Python process from the extension host
- Works as a Visual Studio Code extension project

## Requirements

- VS Code
- Node.js and npm
- Python 3.11
- A local virtual environment named `myenv`

## Setup

1. Open the project in VS Code.
2. Install the Node dependencies:

```bash
npm install
```

3. Create the Python environment if it does not already exist:

```powershell
py -3.11 -m venv myenv
.\myenv\Scripts\python.exe -m pip install opencv-python pygame moviepy
```

4. Press `F5` to launch the extension in Extension Development Host.
5. Open a file in the editor and run:

```text
CodePlayer: Hello World
```

## Run tests

```bash
npm test
```

## Notes

- The project uses a local Python virtual environment in `myenv`.
- Generated VS Code test files and other local artifacts are ignored by Git.
- The extension expects a working local media folder under `Asset/`.

## Project structure

- `extension.js` — VS Code extension entry point
- `frame.py` — Python script that processes file content and renders visuals
- `Asset/` — media assets used for playback
- `myenv/` — local Python environment
- `test/` — extension tests

