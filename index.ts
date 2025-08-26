//Imports
import dotenv from 'dotenv';
import * as readline from 'readline';
import chalk from "chalk";
import {runPipeline} from './functions/utils/managers/manager.ts'
import { WelcomeMessage } from './functions/utils/welcome_mesage.ts';
import { DetectPlatform } from './functions/utils/detect_platform.ts';
import { manager } from './functions/utils/managers/subprocess_manager.ts';
 
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

//variables de entorno PATHS para evitar poner rutas a cada rato.
dotenv.config({path: '/.env'});

var data = {
   confirmation: false,
   platform: {confirmation_platform: false , platform_user: ''},
   fbx:'',
   materials: [],
   textures: [],
}





// Tipo de cada tarea: recibe un input y devuelve un output (Promise porque son async)
type AsyncTask<I, O> = (input: I) => Promise<O>;

(async () => {
  const result = await runPipeline(data, [WelcomeMessage, DetectPlatform, manager]);
  console.log("🎉 Resultado final:", result);
})();