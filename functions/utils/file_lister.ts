import os from 'os';
import path from 'path';
import chalk from 'chalk';
import fs from 'fs';


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

// Now fileLister returns a function that takes input and returns a Promise
export function fileLister(directory: string) {
    return async function(input: any): Promise<any> {
        return new Promise((resolve, reject) => {
            fs.readdir(directory, (err: NodeJS.ErrnoException | null, files: string[] | Buffer[]) => {
                if (err) {
                    console.error(colors.red(`Error reading directory '${directory}': ${err.message}`));
                    reject(err);
                } else {
                    console.log(colors.green(`Files in directory '${directory}':`));
                    console.log(colors.gray('-------------------------------------'))
                    console.log(colors.cyan('These files will be processed:'))
                    files.forEach(file => {
                        console.log(colors.blue(` - ${file}`));
                    });
                    // Exportamos los nombres de los archivos en json.
                    fs.writeFileSync(path.resolve(filesPath, 'file_list.json'), JSON.stringify(files, null, 2));
                    // Merge fileslist into input and return
                    resolve({...input, fileslist: files as string[]});
                }
            });
        });
    }
}

