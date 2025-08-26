import process from 'node:process';
import chalk from 'chalk';
import {askQuestion} from './readuserinput.ts'
import {closeReadline} from './readuserinput.ts'


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


export async function DetectPlatform(): Promise<void | {platform: string}> {
    
   if (typeof process !== 'undefined' && process.platform) {
  const platform = process.platform;
  console.log(`Sistema operativo (Node.js): ${platform}`); // Ejemplo: 'win32', 'darwin', 'linux'

  if (platform.startsWith('win')) {
    return {platform: 'windows'};
  } else if (platform === 'darwin') {
    return {platform: 'macOS'};
  } else if (platform === 'linux') {
    return {platform: 'linux'};
  }
} else {
    console.log('Platform not detected cant continue');
    return;
}

}

