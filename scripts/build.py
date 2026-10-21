# Собирает index.html: упаковывает исходник приложения src/app.html в бандл.
# Остальное в index.html (загрузчик, React, шрифты, логотип) не меняется.
# Использование: python3 scripts/build.py
import json, pathlib, re

root = pathlib.Path(__file__).resolve().parent.parent
index = root / 'index.html'
app = (root / 'src' / 'app.html').read_text(encoding='utf-8')
html = index.read_text(encoding='utf-8')

m = re.search(r'<script type="__bundler/template">\s*(.*?)\s*</script>', html, re.S)
assert m, 'в index.html не найден блок __bundler/template'
# "</" экранируется, чтобы текст шаблона не закрыл окружающий <script>.
enc = json.dumps(app, ensure_ascii=False).replace('</', '<\\u002F')
html = html[:m.start(1)] + enc + html[m.end(1):]
index.write_text(html, encoding='utf-8')
print('index.html собран из src/app.html')
