#!/usr/bin/env python3
"""Offline researcher workspace scaffolding, metadata ingest and evidence stage triage.

Never verifies researcher identity, bibliographic correctness or scientific claims.
No network, no arbitrary code loading, no external process execution.
"""
import argparse
import csv
import hashlib
import json
import re
import sys
from pathlib import Path

from audit import fresh, clean_slug, validate, report, derived_paper_stage, derived_code_stage, derived_run_stage

REPO = Path(__file__).resolve().parents[1]


def normalize(text):
    return re.sub(r'[^a-z0-9]+', '', (text or '').casefold())


def record_key(row):
    doi = (row.get('doi') or '').strip().lower()
    doi = re.sub(r'^(?:https?://(?:dx\.)?doi\.org/|doi:)', '', doi)
    if doi and doi.startswith('10.'):
        return 'doi:' + doi
    arxiv = (row.get('arxiv_id') or '').strip().lower().replace('arxiv:', '')
    arxiv = re.sub(r'v\d+$', '', arxiv)
    if arxiv:
        return 'arxiv:' + arxiv
    return 'title:' + hashlib.sha1((normalize(row.get('title')) + ':' + str(row.get('year', ''))).encode()).hexdigest()[:16]


def load(path):
    d = json.loads(Path(path).read_text(encoding='utf-8'))
    errors = validate(d)
    if errors:
        raise ValueError('Cannot modify invalid researcher ledger: ' + '; '.join(errors))
    return d


def write(path, data):
    p = Path(path)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def make_workspace(root_path, name, slug):
    clean_slug(slug)
    workspace_root = Path(root_path).expanduser().resolve()
    if workspace_root == REPO or REPO in workspace_root.parents:
        raise ValueError('Private workspace must be outside the public Skill repository.')
    folder = workspace_root / slug
    if folder.exists():
        raise FileExistsError(f'Workspace already exists: {folder}')
    folder.mkdir(parents=True)
    write(folder / 'researcher.json', fresh(name, slug))
    (folder / 'notes').mkdir()
    (folder / 'code-audits').mkdir()
    (folder / 'pilot-logs').mkdir()
    (folder / 'README.md').write_text(
        '# Private researcher workspace\n\nThese records are **unverified until reviewed**. '
        'Do not publish this folder without checking for private research material.\n',
        encoding='utf-8')
    return folder


def import_csv(data, input_file, source_name):
    if not source_name.strip():
        raise ValueError('Source name required for provenance')
    existing = {p['canonical_id'] for p in data['papers'] if isinstance(p, dict) and 'canonical_id' in p}
    inserted = 0
    duplicates = 0
    skipped = []
    with open(input_file, 'r', encoding='utf-8-sig', newline='') as fh:
        rows = csv.DictReader(fh)
        needed = {'title', 'year'}
        if not needed.issubset(set(rows.fieldnames or [])):
            raise ValueError('CSV requires title and year headers')
        for row_num, row in enumerate(rows, start=2):
            title = (row.get('title') or '').strip()
            year_text = (row.get('year') or '').strip()
            try:
                year = int(year_text)
            except ValueError:
                year = 0
            if not title or not (1850 <= year <= 2100):
                skipped.append(f'line {row_num}: missing title or invalid year')
                continue
            url = (row.get('url') or '').strip()
            doi = (row.get('doi') or '').strip()
            arxiv = (row.get('arxiv_id') or '').strip()
            if not url and doi:
                url = 'https://doi.org/' + re.sub(
                    r'^(?:doi:|https?://(?:dx\.)?doi\.org/)', '', doi, flags=re.I)
            if not url and arxiv:
                url = 'https://arxiv.org/abs/' + arxiv.replace('arXiv:', '')
            if not url.startswith(('https://', 'http://')):
                skipped.append(f'line {row_num}: no resolvable URL')
                continue
            ident = record_key(row)
            if ident in existing:
                duplicates += 1
                continue
            data['papers'].append({
                'canonical_id': ident, 'title': title, 'year': year, 'url': url,
                'doi': doi, 'arxiv_id': arxiv,
                'authors_raw': (row.get('authors') or '').strip(),
                'venue': (row.get('venue') or '').strip(),
                'candidate_origin': source_name,
                'author_identity_verified': False,
                'abstract_checked': False,
                'claimed_stage': 'metadata_only',
                'notes': 'Imported bibliography metadata only; confirm authorship and source versions independently.'
            })
            existing.add(ident)
            inserted += 1
    errs = validate(data)
    if errs:
        raise ValueError('Ingest produced invalid ledger: ' + '; '.join(errs))
    return {
        'added': inserted, 'duplicate_keys': duplicates,
        'skipped_rows': skipped, 'total_candidates': len(data['papers'])
    }


def next_steps(data):
    r = data['researcher']
    steps = []
    if not r.get('identity_confirmed'):
        steps.append('G1 Verify identity with a real scholar identifier and independent bibliography source. Imported papers are candidates only.')
    if len(r.get('sources_checked', [])) < 2:
        steps.append('G1 Cross-check at least two independent bibliographic sources and record exclusions/duplicates.')
    if not data['papers']:
        steps.append('G1 Discover and import candidate publications, then confirm they belong to this scholar.')
    else:
        selected = [p for p in data['papers'] if derived_paper_stage(p) not in ('full_main', 'full_with_supplement')]
        if selected:
            steps.append(f'G2 Inspect actual PDFs and appendices with page-level notes ({len(selected)} of {len(data["papers"])} lack full-main evidence).')
    if not data['repositories']:
        steps.append('G3 Locate research-code repositories and map methods to pinned source versions; do not treat README as code review.')
    elif any(derived_code_stage(r) != 'source_audited' for r in data['repositories']):
        steps.append('G3 Complete eligible source-file audit and trace data→forward→loss→evaluation.')
    if not data['runs'] or any(derived_run_stage(x) != 'metric_replication' for x in data['runs']):
        steps.append('G4 Where feasible, execute independent reproductions; otherwise record reasons and do not claim success.')
    steps.append('G5 Infer research-method principles from multiple papers plus field counterexamples; distinguish evidence from interpretation.')
    steps.append('G6 Use mentor→skeptical reviewer→one low-cost pilot; pre-register stopping conditions.')
    return steps


def main(argv=None):
    p = argparse.ArgumentParser(description='Offline cyber-supervisor evidence workspace helper')
    sp = p.add_subparsers(dest='command', required=True)
    a = sp.add_parser('init', help='Create private empty research workspace')
    a.add_argument('--name', required=True)
    a.add_argument('--slug', required=True)
    a.add_argument('--workspace', required=True)
    b = sp.add_parser('import-csv', help='Import candidate bibliographic records')
    b.add_argument('ledger')
    b.add_argument('csv')
    b.add_argument('--source-name', required=True)
    for cmd in ('status', 'next'):
        s = sp.add_parser(cmd)
        s.add_argument('ledger')
    args = p.parse_args(argv)
    try:
        if args.command == 'init':
            print('Created:', make_workspace(args.workspace, args.name, args.slug))
            return 0
        d = load(args.ledger)
        if args.command == 'import-csv':
            summary = import_csv(d, args.csv, args.source_name)
            write(args.ledger, d)
            print(json.dumps(summary, ensure_ascii=False, indent=2))
            return 0
        if args.command == 'status':
            print(report(d))
            return 0
        if args.command == 'next':
            for n, item in enumerate(next_steps(d), 1):
                print(f'{n}. {item}')
            return 0
    except (ValueError, FileExistsError, PermissionError, OSError, json.JSONDecodeError) as e:
        print('ERROR:', e, file=sys.stderr)
        return 2
    return 1


if __name__ == '__main__':
    sys.exit(main())
