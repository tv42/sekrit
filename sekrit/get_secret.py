import GnuPGInterface
import contextlib
import subprocess
import sys

@contextlib.contextmanager
def prompt_to_fp(message):
    with file('/dev/null') as devnull:
        askpass = subprocess.Popen(
            args=[
                'gksu',
                '--print-pass',
                '--message',
                message,
                ],
            stdin=devnull,
            stdout=subprocess.PIPE,
            close_fds=True,
            )
        yield askpass.stdout
        retcode = askpass.wait()
        if retcode < 0:
            raise RuntimeError('gksu exited with status %r', retcode)

class GnuPGError(Exception):
    def __init__(self, gnupg_exception):
        self.gnupg_exception = gnupg_exception
    def __str__(self):
        return str(self.gnupg_exception)

def get_secret(cfg, path):
    with file(path) as fp:
        with prompt_to_fp('GnuPG passphrase') as askpass:

            gpg = GnuPGInterface.GnuPG()
            gpg.options.armor = 1
            gpg.options.meta_interactive = 0

            proc = gpg.run(
                [
                    '--decrypt',
                    '--no-use-agent',
                    ],
                attach_fhs=dict(
                    stdin=fp,
                    passphrase=askpass,
                    ),
                create_fhs=['stdout'],
                )

            secret = proc.handles['stdout'].read()

            try:
                proc.wait()
            except IOError, e:
                raise GnuPGError(e)

            return secret
