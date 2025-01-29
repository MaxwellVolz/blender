const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');

const fileName = process.argv[2];  // Taking file name as a command-line argument

// Function to execute shell commands
function executeCommand(command) {
    exec(command, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error: ${error.message}`);
            return;
        }
        if (stderr) {
            console.error(`Stderr: ${stderr}`);
            return;
        }
        console.log(`Stdout: ${stdout}`);
    });
}

// Step 1: Convert GLB to JSX
const gltfjsxCommand = `npx gltfjsx --shadows public/${fileName}.glb --output src/models/${fileName}.jsx`;
executeCommand(gltfjsxCommand);

// Step 2: Modify the JSX file
const filePath = path.join(__dirname, 'src', 'models', `${fileName}.jsx`);

setTimeout(() => {  // Set timeout to wait for file write completion
    fs.readFile(filePath, 'utf8', (err, data) => {
        if (err) {
            console.error(err);
            return;
        }
        const result = data.replace(/export function Model/g, 'export default function Model');

        fs.writeFile(filePath, result, 'utf8', (err) => {
            if (err) {
                console.error(err);
            } else {
                console.log(`${fileName}.jsx modified successfully.`);
            }
        });
    });
}, 3000);
