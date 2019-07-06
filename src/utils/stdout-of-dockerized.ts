import { execSync } from 'child_process'
import { join, normalize, dirname } from 'path'
import { EOL } from 'os'

const dockerizedBin = './bin/run'

export default function stdoutOfDockerized(command: string): string {
  if (module.parent === null) {
    throw new Error()
  }

  const parentModulePath = dirname(module.parent.filename)
  const dockerizedBinAbsolutePath = normalize(join(process.cwd(), dockerizedBin))

  return String(execSync(
    `${dockerizedBinAbsolutePath} ${command}`,
    {
      cwd: parentModulePath
    }
  ))
}