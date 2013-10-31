import GnuPGInterface
import os
import subprocess
import sys

from sekrit import decide_recipients
from sekrit import user_to_fpr

def prompt(message):
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
        reply = askpass.stdout.readline()
        retcode = askpass.wait()
        if retcode < 0:
            raise RuntimeError('gksu exited with status %r', retcode)
        assert reply.endswith('\n')
        return reply

def set_secret(cfg, path):
    users = decide_recipients.decide_recipients(cfg, path)
    users = list(users)
    if not users:
        raise RuntimeError('Nobody to encrypt to: %s', path)

    fingerprints = [
        user_to_fpr.user_to_fpr(cfg=cfg, user=user)
        for user in users
        ]
    if not fingerprints:
        raise RuntimeError('No fingerprints found for users: %s', ' '.join(users))

    gpg = GnuPGInterface.GnuPG()
    gpg.options.armor = 1
    gpg.options.meta_interactive = 0
    gpg.options.recipients = fingerprints

    if not os.isatty(sys.stdin.fileno()):
        # redirected from file / pipe, read passphrase from there
        secret1 = sys.stdin.readline()
        secret1 = secret1.rstrip('\n')
    else:
        secret1 = prompt(message='Passphrase for %s' % path)
        secret2 = prompt(message='Repeat pass for %s' % path)

        if secret1 != secret2:
            del secret1
            del secret2
            print >>sys.stderr, '%s: Passphrases do not match.' % sys.argv[0]
            sys.exit(1)

        del secret2

    tmp = '{path}.{pid}.tmp'.format(
        path=path,
        pid=os.getpid(),
        )
    with file(tmp, 'w') as fp:
        try:
            proc = gpg.run(
                [
                    '--encrypt',
                    '--for-your-eyes-only',
                    '--trust-mode=always',
                    ],
                create_fhs=['stdin'],
                attach_fhs=dict(
                    stdout=fp,
                    logger=sys.stderr,
                    ),
                )

            proc.handles['stdin'].write(secret1)
            del secret1
            proc.handles['stdin'].close()

            try:
                proc.wait()
            except IOError, e:
                print >>sys.stderr, '%s: gnupg: %s' % (sys.argv[0], e)
                sys.exit(1)
        except:
            try:
                os.unlink(tmp)
            except:
                pass
            raise

    os.rename(tmp, path)

    print 'Encrypted to:'
    for uid in users:
        print '\t%s' % uid
