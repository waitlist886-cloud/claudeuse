# -*- coding: utf-8 -*-
"""批量抓页：python3 fetch_list.py <清单文件> <输出目录> [--from=剧情内容]"""
import sys, os, time
sys.path.insert(0, os.path.dirname(__file__)); from bwiki import fetch, to_text
lst, outd = sys.argv[1], sys.argv[2]; cut = next((a[7:] for a in sys.argv if a.startswith('--from=')), None)
os.makedirs(outd, exist_ok=True); fails = []
for i, name in enumerate([l.strip() for l in open(lst, encoding='utf-8') if l.strip()], 1):
    fn = os.path.join(outd, f'{i:02d}_{name.replace("/", "／")}.txt')
    if os.path.exists(fn): continue
    try:
        t = to_text(fetch(name))
        if cut and (cut + '[编辑]') in t: t = t[t.index(cut + '[编辑]'):]
        open(fn, 'w', encoding='utf-8').write(t); print('ok', i, name, len(t))
    except Exception as e:
        print('FAIL', i, name, e); fails.append(name)
    time.sleep(float(os.environ.get("SLP","2.5")))
print('fails:', fails)
