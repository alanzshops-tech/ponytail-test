#!/usr/bin/env python3
"""
bestandsautomatik.py — setzt ausverkaufte Produkte automatisch auf
Entwurf und wieder verfügbare zurück auf aktiv.

Regel, wie vom Nutzer festgelegt (14.08.2026):
  - Eine Variante bei 0 Bestand, andere noch da  -> nichts tun
  - ALLE Varianten bei 0 Bestand                  -> Entwurf
  - Ein Entwurf hat wieder Bestand                 -> aktiv

Absichtliche Abweichung vom wörtlichen Wortlaut, aus Vorsicht: "Entwurf
hat Bestand -> aktiv" wird hier nur auf Entwürfe angewendet, die DIESES
Skript selbst wegen Ausverkauf erzeugt hat (erkennbar am Tag
"auto-draft-ausverkauft"). Der Shop hat laut AUDIT.md 45 weitere
Entwürfe aus anderen Gründen (nie fertig geworden, absichtlich
unvollständig) -- die blind zu reaktivieren, nur weil zufällig Bestand
auf einer Variante liegt, würde ungeprüfte Produkte live schalten. Das
wäre kein Sicherheitsnetz mehr, sondern ein neues Risiko.

Braucht ein Shopify-Admin-API-Zugriffstoken mit den Scopes
read_products, write_products, read_inventory -- siehe README_SETUP.md
für die Einrichtung. Kein Shopify-CLI-Theme-Token (das ist etwas
anderes).

Aufruf:
    python3 scripts/bestandsautomatik.py --store 7a0a31.myshopify.com
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import date
from pathlib import Path

API_VERSION = "2026-07"
TAG_AUTO_DRAFT = "auto-draft-ausverkauft"


def graphql(store: str, token: str, query: str, variables: dict | None = None) -> dict:
    import requests

    url = f"https://{store}/admin/api/{API_VERSION}/graphql.json"
    headers = {"X-Shopify-Access-Token": token, "Content-Type": "application/json"}
    for versuch in range(3):
        antwort = requests.post(
            url, headers=headers,
            json={"query": query, "variables": variables or {}}, timeout=30)
        if antwort.status_code == 429:
            time.sleep(2 * (versuch + 1))
            continue
        antwort.raise_for_status()
        d = antwort.json()
        if "errors" in d:
            raise RuntimeError(f"GraphQL-Fehler: {d['errors']}")
        return d["data"]
    raise RuntimeError("Dreimal Rate-Limit (429), abgebrochen.")


PRODUKTE_ABFRAGEN = """
query Produkte($cursor: String, $query: String!) {
  products(first: 100, after: $cursor, query: $query) {
    edges {
      cursor
      node {
        id
        title
        status
        tags
        variants(first: 100) {
          edges { node { inventoryQuantity } }
        }
      }
    }
    pageInfo { hasNextPage }
  }
}
"""


def alle_produkte(store: str, token: str, status_query: str) -> list[dict]:
    ergebnis = []
    cursor = None
    while True:
        daten = graphql(store, token, PRODUKTE_ABFRAGEN,
                        {"cursor": cursor, "query": status_query})
        kante = daten["products"]["edges"]
        for e in kante:
            n = e["node"]
            bestaende = [v["node"]["inventoryQuantity"]
                        for v in n["variants"]["edges"]]
            ergebnis.append({
                "id": n["id"], "title": n["title"], "status": n["status"],
                "tags": n["tags"], "bestaende": bestaende,
            })
        if not daten["products"]["pageInfo"]["hasNextPage"] or not kante:
            break
        cursor = kante[-1]["cursor"]
    return ergebnis


def produkt_update(store: str, token: str, product_id: str, status: str) -> None:
    mutation = """
    mutation($input: ProductInput!) {
      productUpdate(input: $input) {
        userErrors { field message }
      }
    }
    """
    d = graphql(store, token, mutation, {"input": {"id": product_id, "status": status}})
    fehler = d["productUpdate"]["userErrors"]
    if fehler:
        raise RuntimeError(f"productUpdate-Fehler für {product_id}: {fehler}")


def tags_aendern(store: str, token: str, product_id: str,
                  hinzu: list[str], weg: list[str]) -> None:
    if hinzu:
        d = graphql(store, token,
            "mutation($id: ID!, $tags: [String!]!) { tagsAdd(id: $id, tags: $tags) { userErrors { field message } } }",
            {"id": product_id, "tags": hinzu})
        fehler = d["tagsAdd"]["userErrors"]
        if fehler:
            raise RuntimeError(f"tagsAdd-Fehler für {product_id}: {fehler}")
    if weg:
        d = graphql(store, token,
            "mutation($id: ID!, $tags: [String!]!) { tagsRemove(id: $id, tags: $tags) { userErrors { field message } } }",
            {"id": product_id, "tags": weg})
        fehler = d["tagsRemove"]["userErrors"]
        if fehler:
            raise RuntimeError(f"tagsRemove-Fehler für {product_id}: {fehler}")


def entscheiden(aktive: list[dict], entwuerfe: list[dict]) -> tuple[list[dict], list[dict]]:
    """Reine Entscheidungslogik, ohne Netzwerk -- deshalb einzeln testbar."""
    zu_entwurf = [p for p in aktive
                  if p["bestaende"] and all(b <= 0 for b in p["bestaende"])]
    zu_aktiv = [p for p in entwuerfe
               if TAG_AUTO_DRAFT in p["tags"] and any(b > 0 for b in p["bestaende"])]
    return zu_entwurf, zu_aktiv


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--store", default="7a0a31.myshopify.com")
    a = ap.parse_args()

    token = os.environ.get("SHOPIFY_ADMIN_API_TOKEN", "").strip()
    if not token:
        print("SHOPIFY_ADMIN_API_TOKEN fehlt -- siehe README_SETUP.md für die "
              "Einrichtung eines Admin-API-Zugriffstokens mit den Scopes "
              "read_products, write_products, read_inventory.")
        Path("BESTANDSAUTOMATIK.md").write_text(
            "# Bestandsautomatik\n\nKein Zugang eingerichtet "
            "(SHOPIFY_ADMIN_API_TOKEN fehlt). Nichts geprüft.\n",
            encoding="utf-8")
        return

    aktive = alle_produkte(a.store, token, "status:active")
    entwuerfe = alle_produkte(a.store, token, "status:draft")

    zu_entwurf, zu_aktiv = entscheiden(aktive, entwuerfe)

    fehler_liste = []
    for p in zu_entwurf:
        try:
            produkt_update(a.store, token, p["id"], "DRAFT")
            tags_aendern(a.store, token, p["id"], [TAG_AUTO_DRAFT], [])
        except RuntimeError as e:
            fehler_liste.append(f"{p['title']}: {e}")

    for p in zu_aktiv:
        try:
            produkt_update(a.store, token, p["id"], "ACTIVE")
            tags_aendern(a.store, token, p["id"], [], [TAG_AUTO_DRAFT])
        except RuntimeError as e:
            fehler_liste.append(f"{p['title']}: {e}")

    z = ["# Bestandsautomatik", "", f"Stand: {date.today()}", "",
         f"{len(aktive)} aktive Produkte geprüft, {len(entwuerfe)} Entwürfe "
         f"(davon {sum(1 for p in entwuerfe if TAG_AUTO_DRAFT in p['tags'])} "
         f"von dieser Automatik verwaltet).", ""]

    if zu_entwurf:
        z += ["## Neu auf Entwurf gesetzt (alle Varianten bei 0)", ""]
        z += [f"- {p['title']}" for p in zu_entwurf]
        z.append("")
    else:
        z += ["Kein Produkt musste heute auf Entwurf gesetzt werden.", ""]

    if zu_aktiv:
        z += ["## Wieder aktiv (Bestand ist zurück)", ""]
        z += [f"- {p['title']}" for p in zu_aktiv]
        z.append("")
    else:
        z += ["Kein Entwurf hatte wieder Bestand.", ""]

    if fehler_liste:
        z += ["## Fehler", ""]
        z += [f"- {f}" for f in fehler_liste]
        z.append("")

    Path("BESTANDSAUTOMATIK.md").write_text("\n".join(z) + "\n", encoding="utf-8")
    Path("daten").mkdir(exist_ok=True)
    Path("daten/bestandsautomatik-aktuell.json").write_text(
        json.dumps({"stand": str(date.today()),
                    "zu_entwurf": [p["title"] for p in zu_entwurf],
                    "zu_aktiv": [p["title"] for p in zu_aktiv],
                    "fehler": fehler_liste}, ensure_ascii=False, indent=2),
        encoding="utf-8")

    print(f"{len(zu_entwurf)} auf Entwurf, {len(zu_aktiv)} auf aktiv, "
          f"{len(fehler_liste)} Fehler.")
    if fehler_liste:
        sys.exit(1)


if __name__ == "__main__":
    main()
