#!/usr/bin/env python3
"""
One-shot script: apply newspaper redesign to all article HTML files.
Run from ~/Desktop/renebakalovic/
"""
import os, re
from pathlib import Path

BASE = Path(__file__).parent

NEW_FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '  <link href="https://fonts.googleapis.com/css2?family=UnifrakturMaguntia&family=IM+Fell+English:ital@0;1&family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Libre+Baskerville:ital@0;1&family=Bebas+Neue&family=DM+Sans:wght@400;500&display=swap" rel="stylesheet">\n'
    '  <link rel="stylesheet" href="../style.css">'
)

HEADER = '''\
<header class="site-header">
  <div class="masthead-meta">
    <span>Zagreb, četvrtak 7. svibnja 2026.</span>
    <span>Urbano novinarstvo o hrani, piću i gradu</span>
    <span>renebakalovic.online</span>
  </div>
  <div class="masthead-title-wrap">
    <img src="../logo-full.png" class="logo-full" alt="Rene Bakalović — Food. Drink. City.">
    <div class="masthead-tagline">— online magazin —</div>
  </div>
  <div class="masthead-rules"></div>
  <nav class="site-nav">
    <ul>
      <li><a href="../index.html">Feed</a></li>
      <li class="nav-breaking"><a href="../index.html#breaking">Breaking</a></li>
      <li><a href="../index.html#skriveni-biseri">Skriveni biseri</a></li>
      <li><a href="../index.html#ispod-10-eura">Ispod 10€</a></li>
      <li><a href="../index.html#samo-kod-nas">Samo kod nas</a></li>
      <li class="nav-mv"><a href="../index.html#millennial-view">Millennial View</a></li>
      <li><a href="../index.html#newsletter">Newsletter</a></li>
      <li><a href="../about.html">O nama</a></li>
    </ul>
  </nav>
</header>'''

FOOTER = '''\
<footer class="site-footer">
  <div class="footer-inner">
    <div class="footer-brand">
      <span class="footer-logo">Rene Bakalović</span>
      <p>Online magazin o hrani,<br>piću i gradu.</p>
      <div style="margin-top: 12px; font-family: var(--font-label); font-size: 10px; letter-spacing: 3px; color: var(--ink-muted);">FOOD · DRINK · CITY</div>
    </div>
    <div class="footer-col">
      <h4>Sekcije</h4>
      <ul>
        <li><a href="../index.html#breaking">Breaking</a></li>
        <li><a href="../index.html#skriveni-biseri">Skriveni biseri</a></li>
        <li><a href="../index.html#ispod-10-eura">Ispod 10€</a></li>
        <li><a href="../index.html#samo-kod-nas">Samo kod nas</a></li>
        <li><a href="../index.html#millennial-view" style="color: var(--mv-blue);">Millennial View</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h4>Brend</h4>
      <ul>
        <li><a href="../about.html">O nama</a></li>
        <li><a href="#">Oglašavanje</a></li>
        <li><a href="#">Kontakt</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h4>Prati</h4>
      <ul>
        <li><a href="#">Instagram</a></li>
        <li><a href="#">TikTok</a></li>
        <li><a href="../index.html#newsletter">Newsletter</a></li>
      </ul>
    </div>
  </div>
  <div class="footer-bottom">
    <span>© 2026 Rene Bakalović. Sva prava pridržana.</span>
    <span style="font-family: var(--font-label); letter-spacing: 2px;">FOOD · DRINK · CITY</span>
  </div>
</footer>'''


def replace_fonts(content):
    # Match either single or double preconnect + google fonts stylesheet line
    return re.sub(
        r'<link rel="preconnect" href="https://fonts\.googleapis\.com"[^>]*>.*?<link href="https://fonts\.googleapis\.com[^"]*" rel="stylesheet"[^>]*>',
        NEW_FONTS,
        content, flags=re.DOTALL
    )

def remove_style_block(content):
    return re.sub(r'\n?  <style>.*?</style>', '', content, flags=re.DOTALL)

def replace_footer(content):
    return re.sub(r'<footer[\s\S]*?</footer>', FOOTER, content, flags=re.DOTALL)


# ── RENE ARTICLES ────────────────────────────────────────────
RENE_DIRS = ['skriveni-biseri', 'ispod-10-eura', 'samo-kod-nas']

def process_rene(path):
    c = path.read_text(encoding='utf-8')
    c = replace_fonts(c)
    c = remove_style_block(c)
    # Replace topnav
    c = re.sub(r'<nav class="topnav">.*?</nav>', HEADER, c, flags=re.DOTALL)
    # Remove mobile nav
    c = re.sub(r'\n?<nav class="mobile-nav">.*?</nav>', '', c, flags=re.DOTALL)
    # Add article-page class to article-wrap
    c = c.replace('class="article-wrap"', 'class="article-wrap article-page"')
    c = replace_footer(c)
    path.write_text(c, encoding='utf-8')
    print(f"  Rene: {path.relative_to(BASE)}")


# ── MV ARTICLES ──────────────────────────────────────────────
def process_mv(path):
    c = path.read_text(encoding='utf-8')
    c = replace_fonts(c)
    c = remove_style_block(c)
    # Replace dark nav (starts with <nav\n or <nav ) — no class on MV nav
    c = re.sub(r'<nav>\n.*?</nav>', HEADER, c, flags=re.DOTALL)
    # Add mv-article class to main.article-wrap
    c = re.sub(
        r'class="article-wrap"',
        'class="article-wrap article-page mv-article"',
        c
    )
    c = replace_footer(c)
    path.write_text(c, encoding='utf-8')
    print(f"  MV:   {path.relative_to(BASE)}")


if __name__ == '__main__':
    print("Applying newspaper redesign to article files...")

    for d in RENE_DIRS:
        for html in (BASE / d).glob('*.html'):
            process_rene(html)

    for html in (BASE / 'millennial-view').glob('*.html'):
        process_mv(html)

    print("Done.")
