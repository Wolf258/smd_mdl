import process from 'node:process';
import chalk from 'chalk';
import {askQuestion} from './managers/readuserinput.ts'
import {closeReadline} from './managers/readuserinput.ts'


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


export async function DetectPlatform(): Promise<void | {platform: {confirmation_platform: boolean, platform_user: string}} | {break: boolean}> {
  if (typeof process !== 'undefined' && process.platform) {
    const platform = process.platform;
    console.log(`Sistema operativo (Node.js): ${platform}`); // Ejemplo: 'win32', 'darwin', 'linux'

    if (platform.startsWith('win')) {
      const answer = await askQuestion('¿Are you using Windows? (y/n) To Abort => (x)');
      switch(answer.toLowerCase()){
        case 'y':
          console.log(colors.green('Windows detected'));
          return {platform: {confirmation_platform: true , platform_user: 'windows'}};
        case 'n':
          console.log(colors.red('Platform not supported cannot continue'));
          closeReadline();
          return {platform: {confirmation_platform: false , platform_user: ''}};
        case 'x':
          console.log(colors.yellow('Exiting the application...'));
          closeReadline();
          return {platform: {confirmation_platform: false , platform_user: ''}};
        default:
          console.log(colors.red('Invalid option. Please enter y or n.'));
          return DetectPlatform();
      }
    } else if (platform === 'linux') {
      const answer = await askQuestion('¿Are you using Linux? (y/n). To Abort => (x)');
      switch(answer.toLowerCase()){
        case 'y':
          console.log(colors.green('Linux detected'));
          return {platform: {confirmation_platform: true , platform_user: 'linux'}};
        case 'n':
          console.log(colors.red('Platform not supported cannot continue'));
          closeReadline();
          return {break: true};
        case 'x':
          console.log(colors.yellow('Exiting the application...'));
          closeReadline();
          return {platform: {confirmation_platform: false , platform_user: ''}};
        default:
          console.log(colors.red('Invalid option. Please enter y or n.'));
          return DetectPlatform();
      }
    }
  } else {
    console.log('Platform not supported cannot continue');
    closeReadline();
    return {platform: {confirmation_platform: false , platform_user: ''}};
  }
}

