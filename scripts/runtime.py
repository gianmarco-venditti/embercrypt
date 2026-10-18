#!/usr/bin/env python3
"""Project-local Flare bundle installation and launch; Python standard library only."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / '.runtime'
APP = RUNTIME / 'flare-1.15'
DATA = RUNTIME / 'data'
LOCAL = ROOT / '.local'
MOD = 'ember_slice'


def link(source, target):
    if target.is_symlink():
        if target.resolve() == source.resolve():
            return
        target.unlink()
    elif target.exists():
        raise RuntimeError(f'Non sovrascrivo un percorso esistente: {target}')
    target.symlink_to(source.resolve(), target_is_directory=source.is_dir())


def prepare_data():
    if not APP.is_dir():
        raise RuntimeError('Flare non disponibile. Esegui ./setup.sh dal tuo terminale.')
    (DATA / 'mods').mkdir(parents=True, exist_ok=True)
    for name in ('default', 'fantasycore', 'empyrean_campaign'):
        candidates = sorted(path for path in APP.rglob(name)
                            if path.is_dir() and path.parent.name == 'mods')
        if not candidates:
            raise RuntimeError(f'Bundle incompleto: manca la mod {name}')
        link(candidates[0], DATA / 'mods' / name)
    link(ROOT / 'mods' / MOD, DATA / 'mods' / MOD)


def install(bundle):
    if not bundle.is_file():
        raise RuntimeError(f'Bundle non trovato: {bundle}')
    RUNTIME.mkdir(exist_ok=True)
    if not APP.exists():
        with bundle.open('rb') as stream:
            if stream.read(4) != b'\x7fELF':
                raise RuntimeError('Il file non e un AppImage ELF (download incompleto o pagina HTML).')
        bundle.chmod(bundle.stat().st_mode | 0o100)
        with tempfile.TemporaryDirectory(prefix='extract-', dir=RUNTIME) as stage:
            with (RUNTIME / 'extract.log').open('w') as log:
                subprocess.run([str(bundle), '--appimage-extract'], cwd=stage,
                               stdout=log, stderr=subprocess.STDOUT, check=True)
            extracted = Path(stage) / 'squashfs-root'
            if not extracted.is_dir():
                raise RuntimeError('Estrazione AppImage fallita; vedi .runtime/extract.log')
            extracted.rename(APP)
    prepare_data()
    with bundle.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    manifest = {
        'version': '1.15',
        'url': 'https://github.com/flareteam/flare-game/releases/download/v1.15/flare-linux64-v1.15.AppImage',
        'sha256_local': digest,
        'checksum_note': 'Local fingerprint; not an independently verified upstream signature.',
        'installed_at': datetime.now(timezone.utc).isoformat(),
    }
    (RUNTIME / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print('Flare estratto nel progetto; FUSE e sudo non necessari.')


def environment():
    env = os.environ.copy()
    for key, folder in [('XDG_CONFIG_HOME', 'config'), ('XDG_DATA_HOME', 'share'),
                        ('XDG_CACHE_HOME', 'cache')]:
        path = LOCAL / folder
        path.mkdir(parents=True, exist_ok=True)
        env[key] = str(path)
    # Use the bundled native executable, so AppRun cannot override --data-path.
    # Arch ships newer PipeWire/JACK together. Prefer their coherent host versions
    # over the older bundle copies; use bundled libraries for missing SDL add-ons.
    libdirs = [path for path in ('/usr/lib', '/usr/lib/x86_64-linux-gnu', '/lib/x86_64-linux-gnu')
               if Path(path).is_dir()]
    libdirs += sorted({str(path.parent) for path in APP.rglob('*.so*') if path.is_file()})
    if env.get('LD_LIBRARY_PATH'):
        libdirs.append(env['LD_LIBRARY_PATH'])
    env['LD_LIBRARY_PATH'] = ':'.join(libdirs)
    return env


def command(extra):
    binaries = sorted(p for p in APP.rglob('flare') if p.is_file() and os.access(p, os.X_OK))
    if not binaries:
        raise RuntimeError('Eseguibile flare assente dal bundle estratto.')
    return [str(binaries[0]), f'--data-path={DATA}',
            '--mods=fantasycore,empyrean_campaign,ember_slice', *extra]


def launch(extra):
    prepare_data()
    env = environment()
    config_dir = LOCAL / 'config' / 'flare'
    config_dir.mkdir(parents=True, exist_ok=True)
    settings = config_dir / 'settings.txt'
    if not settings.exists():
        settings.write_text('fullscreen=0\nresolution_w=1280\nresolution_h=720\n'
                            'language=it\nmouse_move=1\nmouse_aim=1\n'
                            'music_volume=48\nsound_volume=96\nmax_fps=60\n'
                            'setup_language=1\nsetup_mousemove=1\n')
    logs = LOCAL / 'logs'
    logs.mkdir(parents=True, exist_ok=True)
    logfile = logs / (datetime.now().strftime('%Y%m%d-%H%M%S') + f'-{os.getpid()}.log')
    cmd = command(extra)
    print('La Cripta della Brace — Flare 1.15', flush=True)
    print(f'Log: {logfile.relative_to(ROOT)}', flush=True)
    with logfile.open('w') as log:
        result = subprocess.run(cmd, cwd=DATA, env=env, stdout=log, stderr=subprocess.STDOUT)
    if result.returncode:
        print(logfile.read_text(errors='replace')[-6000:], file=sys.stderr)
    return result.returncode


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['install', 'play'])
    parser.add_argument('arguments', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    if args.action == 'install':
        if len(args.arguments) != 1:
            parser.error('install richiede il percorso del bundle AppImage')
        install(Path(args.arguments[0]).resolve())
        return 0
    return launch(args.arguments)


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (RuntimeError, OSError, subprocess.CalledProcessError) as exc:
        print(f'Errore: {exc}', file=sys.stderr)
        sys.exit(1)
