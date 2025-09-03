// manager.ts
import { spawn } from 'child_process';
import path from 'path';
import chalk from 'chalk';

// Colores para la salida en consola
const colors = {
    red: chalk.red,
    green: chalk.green,
    yellow: chalk.yellow,
    blue: chalk.blue,
    magenta: chalk.magenta,
    cyan: chalk.cyan,
    white: chalk.white,
    gray: chalk.gray,
    black: chalk.black
};



// Define las rutas a los scripts de Python
const material_obtainer = path.join(__dirname, '../../../scripts/material_obtainer.py');
const fbx2smd = path.join(__dirname, '../../../scripts/fbx2smd.py');




export async function subprocess_manager(): Promise<void> {
  console.log(colors.green('Starting the conversion...'));

  // 1. Iniciar material_obtainer.py
  const child1 = spawn('blender', ['--background', '--python', material_obtainer]);

  child1.stdout.on('data', (data) => {
    const message = data.toString().trim();
    console.log(`Datos recibidos de material_obtainer.py: ${message}`);

  });

  // 2. inciar fbx2smd
  const child2 = spawn('python', [fbx2smd]);
  console.log('fbx2smd executed')

  child2.stdout.on('data', (data) => {
    const message = data.toString().trim();
    console.log(`Datos recibidos de fbx2smd.py: ${message}`);
  });

  child1.stderr.on('data', (error) => {
    console.error(`Error de funcion1.py: ${error.toString()}`);
  });

  child1.on('close', (code) => {
    console.log(`funcion1.py ha terminado con código ${code}`);
  });
};
