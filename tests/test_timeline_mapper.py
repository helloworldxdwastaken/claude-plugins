"""Meaningful local map checks; fixture bytes are not semantic/media certification."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
import wave


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'plugins/source-timeline-mapper/skills/source-timeline-mapper/scripts/verify_timeline.py'
spec = importlib.util.spec_from_file_location('timeline_mapper', SCRIPT)
mapper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mapper)


class TimelineMapTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        for name in ('source', 'output'):
            (self.base / name).write_bytes(('synthetic map fixture ' + name).encode())
        self.doc = {
            'schema_version': 1,
            'assets': [self.asset('source', 'source', '1/48000', 48000),
                       self.asset('output', 'output', '1/24', 24)],
            'mappings': [dict(id='first', source='source', source_range=[0, 48000],
                              output='output', output_range=[0, 24], speed='1', status='verified')],
        }

    def asset(self, name, role, time_base, ticks):
        return dict(id=name, role=role, path=name, sha256=mapper.file_hash(self.base / name),
                    time_base=time_base, duration_ticks=ticks)

    def rejected(self, document):
        with self.assertRaises(mapper.InvalidMap):
            mapper.validate(document, self.base)

    def test_different_tick_units_have_exact_common_duration(self):
        result = mapper.validate(self.doc, self.base, require_verified=True)
        self.assertEqual(result['provisional_mappings'], 0)

    def test_provisional_is_reported_and_cannot_pass_verified_gate(self):
        self.doc['mappings'][0]['status'] = 'provisional'
        self.assertEqual(mapper.validate(self.doc, self.base)['provisional_mappings'], 1)
        with self.assertRaisesRegex(mapper.InvalidMap, 'provisional'):
            mapper.validate(self.doc, self.base, require_verified=True)

    def test_changed_final_bytes_invalidate_previous_map(self):
        mapper.validate(self.doc, self.base)
        (self.base / 'output').write_bytes(b'different final take')
        with self.assertRaisesRegex(mapper.InvalidMap, 'hash differs'):
            mapper.validate(self.doc, self.base)

    def test_missing_original_is_rejected(self):
        (self.base / 'source').unlink()
        self.rejected(self.doc)

    def test_shortened_tail_and_out_of_bounds_cannot_pass(self):
        for endpoint in (23, 25):
            doc = copy.deepcopy(self.doc)
            doc['mappings'][0]['output_range'][1] = endpoint
            self.rejected(doc)

    def test_gap_and_overlap_with_equal_total_lengths_are_rejected(self):
        for ranges in [([0, 10], [12, 24]), ([0, 14], [12, 24])]:
            doc = copy.deepcopy(self.doc)
            first = doc['mappings'][0]
            first['source_range'] = [0, 2000 * (ranges[0][1] - ranges[0][0])]
            first['output_range'] = ranges[0]
            second = copy.deepcopy(first)
            second.update(id='second', source_range=[0, 2000 * (ranges[1][1] - ranges[1][0])],
                          output_range=ranges[1])
            doc['mappings'].append(second)
            self.rejected(doc)

    def test_retiming_must_be_explicit_and_exact(self):
        self.doc['mappings'][0]['source_range'] = [0, 24000]
        self.rejected(self.doc)
        self.doc['mappings'][0]['speed'] = '1/2'
        mapper.validate(self.doc, self.base)

    def test_source_free_intervals_need_explicit_intent(self):
        row = self.doc['mappings'][0]
        row['source'] = None
        del row['source_range']
        del row['speed']
        self.rejected(self.doc)
        row['intent'] = 'intentional_silence'
        mapper.validate(self.doc, self.base)

    def test_invalid_ticks_ratios_and_duplicate_ids(self):
        for mutation in ('bool-ticks', 'zero-ratio', 'duplicate-map', 'duplicate-asset', 'fractional-range'):
            doc = copy.deepcopy(self.doc)
            if mutation == 'bool-ticks':
                doc['assets'][0]['duration_ticks'] = True
            elif mutation == 'zero-ratio':
                doc['assets'][0]['time_base'] = '1/0'
            elif mutation == 'duplicate-map':
                doc['mappings'].append(copy.deepcopy(doc['mappings'][0]))
            elif mutation == 'duplicate-asset':
                doc['assets'].append(copy.deepcopy(doc['assets'][0]))
            else:
                doc['mappings'][0]['output_range'] = [0, 23.5]
            with self.subTest(mutation=mutation):
                self.rejected(doc)

    @unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe'), 'FFmpeg tools unavailable')
    def test_actual_local_video_and_pcm_clock_export(self):
        source = self.base / 'source.mkv'
        output = self.base / 'output.wav'
        subprocess.run(['ffmpeg', '-v', 'error', '-f', 'lavfi', '-i',
                        'testsrc=size=64x64:rate=24:duration=1', '-c:v', 'ffv1', str(source)], check=True)
        probe = json.loads(subprocess.check_output([
            'ffprobe', '-v', 'error', '-select_streams', 'v:0', '-count_frames',
            '-show_entries', 'stream=nb_read_frames,avg_frame_rate', '-of', 'json', str(source)]))
        stream = probe['streams'][0]
        self.assertEqual(stream['avg_frame_rate'], '24/1')
        self.assertEqual(int(stream['nb_read_frames']), 24)
        with wave.open(str(output), 'wb') as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(48000)
            wav.writeframes(bytes(96000))
        with wave.open(str(output), 'rb') as wav:
            self.assertEqual(wav.getnframes(), 48000)
        doc = copy.deepcopy(self.doc)
        for asset, path, time_base, ticks in zip(doc['assets'], [source, output], ['1/24', '1/48000'], [24, 48000]):
            asset.update(path=path.name, sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                         time_base=time_base, duration_ticks=ticks)
        doc['mappings'][0].update(source_range=[0, 24], output_range=[0, 48000])
        mapper.validate(doc, self.base, require_verified=True)
        map_path = self.base / 'map.json'
        map_path.write_text(json.dumps(doc))
        completed = subprocess.run(['python3', str(SCRIPT), str(map_path), '--require-verified'],
                                   capture_output=True, text=True, check=True)
        self.assertEqual(json.loads(completed.stdout)['mappings'], 1)


if __name__ == '__main__':
    unittest.main()
