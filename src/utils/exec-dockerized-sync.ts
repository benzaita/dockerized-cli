import { spawnSync } from 'child_process'
import { join, normalize, dirname } from 'path'

const dockerizedBin = './bin/run'

interface Options {
  cwd?: string
  env?: NodeJS.ProcessEnv
}

interface Output {
  stdout: string
  stderr: string
  status: number | null
}

export default function execDockerizedSync(
  command: string,
  args: string[] = [],
  options: Options = {}
): Output {
  if (module.parent === null) {
    throw new Error()
  }

  const parentModulePath = dirname(module.parent.filename)
  const dockerizedBinAbsolutePath = normalize(join(process.cwd(), dockerizedBin))

  const spawnResult = spawnSync(
    dockerizedBinAbsolutePath,
    [command, ...args],
    {
      cwd: options.cwd || parentModulePath,
      env: Object.assign({}, process.env, options.env)
    }
  )

  return {
    stdout: String(spawnResult.stdout),
    stderr: String(spawnResult.stderr),
    status: spawnResult.status
  }
}