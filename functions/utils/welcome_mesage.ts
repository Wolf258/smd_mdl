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





export async function WelcomeMessage(): Promise<void | {confirmation: boolean}> {

  console.log(colors.cyan('Welcome to the fbx model to SMD converter!'));
  const question = await askQuestion(colors.green('Do you want to start the conversion process? yes / no [y/n]'));
  
  switch(question.toLowerCase()){

  case 'y':
    console.log(colors.green('Starting conversion process...'));
    return {confirmation:true};
    
  case 'n':
    console.log(colors.red('Conversion Cancelled'))
    closeReadline();
    return {confirmation:false};

   default:
    console.log(colors.red('Invalid option. Please enter yes / no [y/n].'));
    return WelcomeMessage();

  }

  

}
