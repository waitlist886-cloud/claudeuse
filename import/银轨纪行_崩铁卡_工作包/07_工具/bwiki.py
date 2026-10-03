# -*- coding: utf-8 -*-
"""取 bwiki 页面正文为纯文本：python3 bwiki.py <页名> [--html]"""
import sys, json, re, html, urllib.parse, urllib.request
def fetch(page):
    u = 'https://wiki.biligame.com/sr/api.php?' + urllib.parse.urlencode(
        dict(action='parse', page=page, prop='text', format='json', formatversion=2, redirects=1))
    r = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
    d = json.load(urllib.request.urlopen(r, timeout=60))
    if 'error' in d: raise RuntimeError('ERR ' + d['error'].get('info', ''))
    return d['parse']['text']
def to_text(h):
    h = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', h, flags=re.S)
    h = re.sub(r'<br\s*/?>', '\n', h)
    h = re.sub(r'</(p|div|li|tr|h[1-6]|table)>', '\n', h)
    h = re.sub(r'<[^>]+>', '', h)
    t = html.unescape(h)
    return re.sub(r'\n{3,}', '\n\n', t).strip()
if __name__ == '__main__':
    h = fetch(sys.argv[1])
    print(h if '--html' in sys.argv else to_text(h))
