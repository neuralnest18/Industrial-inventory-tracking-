const { app, BrowserWindow } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let backend;

function createWindow() {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
    }
  });

  win.loadURL('http://localhost:5173');
}

app.whenReady().then(() => {
  // Start Python Flask server
  backend = spawn('python', ['backend/app.py'], {
    cwd: __dirname,
    shell: true
  });

  backend.stdout.on('data', (data) => {
    console.log(`Flask: ${data}`);
  });

  backend.stderr.on('data', (data) => {
    console.error(`Flask Error: ${data}`);
  });

  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    if (backend) backend.kill();
    app.quit();
  }
});
