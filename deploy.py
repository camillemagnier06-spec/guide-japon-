#!/usr/bin/env python3
"""
deploy.py — Pousse index.html + CONTEXTE_CLAUDE.md sur GitHub → Netlify redéploie automatiquement.

SETUP (une seule fois) :
  1. Va sur https://github.com/settings/tokens/new
  2. Donne un nom (ex: "japon-deploy"), durée 1 an
  3. Coche uniquement "repo" dans les permissions
  4. Clique "Generate token" et copie le token (commence par ghp_...)
  5. Remplace COLLE_TON_TOKEN_ICI ci-dessous par ton token

UTILISATION :
  python3 "/Users/magniercamille/Desktop/japon /deploy.py"
  Ou depuis Claude Code : ! python3 "/Users/magniercamille/Desktop/japon /deploy.py"
"""

import urllib.request
import urllib.error
import json
import base64
import os

# ══════════════════════════════════════════
# CONFIGURATION — À remplir une seule fois
# ══════════════════════════════════════════
GITHUB_TOKEN  = "COLLE_TON_TOKEN_ICI"   # remplacé automatiquement depuis token.txt
GITHUB_OWNER  = "camillemagnier06-spec"
GITHUB_REPO   = "quide-japon-"
GITHUB_BRANCH = "main"
# ══════════════════════════════════════════

FILES_TO_PUSH = [
    "index.html",
    "CONTEXTE_CLAUDE.md",
    "deploy.py",
]

def push_file(file_name, headers, script_dir):
    local_path = os.path.join(script_dir, file_name)

    if not os.path.exists(local_path):
        print(f"   ⚠️  {file_name} introuvable localement, ignoré.")
        return False

    with open(local_path, "r", encoding="utf-8") as f:
        content = f.read()
    content_b64 = base64.b64encode(content.encode("utf-8")).decode("utf-8")

    api_url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/contents/{file_name}"

    # Récupérer le SHA actuel (requis par l'API GitHub pour mettre à jour)
    req = urllib.request.Request(api_url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            current = json.loads(resp.read().decode("utf-8"))
            sha = current["sha"]
    except urllib.error.HTTPError as e:
        if e.code == 404:
            sha = None  # Nouveau fichier, pas de SHA
        else:
            print(f"   ❌ Erreur récupération {file_name} : {e.code} {e.reason}")
            if e.code == 401:
                print("      → Token invalide ou expiré.")
            return False

    payload = {"message": f"Update {file_name} via deploy.py", "content": content_b64, "branch": GITHUB_BRANCH}
    if sha:
        payload["sha"] = sha

    req = urllib.request.Request(
        api_url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="PUT"
    )
    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            commit_url = result["commit"]["html_url"]
        print(f"   ✓ {file_name} → {commit_url}")
        return True
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        print(f"   ❌ Erreur push {file_name} : {e.code} {e.reason} — {body[:200]}")
        return False


def load_token(script_dir):
    token_file = os.path.join(script_dir, "token.txt")
    if os.path.exists(token_file):
        with open(token_file) as f:
            t = f.read().strip()
        if t:
            return t
    if GITHUB_TOKEN != "COLLE_TON_TOKEN_ICI":
        return GITHUB_TOKEN
    return None

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    token = load_token(script_dir)

    if not token:
        print("❌ Token GitHub manquant.")
        print("   Crée un fichier token.txt dans ce dossier avec ton token GitHub (ghp_...).")
        print("   👉 https://github.com/settings/tokens/new  (coche 'repo')")
        return
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json",
    }

    print(f"📡 Connexion à GitHub ({GITHUB_OWNER}/{GITHUB_REPO})...")
    print()

    success = 0
    for file_name in FILES_TO_PUSH:
        print(f"⬆️  {file_name}...")
        if push_file(file_name, headers, script_dir):
            success += 1

    print()
    if success == len(FILES_TO_PUSH):
        print("✅ Tout déployé ! Netlify met à jour le site dans ~30 secondes.")
        print("   🌐 https://delicate-pasca-e5789f.netlify.app/")
        print()
        print("   📄 Pense aussi à mettre à jour le Google Doc contexte si tu as modifié CONTEXTE_CLAUDE.md :")
        print("   https://docs.google.com/document/d/1or44Ij_01MLsbZ_bX3nabJ3SqGheXjBg6JjbpSk325s/edit")
    else:
        print(f"⚠️  {success}/{len(FILES_TO_PUSH)} fichiers déployés. Vérifie les erreurs ci-dessus.")


if __name__ == "__main__":
    main()
