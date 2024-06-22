## pagePeek

This script expects a list of urls as input through stdin or a pipe. It utilizes `gowitness` to take a screenshot of that url and then sends this as a discord notification via a webhook.

Examples:
```
$ cat urls.txt | ./pagePeek.py
```