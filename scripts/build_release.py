from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

from _common import ROOT, all_files, load_yaml, sha256_file, write_text

VERSION = load_yaml('pack-manifest.yaml')['pack']['version']
DIST = ROOT / 'dist'


def zip_paths(output: Path, paths: list[Path]) -> None:
    if output.exists():
        output.unlink()
    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for path in sorted(set(paths)):
            if not path.is_file():
                continue
            rel = path.relative_to(ROOT)
            zf.write(path, Path('agentic-world-graph') / rel)


def expand(prefixes: list[str], include_root: bool = True) -> list[Path]:
    paths: list[Path] = []
    if include_root:
        paths += [p for p in ROOT.iterdir() if p.is_file() and p.name not in {'dist'}]
    for prefix in prefixes:
        p = ROOT / prefix
        if p.is_file():
            paths.append(p)
        elif p.is_dir():
            paths += [x for x in p.rglob('*') if x.is_file() and not ({'dist', '__pycache__', '.pytest_cache', '.git'} & set(x.relative_to(ROOT).parts))]
    return paths


def audit_zip(path: Path, expected_names: set[str] | None = None) -> list[str]:
    messages: list[str] = []
    with zipfile.ZipFile(path) as zf:
        names = zf.namelist()
        if len(names) != len(set(names)):
            raise RuntimeError(f'Duplicate archive entries in {path.name}')
        for name in names:
            posix = PurePosixPath(name)
            if posix.is_absolute() or '..' in posix.parts or not posix.parts or posix.parts[0] != 'agentic-world-graph':
                raise RuntimeError(f'Unsafe archive path in {path.name}: {name}')
        bad = zf.testzip()
        if bad:
            raise RuntimeError(f'Archive integrity failure in {path.name}: {bad}')
        if expected_names is not None and set(names) != expected_names:
            missing = sorted(expected_names - set(names))[:10]
            extra = sorted(set(names) - expected_names)[:10]
            raise RuntimeError(f'Archive content mismatch in {path.name}; missing={missing}, extra={extra}')
        messages.append(f'{path.name}: {len(names)} entries, integrity and path safety PASS')
    return messages


def main() -> None:
    subprocess.run([sys.executable, str(ROOT / 'scripts/validate_all.py')], cwd=ROOT, check=True)
    subprocess.run([sys.executable, '-m', 'pytest', '-q'], cwd=ROOT, check=True)
    DIST.mkdir(exist_ok=True)
    for old in DIST.glob('*'):
        if old.name != '.gitkeep':
            old.unlink() if old.is_file() else shutil.rmtree(old)

    # The manifest covers every source file except itself and release artefacts, avoiding an impossible self-hash.
    source_files = [p for p in all_files(exclude_dist=True) if p.relative_to(ROOT).as_posix() != 'generated/file-manifest.json']
    inventory = [
        {'path': p.relative_to(ROOT).as_posix(), 'size': p.stat().st_size, 'sha256': sha256_file(p)}
        for p in source_files
    ]
    manifest = {
        'pack': 'Agentic World Graph',
        'version': VERSION,
        'created_at': datetime.now(timezone.utc).isoformat(),
        'scope': 'All source files except generated/file-manifest.json and dist release artefacts.',
        'excluded_paths': ['generated/file-manifest.json', 'dist/**'],
        'file_count': len(inventory),
        'files': inventory,
    }
    write_text('generated/file-manifest.json', json.dumps(manifest, indent=2, ensure_ascii=False))
    source_files = all_files(exclude_dist=True)

    full = DIST / f'agentic-world-graph-v{VERSION}.zip'
    zip_paths(full, source_files)

    shared = ['README.md', 'AGENTS.md', 'pack-manifest.yaml', 'docs/README.md', 'generated', 'registers', 'LICENSE', 'NOTICE.md']
    parts = [
        (f'agentic-world-graph-v{VERSION}-part-1-foundation-domain.zip', shared + ['docs/00-vision-and-research', 'docs/01-governance-and-safety', 'docs/02-domain-model']),
        (f'agentic-world-graph-v{VERSION}-part-2-platform-scenarios.zip', shared + ['docs/03-platform-architecture', 'docs/04-scenarios-and-validation', 'contracts']),
        (f'agentic-world-graph-v{VERSION}-part-3-ui-delivery.zip', shared + ['docs/05-ui-ux', 'docs/06-delivery-and-operations', 'decisions', '.github']),
        (f'agentic-world-graph-v{VERSION}-part-4-contracts-tools-archive.zip', shared + ['docs/10-appendices', 'contracts', 'examples', 'scripts', 'tests', 'templates', 'archive', 'pyproject.toml', 'requirements-dev.txt', 'Dockerfile', 'docker-compose.yml', 'Makefile', 'mkdocs.yml']),
    ]
    archives = [full]
    for name, prefixes in parts:
        output = DIST / name
        zip_paths(output, expand(prefixes, include_root=True))
        archives.append(output)

    audit_lines: list[str] = []
    expected_full_names = {f'agentic-world-graph/{p.relative_to(ROOT).as_posix()}' for p in source_files}
    audit_lines.extend(audit_zip(full, expected_full_names))
    part_union: set[str] = set()
    for archive in archives[1:]:
        audit_lines.extend(audit_zip(archive))
        with zipfile.ZipFile(archive) as zf:
            part_union.update(zf.namelist())
    if part_union != expected_full_names:
        missing = sorted(expected_full_names - part_union)[:20]
        extra = sorted(part_union - expected_full_names)[:20]
        raise RuntimeError(f'Logical part union does not reconstruct the full source set; missing={missing}, extra={extra}')
    audit_lines.append('Logical part union reconstructs the complete full-archive source set: PASS')

    # Extract and verify every hash covered by the self-excluding source manifest.
    with tempfile.TemporaryDirectory(prefix='awg-release-audit-') as tmp:
        tmp_path = Path(tmp)
        with zipfile.ZipFile(full) as zf:
            zf.extractall(tmp_path)
        extracted_root = tmp_path / 'agentic-world-graph'
        extracted_manifest = json.loads((extracted_root / 'generated/file-manifest.json').read_text(encoding='utf-8'))
        for item in extracted_manifest['files']:
            candidate = extracted_root / item['path']
            if not candidate.is_file():
                raise RuntimeError(f'Manifest file missing after extraction: {item["path"]}')
            if candidate.stat().st_size != item['size']:
                raise RuntimeError(f'Manifest size mismatch after extraction: {item["path"]}')
            if sha256_file(candidate) != item['sha256']:
                raise RuntimeError(f'Manifest hash mismatch after extraction: {item["path"]}')
        audit_lines.append(f'Full archive manifest: {extracted_manifest["file_count"]} source files verified by SHA-256')

        # Re-run the repository checks from the extracted release to prove it is self-contained.
        validation = subprocess.run(
            [sys.executable, 'scripts/validate_all.py'], cwd=extracted_root,
            text=True, capture_output=True, check=True,
        )
        tests = subprocess.run(
            [sys.executable, '-m', 'pytest', '-q'], cwd=extracted_root,
            text=True, capture_output=True, check=True,
        )
        audit_lines.append('Extracted full archive validation: PASS')
        audit_lines.append('Extracted full archive pytest suite: PASS')
        validation_output = (validation.stdout + validation.stderr).strip()
        tests_output = (tests.stdout + tests.stderr).strip()

    checksum_lines = [f'{sha256_file(a)}  {a.name}' for a in archives]
    write_text('dist/SHA256SUMS.txt', '\n'.join(checksum_lines))
    release_rows = ['# Release Inventory', '', f'Version: {VERSION}', '', 'The full ZIP contains the complete repository. Logical part ZIPs are independently downloadable subsets and do not require binary recombination.', '']
    for a in archives:
        release_rows.append(f'- `{a.name}` — {a.stat().st_size} bytes — SHA-256 `{sha256_file(a)}`')
    write_text('dist/RELEASE-INVENTORY.md', '\n'.join(release_rows))

    audit_report = [
        '# Release Validation Report', '',
        f'**Version:** {VERSION}',
        f'**Created at:** {datetime.now(timezone.utc).isoformat()}',
        '**Overall result:** PASS', '',
        '## Archive and manifest checks', '',
    ]
    audit_report += [f'- {line}' for line in audit_lines]
    audit_report += ['', '## Validation output from extracted full archive', '', '```text', validation_output, '```', '', '## Test output from extracted full archive', '', '```text', tests_output, '```', '', '## Interpretation', '', 'PASS confirms repository structure, traceability, schema references/catalogue, valid and invalid fixtures, internal links, file-manifest hashes, archive integrity/path safety, extracted-package validation, and the packaged Python test suite. It does not imply that draft architecture decisions are human-approved or that a future simulator implementation is empirically validated.']
    write_text('dist/RELEASE-VALIDATION.md', '\n'.join(audit_report))

    print(f'Built, extracted, hash-verified, and integrity-tested {len(archives)} release archives in {DIST}.')


if __name__ == '__main__':
    main()
