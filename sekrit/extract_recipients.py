from __future__ import with_statement

import sys
import GnuPGInterface

def extract_recipients(path):
    # See gpg FAQ, /usr/share/doc/gnupg2/faq.html question 4.12, "How
    # can I get list of key IDs used to encrypt a message?". Note that
    # the result is often subkeys, not primary keys.

    # Don't use --hidden-recipient or --throw-keyids, or extracting
    # recipients will not be possible.
    gpg = GnuPGInterface.GnuPG()

    with file(path, 'rb') as f:
        fpr = gpg.run(
            [
                '--decrypt',
                '--list-only',
                '--quiet',
                ],
            create_fhs=[
                'status',
                # have to redirect stdout as nose sets stdout to be a
                # cStringIO, which has no fileno method
                'stdout',
                ],
            attach_fhs=dict(
                stdin=f,
                ),
            )

        recipients = []
        for line in fpr.handles['status']:
            PREFIX = '[GNUPG:] ENC_TO '
            if not line.startswith(PREFIX):
                continue
            keyid = line[len(PREFIX):].split(None, 1)[0]

            yield keyid

        for line in fpr.handles['stdout']:
            print >>sys.stderr, 'GnuPG stdout:', line.rstrip('\n')

        try:
            fpr.wait()
        except IOError, e:
            print >>sys.stderr, '%s: gnupg: %s' % (sys.argv[0], e)
            sys.exit(1)
