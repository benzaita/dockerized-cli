# Environment Variables

This example shows how to pass arbitrary environment variables to a command that `builder` executes.

Simply prepend the command with `KEY=VALUE` pairs:

```sh
$ builder exec FOO=foo BAR=bar env
HOSTNAME=linuxkit-025000000001
SHLVL=1
HOME=/root
TERM=xterm
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
FOO=foo
BAR=bar
```
