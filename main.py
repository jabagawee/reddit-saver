#! /usr/bin/env python3

from collections import defaultdict, namedtuple
import getpass
import time
import sys

import praw

DATE = int(time.time())
LIMIT = None
REDDIT_MAX = 1000

r = praw.Reddit(user_agent="1l82ei")
r.login(input("Username: "),getpass.getpass())

bookmarks = list(r.user.get_saved(limit=LIMIT))
if len(bookmarks) == REDDIT_MAX:
    sys.stderr.write("Warning: we've retrieved %d bookmarks (the limit set by reddit), but there may be more\n" % REDDIT_MAX)

folders = defaultdict(list)
Bookmark = namedtuple("Bookmark", ["title", "url"])
for bookmark in bookmarks:
    folders[str(bookmark.subreddit)].append(Bookmark(bookmark.title, str(bookmark.permalink)))

output = ["<!DOCTYPE NETSCAPE-Bookmark-file-1>",
"<title>Bookmarks</title>",
"<h1>Bookmarks</h1>",
"<dl><p>",
'<dt><h3 ADD_DATE="%d" LAST_MODIFIED="%d">Reddit</h3>',
"<dl><p>"]

for subreddit in sorted(folders.keys()):
    output.append('<dt><h3 ADD_DATE="%d" LAST_MODIFIED="%d">%s</h3>' % (DATE, DATE, subreddit))
    output.append("<dl><p>")
    for bookmark in folders[subreddit]:
        output.append('<dt><a href="%s" ADD_DATE="%d">%s</a>' % (bookmark.url, DATE, bookmark.title))
    output.append("</p></dl>")

output.append("</p></dl>")
output.append("</p></dl>")
output = "".join(output)
open("bookmarks.html", "w").write(output)
