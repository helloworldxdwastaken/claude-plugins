#!/usr/bin/env python3
"""Validate declared timeline arithmetic and local bytes; not content correspondence."""
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re
import sys


class InvalidMap(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise InvalidMap(message)


def positive_ratio(value, label):
    require(isinstance(value, str), label + ' must be a rational string')
    try:
        ratio = Fraction(value)
    except (ValueError, ZeroDivisionError):
        raise InvalidMap(label + ' must be a positive rational') from None
    require(ratio > 0, label + ' must be positive')
    return ratio


def bounds(value, length, label):
    require(isinstance(value, list) and len(value) == 2, label + ' must have two bounds')
    require(all(type(n) is int for n in value), label + ' bounds must be integers')
    require(0 <= value[0] < value[1] <= length, label + ' is empty or out of bounds')
    return value


def file_hash(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def validate(document, base, require_verified=False):
    require(isinstance(document, dict), 'map must be an object')
    require(type(document.get('schema_version')) is int and document['schema_version'] == 1,
            'unsupported schema_version')
    require(isinstance(document.get('assets'), list) and document['assets'], 'assets are required')
    require(isinstance(document.get('mappings'), list) and document['mappings'], 'mappings are required')
    assets = {}
    for asset in document['assets']:
        require(isinstance(asset, dict), 'asset must be an object')
        name = asset.get('id')
        require(isinstance(name, str) and name and name not in assets, 'asset IDs must be unique strings')
        require(asset.get('role') in ('source', 'output'), name + ': invalid role')
        require(type(asset.get('duration_ticks')) is int and asset['duration_ticks'] > 0,
                name + ': duration_ticks must be a positive integer')
        positive_ratio(asset.get('time_base'), name + ': time_base')
        require(isinstance(asset.get('path'), str) and asset['path'], name + ': path is required')
        sha = asset.get('sha256')
        require(isinstance(sha, str) and re.fullmatch('[0-9a-f]{64}', sha), name + ': invalid sha256')
        path = (base / asset['path']).resolve()
        require(path.is_file(), name + ': file is missing')
        require(file_hash(path) == sha, name + ': file hash differs')
        assets[name] = asset
    output_intervals = {key: [] for key, asset in assets.items() if asset['role'] == 'output'}
    require(output_intervals, 'at least one output asset is required')
    seen = set()
    provisional = 0
    for mapping in document['mappings']:
        require(isinstance(mapping, dict), 'mapping must be an object')
        name = mapping.get('id')
        require(isinstance(name, str) and name and name not in seen, 'mapping IDs must be unique strings')
        seen.add(name)
        output = mapping.get('output')
        require(isinstance(output, str) and output in output_intervals, name + ': unknown output asset')
        out_asset = assets[output]
        out_range = bounds(mapping.get('output_range'), out_asset['duration_ticks'], name + ': output_range')
        output_intervals[output].append(out_range)
        require(mapping.get('status') in ('provisional', 'verified'), name + ': invalid status')
        provisional += mapping['status'] == 'provisional'
        require(not require_verified or mapping['status'] == 'verified', name + ': provisional correspondence')
        require('source' in mapping, name + ': source must be explicit')
        source = mapping['source']
        if source is None:
            require(mapping.get('intent') in ('intentional_silence', 'generated_cutaway'), name + ': missing non-source intent')
            require('source_range' not in mapping and 'speed' not in mapping, name + ': source-free interval has source timing')
            continue
        require(isinstance(source, str) and source in assets and assets[source]['role'] == 'source',
                name + ': unknown source asset')
        src_asset = assets[source]
        src_range = bounds(mapping.get('source_range'), src_asset['duration_ticks'], name + ': source_range')
        speed = positive_ratio(mapping.get('speed'), name + ': speed')
        source_seconds = (src_range[1] - src_range[0]) * Fraction(src_asset['time_base'])
        output_seconds = (out_range[1] - out_range[0]) * Fraction(out_asset['time_base'])
        require(source_seconds == output_seconds * speed, name + ': duration/speed mismatch')
    for name, intervals in output_intervals.items():
        cursor = 0
        for start, end in sorted(intervals):
            require(start == cursor, name + ': output coverage has a gap or overlap at tick ' + str(cursor))
            cursor = end
        require(cursor == assets[name]['duration_ticks'], name + ': output tail is not covered')
    return {'assets': len(assets), 'mappings': len(seen), 'provisional_mappings': provisional,
            'scope': 'declared arithmetic, coverage and file hashes; no content or decoded-clock certification'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('map', type=Path)
    parser.add_argument('--require-verified', action='store_true')
    args = parser.parse_args()
    try:
        document = json.loads(args.map.read_text())
        result = validate(document, args.map.resolve().parent, args.require_verified)
    except (OSError, ValueError, TypeError) as exc:
        print('INVALID: ' + str(exc), file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main())
