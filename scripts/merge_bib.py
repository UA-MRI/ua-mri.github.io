#!/usr/bin/env python3
"""
Merge two BibTeX files while removing duplicates based on title.
"""

import re
import sys
from typing import Dict, List, Set


def find_matching_brace(text: str, start_pos: int) -> int:
    """Find the matching closing brace for an opening brace."""
    depth = 0
    i = start_pos
    while i < len(text):
        if text[i] == '{':
            depth += 1
        elif text[i] == '}':
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return -1


def normalize_title(title: str) -> str:
    """
    Normalize a title for comparison by:
    - Converting to lowercase
    - Removing special characters and extra whitespace
    - Removing common LaTeX commands
    """
    if not title:
        return ""
    
    # Remove LaTeX commands like \scp, \&, etc.
    title = re.sub(r'\\[a-zA-Z]+\{([^}]*)\}', r'\1', title)
    title = re.sub(r'\\[a-zA-Z]+', '', title)
    
    # Remove special characters, keep only alphanumeric and spaces
    title = re.sub(r'[^a-zA-Z0-9\s]', '', title)
    
    # Normalize whitespace
    title = ' '.join(title.split())
    
    return title.lower().strip()


def extract_title(entry: str) -> str:
    """Extract title from a BibTeX entry."""
    # Find title field (case-insensitive)
    title_match = re.search(r'title\s*=\s*', entry, re.IGNORECASE)
    if not title_match:
        return ""
    
    title_start = title_match.end()
    
    # Check if it's a quoted string
    if title_start < len(entry) and entry[title_start] == '"':
        # Find closing quote
        quote_end = entry.find('"', title_start + 1)
        if quote_end != -1:
            return entry[title_start + 1:quote_end].strip()
    
    # Check if it's a braced string
    elif title_start < len(entry) and entry[title_start] == '{':
        brace_end = find_matching_brace(entry, title_start)
        if brace_end != -1:
            return entry[title_start + 1:brace_end].strip()
    
    # Otherwise, find until comma or newline (simple case)
    else:
        end_chars = [',', '\n', '}']
        title_end = len(entry)
        for char in end_chars:
            pos = entry.find(char, title_start)
            if pos != -1 and pos < title_end:
                title_end = pos
        return entry[title_start:title_end].strip()
    
    return ""


def parse_bibtex_entries(bib_content: str) -> List[Dict[str, str]]:
    """
    Parse BibTeX entries from a string.
    Returns a list of dictionaries with 'key', 'entry', and 'title' fields.
    """
    entries = []
    i = 0
    
    while i < len(bib_content):
        # Find next @ symbol
        at_pos = bib_content.find('@', i)
        if at_pos == -1:
            break
        
        # Find entry type
        type_end = at_pos + 1
        while type_end < len(bib_content) and (bib_content[type_end].isalnum() or bib_content[type_end] == '_'):
            type_end += 1
        
        if type_end == at_pos + 1:
            i = at_pos + 1
            continue
        
        entry_type = bib_content[at_pos + 1:type_end]
        
        # Skip whitespace and find opening brace
        brace_start = type_end
        while brace_start < len(bib_content) and bib_content[brace_start] in ' \t\n':
            brace_start += 1
        
        if brace_start >= len(bib_content) or bib_content[brace_start] != '{':
            i = type_end
            continue
        
        # Find entry key (until comma or closing brace)
        key_start = brace_start + 1
        key_end = key_start
        while key_end < len(bib_content) and bib_content[key_end] not in ',}':
            key_end += 1
        
        if key_end >= len(bib_content):
            i = brace_start + 1
            continue
        
        entry_key = bib_content[key_start:key_end].strip()
        
        # Find the matching closing brace for the entire entry
        entry_end = find_matching_brace(bib_content, brace_start)
        if entry_end == -1:
            i = key_end
            continue
        
        # Extract full entry
        full_entry = bib_content[at_pos:entry_end + 1]
        
        # Extract entry body (everything after the key)
        body_start = key_end
        if body_start < len(bib_content) and bib_content[body_start] == ',':
            body_start += 1
        entry_body = bib_content[body_start:entry_end].strip()
        
        # Extract title
        title = extract_title(entry_body)
        
        entries.append({
            'key': entry_key,
            'type': entry_type,
            'entry': full_entry,
            'title': title
        })
        
        i = entry_end + 1
    
    return entries


def merge_bib_files(file1_path: str, file2_path: str, output_path: str):
    """
    Merge two BibTeX files, removing duplicates based on normalized titles.
    """
    # Read both files
    try:
        with open(file1_path, 'r', encoding='utf-8') as f:
            content1 = f.read()
    except FileNotFoundError:
        print(f"Error: File '{file1_path}' not found.")
        sys.exit(1)
    
    try:
        with open(file2_path, 'r', encoding='utf-8') as f:
            content2 = f.read()
    except FileNotFoundError:
        print(f"Error: File '{file2_path}' not found.")
        sys.exit(1)
    
    # Parse entries from both files
    print(f"Parsing entries from {file1_path}...")
    entries1 = parse_bibtex_entries(content1)
    print(f"  Found {len(entries1)} entries")
    
    print(f"Parsing entries from {file2_path}...")
    entries2 = parse_bibtex_entries(content2)
    print(f"  Found {len(entries2)} entries")
    
    # Track seen titles (normalized)
    seen_titles: Set[str] = {}
    merged_entries: List[Dict[str, str]] = []
    duplicates: List[str] = []
    
    # Add entries from first file
    for entry in entries1:
        normalized_title = normalize_title(entry['title'])
        if normalized_title and normalized_title not in seen_titles:
            seen_titles[normalized_title] = entry['key']
            merged_entries.append(entry)
        elif normalized_title:
            duplicates.append(f"  - {entry['key']} (duplicate of {seen_titles[normalized_title]})")
    
    # Add entries from second file (skip duplicates)
    for entry in entries2:
        normalized_title = normalize_title(entry['title'])
        if normalized_title and normalized_title not in seen_titles:
            seen_titles[normalized_title] = entry['key']
            merged_entries.append(entry)
        elif normalized_title:
            duplicates.append(f"  - {entry['key']} (duplicate of {seen_titles[normalized_title]})")
    
    # Write merged entries to output file
    with open(output_path, 'w', encoding='utf-8') as f:
        for entry in merged_entries:
            f.write(entry['entry'])
            f.write('\n\n')
    
    print(f"\nMerged {len(merged_entries)} unique entries")
    if duplicates:
        print(f"\nSkipped {len(duplicates)} duplicate entries:")
        for dup in duplicates[:10]:  # Show first 10
            print(dup)
        if len(duplicates) > 10:
            print(f"  ... and {len(duplicates) - 10} more")
    print(f"\nOutput written to: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python merge_bib.py <file1.bib> <file2.bib> [output.bib]")
        print("\nExample:")
        print("  python merge_bib.py file1.bib file2.bib merged.bib")
        sys.exit(1)
    
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) > 3 else "merged.bib"
    
    merge_bib_files(file1, file2, output)

