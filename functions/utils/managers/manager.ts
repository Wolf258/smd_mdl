import chalk from 'chalk';



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
 
// Tipo de cada tarea: recibe un input y devuelve un output (Promise porque son async)
type AsyncTask<I, O> = (input: I) => Promise<O>;

export async function runPipeline<T>(initialValue: T, tasks: AsyncTask<any, any>[]) {
  let result: any = initialValue;
  for (const task of tasks) {
    result = await task(result);
  }
  return result;
}

