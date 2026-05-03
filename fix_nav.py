import os
import re

# Svi folderi s člancima
folders = [
    'skriveni-biseri',
    'ispod-10-eura', 
    'samo-kod-nas',
    'millennial-view',
    'breaking-news',
    'nova-otvorenja',
    'street-food',
    'fine-dining'
]

new_desktop_nav = '''    <ul class="nav-links">
      <li><a href="../index.html">← Feed</a></li>
      <li><a href="../about.html">O nama</a></li>
    </ul>'''

new_mobile_nav = '''  <div class="mobile-nav-inner">
    <a href="../index.html" class="mobile-nav-item active">
      <img src="../RBlogo.png" alt="RB">
      <span>Feed</span>
    </a>
    <a href="../about.html" class="mobile-nav-item">
      <svg viewBox="0 0 24 24"><circle cx="12" cy="7" r="4"/><path d="M5 21v-2a7 7 0 0 1 14 0v2"/></svg>
      <span>O nama</span>
    </a>
  </div>'''

processed = 0

for folder in folders:
    folder_path = os.path.join(os.path.dirname(__file__), folder)
    if not os.path.exists(folder_path):
        continue
    for filename in os.listdir(folder_path):
        if not filename.endswith('.html'):
            continue
        filepath = os.path.join(folder_path, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()

        # Desktop nav — zamijeni sve između <ul class="nav-links"> i </ul>
        html = re.sub(
            r'<ul class="nav-links">.*?</ul>',
            new_desktop_nav,
            html,
            flags=re.DOTALL
        )

        # Mobile nav — zamijeni sve između <div class="mobile-nav-inner"> i </div>
        html = re.sub(
            r'<div class="mobile-nav-inner">.*?</div>',
            new_mobile_nav,
            html,
            flags=re.DOTALL
        )

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"✅ {folder}/{filename}")
        processed += 1

print(f"\nGotovo — {processed} fajlova ažurirano.")
