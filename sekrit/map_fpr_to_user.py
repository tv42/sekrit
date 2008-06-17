def map_fpr_to_user(cfg, fpr):
    result = None
    for user in cfg.options('fingerprints'):
        got_fpr = cfg.get('fingerprints', user)
        # allow spaces inside the fingerprint, for copy-paste
        # from gpg --list-secret-keys --fingerprint
        got_fpr = ''.join(got_fpr.split(None))

        if got_fpr == fpr:
            if result is not None:
                raise RuntimeError(
                    'Fingerprint %r belongs to both %r and %r' \
                        % (fpr, result, user),
                    )
            result = user

    return result
