import GnuPGInterface

def keyid_to_fingerprint(keyid):
    """
    Look up the fingerprint for keyid.

    C{keyid} can also be a keyid of a subkey, and the fingerprint of
    the primary key will be returned.

    @param keyid: the keyid, as hex, without "0x" prefix

    @type keyid: str
    """
    gpg = GnuPGInterface.GnuPG()

    p = gpg.run(
        [
            '--fingerprint',
            '--fingerprint',
            '--with-colons',
            '--fixed-list-mode',
            '0x%s' % keyid,
            ],
        create_fhs=[
            'stdout',
            ],
        )

    pub = None
    fpr = None
    for line in p.handles['stdout']:
        type_ = line.split(':', 1)[0]
        if type_ == 'pub':
            pub = line.split(':', 5)[4]
        elif type_ == 'fpr':
            if pub is None:
                # subkey fingerprint, ignore
                continue
            if fpr is not None:
                raise RuntimeError('More than one key found with keyid: %r' % keyid)
            assert pub is not None
            fpr = line.split(':', 10)[9]
            assert fpr.endswith(pub)
        elif type_ == 'sub':
            pub = None

    try:
        p.wait()
    except IOError, e:
        print >>sys.stderr, '%s: gnupg: %s' % (sys.argv[0], e)
        sys.exit(1)

    return fpr

