#!/usr/bin/env python3

"""
Generate papers.bib from two ORCID profiles.
Uses CrossRef to fetch clean BibTeX entries.
Automatically removes duplicates using DOI.
Requires: pip install requests
"""

import requests
import time

# ---------------------------------------------------------
# ENTER YOUR ORCID IDs HERE
# Example: "0000-0002-1825-0097"
# ---------------------------------------------------------
ORCID_IDS = [
    "0000-0003-4196-4036",
    "0000-0001-9368-2458"
]

OUTPUT_FILE = "_bibliography/papers.bib"


def get_orcid_works(orcid):
    """Fetch all works (publications) from ORCID."""
    print(f"\n→ Fetching ORCID works for {orcid}")

    url = f"https://pub.orcid.org/v3.0/{orcid}/works"
    headers = {"Accept": "application/json"}

    r = requests.get(url, headers=headers)
    data = r.json()

    works = data.get("group", [])
    dois = []

    for work in works:
        try:
            summary = work["work-summary"][0]
            ext_ids = summary.get("external-ids", {}).get("external-id", [])

            for ext in ext_ids:
                if ext["external-id-type"].lower() == "doi":
                    doi = ext["external-id-value"]
                    dois.append(doi)
        except Exception:
            continue

    print(f"   Found {len(dois)} DOIs")
    return dois


def fetch_bibtex_from_doi(doi):
    """Fetch BibTeX from CrossRef using DOI."""
    url = f"https://api.crossref.org/works/{doi}/transform/application/x-bibtex"
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.text.strip()
    except:
        return None
    return None


def main():
    all_dois = set()

    # Collect DOIs from both authors
    for orcid in ORCID_IDS:
        dois = get_orcid_works(orcid)
        all_dois.update([d.lower() for d in dois])  # normalize

    print(f"\nTotal unique DOIs: {len(all_dois)}\n")

    bib_entries = []

    for doi in sorted(all_dois):
        print(f" → Fetching BibTeX: {doi}")
        bib = fetch_bibtex_from_doi(doi)
        if bib:
            bib_entries.append(bib)
        time.sleep(0.2)  # be polite to CrossRef

    # Save
    with open(OUTPUT_FILE, "w") as f:
        for entry in bib_entries:
            f.write(entry + "\n\n")

    print(f"\n✅ Done! Saved {len(bib_entries)} publications to {OUTPUT_FILE}\n")


if __name__ == "__main__":
    main()
