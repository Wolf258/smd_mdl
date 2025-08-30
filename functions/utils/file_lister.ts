import os from 'os';
import path from 'path';
import chalk from 'chalk';
import fs from 'fs';
import {askQuestion} from './managers/readuserinput.ts'

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

const scriptPath = path.resolve(__filename);
const filesPath = path.resolve(scriptPath, '../../../resources/models');

export function fileLister(directory: string): Promise<string[]> {
    return new Promise((resolve, reject) => {
        fs.readdir(directory, (err: NodeJS.ErrnoException | null, files: string[] | Buffer[]) => {
            if (err) {
                console.error(colors.red(`Error reading directory '${directory}': ${err.message}`));
                reject(err);
            } else {
                console.log(colors.green(`Files in directory '${directory}':`));
                files.forEach(file => {
                    console.log(colors.blue(` - ${file}`));
                    // Exportamos los nombres de los archivos en json.
                    fs.writeFileSync(path.resolve(filesPath, 'file_list.json'), JSON.stringify(files, null, 2));
                });
                resolve(files as string[]);
            }
        });
    });
}


fileLister(filesPath);

