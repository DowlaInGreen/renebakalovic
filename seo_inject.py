import json
import os
import re

with open('data/articles.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)

for article in articles:
    url_path = article['url']  # npr. skriveni-biseri/rakovice-za-znalce-i-pocetnike.html
    filepath = os.path.join(os.path.dirname(__file__), url_path)

    if not os.path.exists(filepath):
        print(f"PRESKAČEM (ne postoji): {filepath}")
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # Preskači ako je već injektirano
    if 'application/ld+json' in html:
        print(f"PRESKAČEM (već ima schema): {url_path}")
        continue

    # Određujemo depth za relativne pathove
    depth = url_path.count('/')
    prefix = '../' * depth

    full_url = f"https://renebakalovic.online/{url_path}"
    image_url = f"https://renebakalovic.online/{article['image']}"
    category_folder = url_path.split('/')[0]
    category_url = f"https://renebakalovic.online/{category_folder}/"

    if article['author'] == 'Vlado Stipan':
        author_id = "https://renebakalovic.online/#vlado"
        author_job = '"jobTitle": "F&B veteran & AI specialist",'
    else:
        author_id = "https://renebakalovic.online/#rene"
        author_job = ''

    schema = f"""<link rel="canonical" href="{full_url}">
<meta property="og:type" content="article">
<meta property="og:title" content="{article['title']} — Rene Bakalović">
<meta property="og:description" content="{article['excerpt']}">
<meta property="og:image" content="{image_url}">
<meta property="og:url" content="{full_url}">
<meta property="og:site_name" content="Rene Bakalović — Food. Drink. City.">
<meta property="og:locale" content="hr_HR">
<meta property="article:published_time" content="{article['date']}T00:00:00+02:00">
<meta property="article:author" content="{article['author']}">
<meta property="article:section" content="{article['categoryLabel']}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{article['title']} — Rene Bakalović">
<meta name="twitter:description" content="{article['excerpt']}">
<meta name="twitter:image" content="{image_url}">
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@graph": [
    {{
      "@type": "Article",
      "@id": "{full_url}#article",
      "headline": "{article['title']}",
      "description": "{article['excerpt']}",
      "image": {{
        "@type": "ImageObject",
        "url": "{image_url}",
        "width": 1200,
        "height": 630
      }},
      "datePublished": "{article['date']}T00:00:00+02:00",
      "dateModified": "{article['date']}T00:00:00+02:00",
      "author": {{
        "@type": "Person",
        "@id": "{author_id}",
        "name": "{article['author']}",
        {author_job}
        "url": "https://renebakalovic.online/"
      }},
      "publisher": {{
        "@id": "https://renebakalovic.online/#organization"
      }},
      "mainEntityOfPage": {{
        "@type": "WebPage",
        "@id": "{full_url}"
      }},
      "articleSection": "{article['categoryLabel']}",
      "inLanguage": "hr",
      "speakable": {{
        "@type": "SpeakableSpecification",
        "cssSelector": [".article-title", ".article-body p:first-of-type"]
      }}
    }},
    {{
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{
          "@type": "ListItem",
          "position": 1,
          "name": "Početna",
          "item": "https://renebakalovic.online/"
        }},
        {{
          "@type": "ListItem",
          "position": 2,
          "name": "{article['categoryLabel']}",
          "item": "{category_url}"
        }},
        {{
          "@type": "ListItem",
          "position": 3,
          "name": "{article['title']}",
          "item": "{full_url}"
        }}
      ]
    }}
  ]
}}
</script>"""

    # Ubaci prije </head>
    new_html = html.replace('</head>', schema + '\n</head>', 1)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_html)

    print(f"✅ DONE: {url_path}")

print("\nGotovo.")
