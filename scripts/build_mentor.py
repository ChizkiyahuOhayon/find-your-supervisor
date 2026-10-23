#!/usr/bin/env python3
"""Compile a private, evidence-based scholar-method Skill; never impersonate."""
import argparse
import json
import re
import sys
from pathlib import Path
from audit import validate, derived_paper_stage, derived_code_stage

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_PAPER_STAGES = {'selected_pages', 'full_main', 'full_with_supplement'}


def check(data, dna):
    issues = ['ledger: ' + e for e in validate(data)]
    person = data.get('researcher', {})
    if not person.get('identity_confirmed'):
        issues.append('researcher identity not independently confirmed')
    if len(person.get('sources_checked', [])) < 2:
        issues.append('fewer than two independent bibliography sources logged')
    if dna.get('schema_version') != '1.0.0':
        issues.append('DNA schema must be 1.0.0')
    if dna.get('researcher_slug') != person.get('slug'):
        issues.append('DNA slug does not match ledger')
    papers = {p['canonical_id']: p for p in data.get('papers', []) if isinstance(p, dict) and 'canonical_id' in p}
    ideas = dna.get('principles', [])
    if not isinstance(ideas, list) or not ideas:
        issues.append('at least one documented principle required')
        ideas = []
    seen = set()
    for idea in ideas:
        if not isinstance(idea, dict):
            issues.append('principle must be object')
            continue
        ident = idea.get('id', '<unknown>')
        if ident in seen:
            issues.append(f'duplicate principle {ident}')
        seen.add(ident)
        if not all(isinstance(idea.get(k), str) and idea[k].strip() for k in ('id','principle','student_application','falsification_test')):
            issues.append(f'{ident}: missing principle/application/falsification')
        refs = idea.get('supporting_paper_ids')
        if not isinstance(refs,list) or len(set(refs)) < 2:
            issues.append(f'{ident}: at least two distinct supporting papers required')
            continue
        for ref in refs:
            if ref not in papers:
                issues.append(f'{ident}: paper not in ledger: {ref}')
                continue
            if not papers[ref].get('author_identity_verified'):
                issues.append(f'{ident}: authorship unverified for {ref}')
            if derived_paper_stage(papers[ref]) not in ALLOWED_PAPER_STAGES:
                issues.append(f'{ident}: no page-level paper evidence for {ref}')
        if idea.get('confidence') not in {'hypothesis','cross-checked','strong'}:
            issues.append(f'{ident}: invalid confidence')
        if idea.get('confidence') == 'strong':
            for ref in refs:
                if ref in papers and derived_paper_stage(papers[ref]) not in ('full_main','full_with_supplement'):
                    issues.append(f'{ident}: strong requires fully inspected main PDF for each supporting paper')
        if not isinstance(idea.get('field_counterexamples', []), list):
            issues.append(f'{ident}: counterexamples must be a list')
    return issues


def clean(text):
    return re.sub(r'\s+', ' ', str(text or '')).strip().replace('<', '‹').replace('>', '›')


def compile_markdown(data, dna):
    person = data['researcher']
    name, slug = clean(person['name']), person['slug']
    rows = [
        f'---\nname: {slug}-research-mentor\ndescription: Evidence-grounded, non-impersonating research methodology lens derived from public work of {name}. Use to mentor original research decisions with independent novelty and falsification.\n---',
        f'# Research methods associated with {name} (independent analysis)',
        '**Not the researcher, not officially endorsed, not a substitute for a human advisor.** This profile is a set of evidence-backed hypotheses about public research practice.',
        '## Before mentoring',
        'Read SOURCES.md and the linked public papers. Verify recent outside work and never treat an unrun result as reproduced.',
        '## Research-method hypotheses'
    ]
    for item in dna['principles']:
        refs = ', '.join(item['supporting_paper_ids'])
        rows.append(f'### {clean(item["id"])} — {clean(item["principle"])}')
        rows.append(f'- **Evidence level:** {clean(item["confidence"])}; papers: {refs}')
        rows.append(f'- **Possible student application:** {clean(item["student_application"])}')
        rows.append(f'- **Cheap disconfirmation test:** {clean(item["falsification_test"])}')
        if item.get('field_counterexamples'):
            rows.append('- **Field counterexamples:** ' + '; '.join(clean(x) for x in item['field_counterexamples']))
    rows.extend([
        '## Mentor workflow',
        '1. Define observable problem, falsifiable hypothesis, and task metric.',
        '2. Search closest external competing methods and compare mechanisms.',
        '3. Propose the smallest matched-compute experiment.',
        '4. Perform skeptical review for novelty, leakage, baseline, reliability and resources.',
        '5. Return GO / REVISE / PIVOT / BLOCKED with an explicit stop criterion.',
        '## Evidence limitations',
        f'- Corpus ledger: {len(data["papers"])} papers; completeness not guaranteed.',
        f'- Repository records: {len(data["repositories"])}; do not confuse READMEs with source audit.',
        f'- Experiment run records: {len(data["runs"])}; do not infer replication.',
        'Profiles generated by this tool are intended to remain private.'
    ])
    return '\n\n'.join(rows) + '\n'


def sources_md(data, dna):
    papers = {p['canonical_id']:p for p in data['papers']}
    out = ['# Sources and provenance', '', 'Independent public evidence, not a personal endorsement.', '']
    ids = sorted(set(ref for item in dna['principles'] for ref in item['supporting_paper_ids']))
    for ident in ids:
        p = papers[ident]
        out.append(f'- {ident}: {clean(p["title"])} ({p["year"]}); {p["url"]}; source stage {derived_paper_stage(p)}')
    out.append('\nThe ledger describes recorded evidence and is not independent certification of reading.')
    return '\n'.join(out) + '\n'


def main(argv=None):
    ap=argparse.ArgumentParser(description='Compile private scholar mentor from verified source records')
    ap.add_argument('--ledger',required=True)
    ap.add_argument('--dna',required=True)
    ap.add_argument('--output',required=True)
    args=ap.parse_args(argv)
    try:
        data=json.loads(Path(args.ledger).read_text(encoding='utf-8'))
        dna=json.loads(Path(args.dna).read_text(encoding='utf-8'))
        issues=check(data,dna)
        if issues:
            for issue in issues: print('BLOCKED:',issue,file=sys.stderr)
            return 2
        target=Path(args.output).expanduser().resolve()
        if target==ROOT or ROOT in target.parents:
            raise ValueError('Researcher-specific profiles must remain outside public repository')
        if target.exists() and any(target.iterdir()):
            raise ValueError('Output directory must be absent or empty')
        target.mkdir(parents=True,exist_ok=True)
        (target/'SKILL.md').write_text(compile_markdown(data,dna),encoding='utf-8')
        (target/'SOURCES.md').write_text(sources_md(data,dna),encoding='utf-8')
        print('Generated private evidence-grounded mentor:',target)
        return 0
    except (OSError,ValueError,json.JSONDecodeError) as e:
        print('ERROR:',e,file=sys.stderr)
        return 2


if __name__=='__main__':
    sys.exit(main())
