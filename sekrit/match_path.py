import fnmatch

def match_path(path, glob):
    return (
        fnmatch.fnmatchcase(path, glob)
        or fnmatch.fnmatchcase(path, '%s/*' % glob)
        )
