//Imports
import dotenv from 'dotenv';
import chalk from "chalk";
import {runPipeline} from './functions/utils/managers/manager.ts'
import { WelcomeMessage } from './functions/utils/welcome_mesage.ts';
import { DetectPlatform } from './functions/utils/detect_platform.ts';
import { subprocess_manager } from './functions/utils/managers/subprocess_manager.ts';
import {fileLister} from './functions/utils/file_lister.ts'
 


// Variables de entorno PATHS para evitar poner rutas a cada rato.
dotenv.config({path: '/.env'});
// Variables globales.
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

const path_files_list_json = process.env.path_files_list_json;

var data = {
   confirmation: false,
   platform: {confirmation_platform: null , platform_user: ''},
   break: false,
   filesList_jsonpath: './resources/temp/file_list.json'
}


// Tipo de cada tarea: recibe un input y devuelve un output (Promise porque son async)
type AsyncTask<I, O> = (input: I) => Promise<O>;

(async () => {
  const result = await runPipeline(data, [WelcomeMessage,DetectPlatform,fileLister(path_files_list_json)]);
  console.log("Resultado final:", result);
})();