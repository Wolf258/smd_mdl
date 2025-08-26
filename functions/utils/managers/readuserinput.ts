import * as readline from 'readline';
import chalk from "chalk";

// Colores
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
// Crea una única instancia de readline
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

/**
 * Lee la entrada del usuario con una pregunta y devuelve una promesa con la respuesta.
 * @param query La pregunta a mostrar al usuario.
 * @returns Una promesa que se resuelve con la respuesta del usuario.
 */
export function askQuestion(query: string): Promise<string> {
  return new Promise(resolve => {
    rl.question(colors.blue(query), (answer) => {
      resolve(answer);
    });
  });
}

/**
 * Cierra la interfaz de readline. Debe llamarse al final del programa.
 */
export function closeReadline(): void {
  rl.close();
}