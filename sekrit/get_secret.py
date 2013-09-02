import GnuPGInterface

class GnuPGError(Exception):
    def __init__(self, gnupg_exception):
        self.gnupg_exception = gnupg_exception
    def __str__(self):
        return str(self.gnupg_exception)

def get_secret(cfg, path):
    with file(path) as fp:
        gpg = GnuPGInterface.GnuPG()
        gpg.options.armor = 1
        gpg.options.meta_interactive = 0

        proc = gpg.run(
            [
                '--decrypt',
                ],
            attach_fhs=dict(
                stdin=fp,
                ),
            create_fhs=['stdout'],
            )

        secret = proc.handles['stdout'].read()

        try:
            proc.wait()
        except IOError, e:
            raise GnuPGError(e)

        return secret
