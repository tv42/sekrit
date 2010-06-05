import ConfigParser

class UnknownUserError(Exception):
    """Unknown user"""

    def __init__(self, user):
        self.user = user

    def __str__(self):
        return '%s: %s' % (self.__doc__, self.user)

def user_to_fpr(cfg, user):
    try:
        fpr = cfg.get('fingerprints', user)
    except ConfigParser.NoOptionError:
        raise UnknownUserError(user)
    fpr = ''.join(fpr.split(None))
    return fpr
