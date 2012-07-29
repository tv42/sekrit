import ConfigParser
import fnmatch
import logging
import os


log = logging.getLogger(__name__)


def filter_ignored(filenames, ignore):
    for name in filenames:
        for pattern in ignore:
            if fnmatch.fnmatch(name, pattern):
                break
        else:
            yield name


def walk(cfg, path):
    prefix = path+os.sep
    def reraise(e):
        raise e
    for root, dirs, files in os.walk(
        top=path,
        onerror=reraise,
        ):

        dirs[:] = [d for d in dirs if d[0] not in '._']
        dirs.sort()
        try:
            ignore = cfg.get('sekrit', 'ignore')
        except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
            ignore = []
        else:
            ignore = ignore.split('\n')
            ignore = [s.strip() for s in ignore]
            ignore = [s for s in ignore if s]

        files = (f for f in files if f[0] not in '._')
        files = filter_ignored(filenames=files, ignore=ignore)
        files = sorted(files)

        if root == path:
            reldir = ''
        else:
            assert root.startswith(prefix), \
                'expecting root to start with prefix: %r' % root
            reldir = root[len(prefix):]
        log.debug('Walking dir: %s', reldir or '.')
        for filename in files:
            relpath = os.path.join(reldir, filename)
            fullpath = os.path.join(root, filename)
            yield (relpath, fullpath)
