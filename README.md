# Mental Floss author feed

Given a mentalfloss.com author slug, this script scrapes their articles,
generates an Atom feed, and prints it to standard output.

Intended use case is in a cron job writing to a file which is served
by an HTTP server. Point your feed reader to the generated file's URL.

Example crontab, refreshing once per hour:

```bash
MAILTO=me@example.com
0 * * * * /path/to/mf-feed.py 'ken-jennings' > /var/www/example.com/kennections.atom
```

Requires Python3, Requests, Beautiful Soup, lxml, and feedgen.
