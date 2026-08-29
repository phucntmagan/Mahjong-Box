#!/usr/bin/env python3
"""Markdown -> HTML da dinh dang, dung chung CSS voi build/review.html.
Chay: python3 tools/md2html.py docs/X.md build/x.html "Tieu de" "dong meta 1" ...
Ho tro: # ## ###, doan van, bang, danh sach - va 1., ``` khoi ma, > trich dan,
        **dam** *nghieng* `ma`, ![chu thich](figs/x.png), --- ngat trang.
Chi du dung cho ho so nay — khong phai bo phan tich markdown day du."""
import html, os, re, sys

CSS = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..',
                        'build', 'review.html')).read()
CSS = CSS[CSS.index('<style>'):CSS.index('</style>')+8]

def inline(t):
    t = html.escape(t)
    t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
    t = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<i>\1</i>', t)
    t = t.replace('--&gt;', '&rarr;').replace('-&gt;', '&rarr;')
    return t

def cells(row):
    return [c.strip() for c in row.strip().strip('|').split('|')]

def convert(md):
    out, i, lines = [], 0, md.split('\n')
    while i < len(lines):
        ln = lines[i]
        if ln.startswith('```'):
            j = i+1
            buf = []
            while j < len(lines) and not lines[j].startswith('```'):
                buf.append(html.escape(lines[j])); j += 1
            out.append('<pre>' + '\n'.join(buf) + '</pre>'); i = j+1; continue
        m = re.match(r'^(#{1,4})\s+(.*)$', ln)
        if m:
            lv = len(m.group(1))
            out.append(f'<h{lv}>{inline(m.group(2))}</h{lv}>'); i += 1; continue
        if re.match(r'^!\[', ln):
            m = re.match(r'^!\[(.*?)\]\((.*?)\)\s*$', ln)
            if m:
                out.append(f'<figure><img src="../{m.group(2)}" style="width:100%">'
                           f'<figcaption>{inline(m.group(1))}</figcaption></figure>')
                i += 1; continue
        if ln.strip() in ('---', '***'):
            out.append('<div class="pb"></div>'); i += 1; continue
        if ln.startswith('|') and i+1 < len(lines) and re.match(r'^\|[\s:|-]+\|?$', lines[i+1]):
            hdr = cells(ln)
            align = ['n' if s.strip().endswith(':') and s.strip().startswith('-') is False
                     else ('n' if s.strip().endswith(':') else '') for s in cells(lines[i+1])]
            j, rows = i+2, []
            while j < len(lines) and lines[j].startswith('|'):
                rows.append(cells(lines[j])); j += 1
            # bang khong co tieu de (| | |) thi bo hang tieu de di
            t = ['<table>']
            if any(c.strip() for c in hdr):
                t += ['<tr>'] + [f'<th class="{a}">{inline(c)}</th>'
                                 for c, a in zip(hdr, align)] + ['</tr>']
            for r in rows:
                t.append('<tr>' + ''.join(f'<td class="{a}">{inline(c)}</td>'
                                          for c, a in zip(r, align + ['']*9)) + '</tr>')
            t.append('</table>')
            out.append(''.join(t)); i = j; continue
        if re.match(r'^\s*[-*]\s+', ln) or re.match(r'^\s*\d+\.\s+', ln):
            ordered = bool(re.match(r'^\s*\d+\.\s+', ln))
            tagn = 'ol' if ordered else 'ul'
            items, j = [], i
            while j < len(lines):
                if re.match(r'^\s*[-*]\s+', lines[j]) or re.match(r'^\s*\d+\.\s+', lines[j]):
                    items.append(re.sub(r'^\s*(?:[-*]|\d+\.)\s+', '', lines[j]))
                elif items and lines[j].strip() and not re.match(
                        r'^(#{1,4}\s|\||```|>|!\[|---$)', lines[j]):
                    items[-1] += ' ' + lines[j].strip()   # dong xuong dong cua cung mot muc
                else:
                    break
                j += 1
            out.append(f'<{tagn}>' + ''.join(f'<li>{inline(x)}</li>' for x in items)
                       + f'</{tagn}>'); i = j; continue
        if ln.startswith('>'):
            buf, j = [], i
            while j < len(lines) and lines[j].startswith('>'):
                buf.append(lines[j].lstrip('> ')); j += 1
            out.append('<div class="warn">' + inline(' '.join(buf)) + '</div>')
            i = j; continue
        if ln.strip() == '':
            i += 1; continue
        buf, j = [], i
        while j < len(lines) and lines[j].strip() and not re.match(
                r'^(#{1,4}\s|\||```|>|!\[|\s*[-*]\s|\s*\d+\.\s|---$)', lines[j]):
            buf.append(lines[j]); j += 1
        out.append('<p>' + inline(' '.join(buf)) + '</p>'); i = j
    return '\n'.join(out)

if __name__ == '__main__':
    src, dst, title, *meta = sys.argv[1:]
    md = open(src, encoding='utf-8').read()
    body = convert(md)
    # meta do build_pdf.sh truyen vao, la HTML tin cay -> khong escape
    head = (f'<div class="head"><h1>{html.escape(title)}</h1><div class="meta">'
            + '<br>'.join(meta) + '</div></div>')
    foot = (f'<div class="foot">Sinh tu <code>{html.escape(src)}</code> bang '
            f'<code>tools/md2html.py</code>. Moi tri so sinh tu '
            f'<code>tools/box_spec.py</code>.</div>')
    open(dst, 'w', encoding='utf-8').write(
        f'<!doctype html>\n<html lang="vi"><head><meta charset="utf-8">\n'
        f'<title>{html.escape(title)}</title>\n{CSS}</head><body>\n'
        f'{head}\n{body}\n{foot}\n</body></html>\n')
    print(f'  {dst}')
