# Собирает index.html из экспорта (бандла) Claude: добавляет заголовок вкладки,
# иконку и мета-теги во внешнюю страницу-загрузчик и во внутренний шаблон.
# Использование: python3 scripts/build.py BURAQ_KP_Platforma.html index.html
import sys, json, re
src, dst = sys.argv[1], sys.argv[2]
html = open(src, encoding='utf-8').read()

TITLE = 'BURAQ — Платформа КП'
DESC = 'BURAQ Logistics: заявки на груз и согласование коммерческих предложений (KP)'
ICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E"
        "%3Crect width='64' height='64' rx='14' fill='%230E2E54'/%3E"
        "%3Cpath d='M14 34h34M40 26l9 8-9 8' stroke='%23DE0441' stroke-width='5' fill='none' "
        "stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E")
head_tags = (f'<title>{TITLE}</title>\n'
             f'<meta name="description" content="{DESC}">\n'
             f'<meta name="robots" content="noindex, nofollow">\n'
             f'<meta name="theme-color" content="#0E2E54">\n'
             f'<link rel="icon" href="{ICON}">')

# 1) Outer loader page: shown while the bundle unpacks.
old = '<title>Bundled Page</title>'
assert html.count(old) == 1
html = html.replace(old, head_tags.replace('\n', '\n  '))

# 2) Inner template: replaces the whole document after unpacking, so it needs
#    its own <title>/icon. Edit the JSON-encoded string in place; "</" must
#    stay escaped so it cannot close the surrounding <script> tag.
anchor = '<html><head>\\n<meta charset=\\"utf-8\\">'
assert html.count(anchor) == 1
inj = json.dumps('\n' + head_tags, ensure_ascii=False)[1:-1].replace('</', '<\\u002F')
html = html.replace(anchor, anchor + inj)

open(dst, 'w', encoding='utf-8').write(html)

# Sanity: template still parses and contains the title.
t = json.loads(re.search(r'<script type="__bundler/template">\s*(.*?)\s*</script>', html, re.S).group(1))
assert f'<title>{TITLE}</title>' in t and t.count('<title>') == 1
print('ok', len(html))
