#!/usr/bin/env python3
"""Read-only optional research skill availability router; never installs or executes."""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def manifest():
    return json.loads((ROOT / 'integrations' / 'routes.json').read_text(encoding='utf-8'))


def parsed_roots(values):
    result = {}
    for value in values:
        if '=' not in value:
            raise ValueError('Root must be source=/local/directory')
        source, path = value.split('=', 1)
        if source not in manifest()['sources']:
            raise ValueError(f'Unknown source: {source}')
        home = Path(path).expanduser().resolve()
        if not home.is_dir():
            raise ValueError(f'Not a directory: {home}')
        result[source] = home
    return result


def candidates(task, roots, config=None):
    data = config or manifest()
    if task not in data['tasks']:
        raise ValueError(f'Unknown task: {task}')
    result = []
    for entry in data['tasks'][task]:
        source, path = entry['source'], entry['path']
        rel = Path(path)
        if rel.is_absolute() or '..' in rel.parts:
            raise ValueError('Unsafe skill path')
        location = roots.get(source)
        skill_file = (location / rel).resolve() if location else None
        safe = location is not None and (location == skill_file or location in skill_file.parents)
        exists = bool(safe and skill_file.is_file())
        result.append({
            'source': source, 'path': path, 'available': exists,
            'local_path': str(skill_file) if exists else None,
            'license': data['sources'][source]['license'],
            'note': 'Presence check only. Do not auto-execute; observe third-party terms.'
        })
    return result


def main(argv=None):
    ap = argparse.ArgumentParser(description='Inspect optional independently installed research skill routes')
    sub = ap.add_subparsers(dest='cmd', required=True)
    sub.add_parser('list')
    route = sub.add_parser('route')
    route.add_argument('--task', required=True)
    route.add_argument('--root', action='append', default=[])
    route.add_argument('--json', action='store_true')
    args = ap.parse_args(argv)
    try:
        if args.cmd == 'list':
            print('Known tasks:', ', '.join(sorted(manifest()['tasks'])))
            print('Sources:', ', '.join(sorted(manifest()['sources'])))
            return 0
        results = candidates(args.task, parsed_roots(args.root))
        if args.json:
            print(json.dumps(results, indent=2, ensure_ascii=False))
        else:
            for item in results:
                mark = 'AVAILABLE' if item['available'] else 'NOT INSTALLED'
                print(f'{mark}: {item["source"]}/{item["path"]} [{item["license"]}]')
            print('These are suggestions, not installed tools or authorization to execute.')
        return 0
    except (ValueError, OSError) as e:
        print('ERROR:', e, file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
