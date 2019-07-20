import { execSync } from 'child_process'
import { join, normalize, dirname } from 'path'

const dockerizedBin = './bin/run'

interface Options {
  cwd?: string
}

export default function stdoutOfDockerized(command: string, options: Options = {}): string {
  if (module.parent === null) {
    throw new Error()
  }

  const parentModulePath = dirname(module.parent.filename)
  const dockerizedBinAbsolutePath = normalize(join(process.cwd(), dockerizedBin))

  return String(execSync(
    `${dockerizedBinAbsolutePath} ${command}`,
    {
      cwd: options.cwd || parentModulePath
    }
  ))
}