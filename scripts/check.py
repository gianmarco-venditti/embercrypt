#!/usr/bin/env python3
"""Validate map geometry, campaign links, and (when installed) upstream references."""
import argparse
from collections import deque
from pathlib import Path
import re
import sys

from build_maps import build, START, CHEST, EXIT, ENEMIES
from runtime import ROOT, DATA, prepare_data

MOD = ROOT / 'mods' / 'ember_slice'


def sections(path):
    result = []
    current = []
    name = ''
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith('#') or line in ('APPEND', 'INCLUDE'):
            continue
        if line.startswith('[') and line.endswith(']'):
            result.append((name, current))
            name, current = line[1:-1], []
        elif '=' in line:
            key, value = line.split('=', 1)
            current.append((key, value))
        elif current and current[-1][0] == 'data':
            key, value = current.pop()
            current.append((key, value + line))
    result.append((name, current))
    return result


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def map_info(path):
    parts = sections(path)
    header = next(dict(values) for name, values in parts if name == 'header')
    width, height = int(header['width']), int(header['height'])
    layers = {}
    for name, values in parts:
        if name != 'layer':
            continue
        layer = dict(values)
        numbers = [int(value) for value in layer['data'].split(',') if value]
        require(len(numbers) == width * height, f'{path.name}: dimensioni layer {layer["type"]} errate')
        layers[layer['type']] = numbers
    require({'background', 'object', 'collision'} <= layers.keys(), f'{path.name}: layer mancanti')
    walkable = {(x, y) for y in range(height) for x in range(width)
                if layers['collision'][y * width + x] == 0}
    spawn = tuple(map(int, header['hero_pos'].split(',')))
    require(spawn in walkable, f'{path.name}: spawn in una parete')
    visited, queue = {spawn}, deque([spawn])
    while queue:
        x, y = queue.popleft()
        for point in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
            if point in walkable and point not in visited:
                visited.add(point)
                queue.append(point)
    require(visited == walkable, f'{path.name}: zone calpestabili scollegate')
    return parts, walkable, visited


def resolve(relative):
    for name in ('ember_slice', 'empyrean_campaign', 'fantasycore', 'default'):
        candidate = DATA / 'mods' / name / relative
        if candidate.is_file():
            return candidate
    return None


def flatten(path, stack=()):
    require(path not in stack, f'INCLUDE circolare: {path}')
    lines = []
    for line in path.read_text().splitlines():
        if line.startswith('INCLUDE '):
            relative = line.split(None, 1)[1]
            target = resolve(relative)
            require(target is not None, f'INCLUDE mancante: {relative}')
            lines.extend(flatten(target, (*stack, path)))
        else:
            lines.append(line)
    return lines


def check_assets():
    prepare_data()
    checked = set()

    def check_file(path):
        if path in checked:
            return
        checked.add(path)
        for raw in path.read_text().splitlines():
            line = raw.strip()
            if not line or line.startswith('#'):
                continue
            if line.startswith('INCLUDE '):
                relative = line.split(None, 1)[1]
                target = resolve(relative)
                require(target is not None, f'{path.name}: INCLUDE assente: {relative}')
                check_file(target)
            elif '=' in line:
                _, value = line.split('=', 1)
                for relative in re.findall(r'(?:^|,)([\w/.-]+\.(?:txt|png|ogg|wav))(?:,|$)', value):
                    require(resolve(relative) is not None, f'{path.name}: risorsa assente: {relative}')

    for path in MOD.rglob('*.txt'):
        check_file(path)
    for path in (MOD / 'maps').glob('ember_*.txt'):
        parts = sections(path)
        header = next(dict(values) for name, values in parts if name == 'header')
        tileset = resolve(header['tileset'])
        require(tileset is not None, f'Tileset mancante: {header["tileset"]}')
        tile_ids = {int(line.split('=', 1)[1].split(',')[0])
                    for line in tileset.read_text().splitlines() if line.startswith('tile=')}
        for name, values in parts:
            layer = dict(values)
            if name == 'layer' and layer.get('type') in ('background', 'object'):
                used = {int(value) for value in layer['data'].split(',') if value} - {0}
                require(used <= tile_ids, f'{path.name}: tile non definiti: {sorted(used - tile_ids)}')
    # Ensure upstream item data doesn't already use our custom identifier.
    upstream = DATA / 'mods' / 'empyrean_campaign' / 'items' / 'items.txt'
    require('id=5000' not in [line.strip() for line in flatten(upstream)], 'ID oggetto 5000 gia usato a monte')
    # Verify each custom enemy can be selected by its map category.
    for filename, category in [('ember_skeleton.txt', 'ember_melee'),
                               ('ember_archer.txt', 'ember_archer'),
                               ('ember_guardian.txt', 'ember_guardian')]:
        values = dict(line.split('=', 1) for line in flatten(MOD / 'enemies' / filename)
                      if '=' in line and not line.lstrip().startswith('#'))
        require(values.get('categories') == category, f'Categoria errata: {filename}')
        require(values.get('level') == '1' and values.get('rarity') == 'common', f'Nemico non selezionabile: {filename}')
    print(f'Riferimenti agli asset verificati ({len(checked)} file).')


def check():
    build(check=True)
    parts, walkable, visited = map_info(MOD / 'maps' / 'ember_crypt.txt')
    map_info(MOD / 'maps' / 'ember_refuge.txt')
    require(START in visited and CHEST in visited and EXIT in visited, 'Obiettivi irraggiungibili')
    groups = [dict(values) for name, values in parts if name == 'enemy']
    require(len(groups) == len(ENEMIES), 'Numero incontri inatteso')
    for group in groups:
        x, y, width, height = map(int, group['location'].split(','))
        require(width == height == 1 and (x, y) in visited, f'Nemico irraggiungibile: {group}')
    events = [dict(values) for name, values in parts if name == 'event']
    exits = [event for event in events if 'intermap' in event]
    require(len(exits) == 1, 'Numero uscite inatteso')
    require(exits[0].get('requires_status') == 'ember_guardian_dead', 'Uscita non vincolata al guardiano')
    require('defeat_status=ember_guardian_dead' in (MOD / 'enemies' / 'ember_guardian.txt').read_text(), 'Stato morte guardiano mancante')
    require(any(event.get('set_status') == 'ember_chest' and event.get('requires_not_status') == 'ember_chest'
                for event in events), 'Forziere senza protezione contro ricompense ripetute')
    for name, values in sections(MOD / 'quests' / 'ember.txt'):
        if name == 'quest':
            require(bool(dict(values).get('quest_text')), 'Quest senza testo riconosciuto dal motore')
    for path in (MOD / 'maps').glob('*.txt'):
        for name, values in sections(path):
            for key, value in values:
                if key != 'intermap':
                    continue
                filename, x, y = value.split(',')[:3]
                target = MOD / filename
                require(target.is_file(), f'Transizione verso mappa assente: {filename}')
                _, floor, _ = map_info(target)
                require((int(x), int(y)) in floor, f'Destinazione in una parete: {value}')
    print(f'Geometria e collegamenti validi: {len(walkable)} caselle raggiungibili, {len(groups)} nemici.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--assets', action='store_true', help='richiede il bundle Flare installato')
    args = parser.parse_args()
    try:
        check()
        if args.assets:
            check_assets()
        else:
            print('Asset e avvio del motore non verificati da questo controllo statico.')
    except (OSError, RuntimeError, ValueError, KeyError, StopIteration) as exc:
        print(f'ERRORE: {exc}', file=sys.stderr)
        sys.exit(1)
