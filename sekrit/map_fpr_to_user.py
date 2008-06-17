def map_fpr_to_user(cfg, users):
    r = {}
    for user in users:
        fpr = cfg.get('fingerprints', user)
        # allow spaces inside the fingerprint, for copy-paste
        # from gpg --list-secret-keys --fingerprint
        fpr = ''.join(fpr.split(None))

        if fpr in r:
            raise RuntimeError(
                'Fingerprint %r belongs to both %r and %r' \
                    % (fpr, user, r[fpr]),
                )
        r[fpr] = user

    return r
