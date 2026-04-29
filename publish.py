#!/usr/bin/env python3
"""
publish.py — Rene Bakalović · auto deploy helper
Čita HTML i JSON entry s Desktopa, pusha na GitHub.

Uso:
  python3 publish.py

Prije pokretanja postavi env varijablu:
  export GITHUB_TOKEN="ghp_tvoj_novi_token"
"""

import os, sys, base64, json, requests
from pathlib import Path

# ── CONFIG ────────────────────────────────────────────────────────────────────
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_USER  = "DowlaInGreen"
GITHUB_REPO  = "renebakalovic"
DESKTOP      = Path("/Users/vladostipan/Desktop")
ARTICLES_JSON_PATH = "data/articles.json"
# ─────────────────────────────────────────────────────────────────────────────

def check_token():
    if not GITHUB_TOKEN:
        print("❌ GITHUB_TOKEN nije postavljen.")
        print("   Pokreni: export GITHUB_TOKEN='ghp_tvoj_token'")
        sys.exit(1)

def get_headers():
    return {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

def github_get(path):
    url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents/{path}"
    r = requests.get(url, headers=get_headers())
    return r

def github_put(path, content_bytes, commit_message, sha=None):
    url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents/{path}"
    payload = {
        "message": commit_message,
        "content": base64.b64encode(content_bytes).decode("utf-8"),
    }
    if sha:
        payload["sha"] = sha
    r = requests.put(url, headers=get_headers(), json=payload)
    return r

def upload_file(local_path: Path, repo_path: str, commit_message: str):
    print(f"→ Upload: {repo_path}")
    content_bytes = local_path.read_bytes()

    # Dohvati SHA ako fajl već postoji
    sha = None
    r = github_get(repo_path)
    if r.status_code == 200:
        sha = r.json().get("sha")

    r = github_put(repo_path, content_bytes, commit_message, sha)
    if r.status_code in (200, 201):
        print(f"  ✅ OK")
        return True
    else:
        print(f"  ❌ Greška {r.status_code}: {r.json().get('message')}")
        return False

def update_articles_json(new_entry: dict):
    print(f"→ Ažuriranje articles.json")

    r = github_get(ARTICLES_JSON_PATH)
    if r.status_code != 200:
        print(f"  ❌ Ne mogu dohvatiti articles.json: {r.status_code}")
        return False

    data = r.json()
    sha = data["sha"]
    existing = json.loads(base64.b64decode(data["content"]).decode("utf-8"))

    # Provjeri duplikat
    ids = [e["id"] for e in existing]
    if new_entry["id"] in ids:
        print(f"  ⚠️  Entry '{new_entry['id']}' već postoji u articles.json — preskačem.")
        return True

    # Novi entry na vrh
    updated = [new_entry] + existing
    updated_bytes = json.dumps(updated, ensure_ascii=False, indent=2).encode("utf-8")

    r = github_put(
        ARTICLES_JSON_PATH,
        updated_bytes,
        f"JSON: dodaj {new_entry['id']}",
        sha
    )
    if r.status_code in (200, 201):
        print(f"  ✅ articles.json ažuriran")
        return True
    else:
        print(f"  ❌ Greška {r.status_code}: {r.json().get('message')}")
        return False

def main():
    check_token()

    # ── UNESI PODATKE ─────────────────────────────────────────────────────────
    print("\n── RENE BAKALOVIĆ · PUBLISH ──────────────────────────────")
    html_filename  = input("HTML fajl (npr. mv-naziv.html):          ").strip()
    image_filename = input("Slika (npr. mv-naziv.png):               ").strip()
    folder         = input("Folder u repou (npr. millennial-view):   ").strip()
    article_id     = input("ID članka (npr. mv-naziv):               ").strip()
    title          = input("Naslov:                                  ").strip()
    excerpt        = input("Excerpt (2-3 rečenice):                  ").strip()
    category       = input("category value (npr. millennial-view):   ").strip()
    category_label = input("categoryLabel (npr. Millennial View):    ").strip()
    author         = input("Autor:                                   ").strip()
    date_iso       = input("Datum ISO (npr. 2026-04-29):             ").strip()
    date_label     = input("Datum label (npr. 29. travnja 2026.):    ").strip()
    # ─────────────────────────────────────────────────────────────────────────

    html_local  = DESKTOP / html_filename
    image_local = DESKTOP / image_filename

    # Provjera fajlova
    for f in [html_local, image_local]:
        if not f.exists():
            print(f"❌ Fajl ne postoji: {f}")
            sys.exit(1)

    repo_html  = f"{folder}/{html_filename}"
    repo_image = f"images/{image_filename}"
    commit_msg = f"Dodaj: {title}"

    print()

    # Upload HTML
    upload_file(html_local, repo_html, commit_msg)

    # Upload slika
    upload_file(image_local, repo_image, commit_msg)

    # JSON entry
    new_entry = {
        "id": article_id,
        "title": title,
        "excerpt": excerpt,
        "category": category,
        "categoryLabel": category_label,
        "author": author,
        "date": date_iso,
        "dateLabel": date_label,
        "image": f"images/{image_filename}",
        "url": f"{folder}/{html_filename}"
    }
    update_articles_json(new_entry)

    print(f"\n🚀 Deploy završen → https://www.renebakalovic.online/{folder}/{html_filename}\n")

if __name__ == "__main__":
    main()
