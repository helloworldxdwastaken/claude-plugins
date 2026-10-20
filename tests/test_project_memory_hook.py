"""Exercise the Claude hook in isolated repositories without touching user memory."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

HOOK = Path(__file__).resolve().parents[1] / 'plugins/project-memory/hooks/session-start.sh'


class ProjectMemoryHookTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='project-memory test ')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def git(self, *args):
        subprocess.run(['git', '-C', str(self.root), *args], check=True,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def run_hook(self, cwd=None, **overrides):
        env = os.environ.copy()
        for key in ('CLAUDE_PROJECT_DIR', 'PROJECT_MEMORY_NUDGE', 'GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE'):
            env.pop(key, None)
        env.update(overrides)
        result = subprocess.run(['bash', str(HOOK)], cwd=cwd or self.root, env=env,
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, '')
        return result.stdout

    def test_small_legacy_memory_is_inlined_unchanged(self):
        legacy = '# Old project\n\n## Custom heading\n- Existing fact.\n'
        memory = self.root / 'PROJECT_MEMORY.md'
        memory.write_text(legacy)
        self.assertIn('<PROJECT_MEMORY.md>\n' + legacy + '</PROJECT_MEMORY.md>', self.run_hook())
        self.assertEqual(memory.read_text(), legacy)

    def test_nested_start_uses_git_root(self):
        self.git('init')
        (self.root / 'PROJECT_MEMORY.md').write_text('ROOT FACT\n')
        nested = self.root / 'nested'
        nested.mkdir()
        (nested / 'PROJECT_MEMORY.md').write_text('WRONG FILE\n')
        out = self.run_hook(nested)
        self.assertIn('ROOT FACT', out)
        self.assertNotIn('WRONG FILE', out)

    def test_explicit_project_directory_takes_precedence(self):
        self.git('init')
        (self.root / 'PROJECT_MEMORY.md').write_text('EXPLICIT ROOT\n')
        nested = self.root / 'nested'
        nested.mkdir()
        other = self.root / 'outside'
        other.mkdir()
        self.assertIn('EXPLICIT ROOT', self.run_hook(other, CLAUDE_PROJECT_DIR=str(nested)))

    def test_large_file_is_pointed_to_without_inlining(self):
        memory = self.root / 'PROJECT_MEMORY.md'
        memory.write_text('LARGE FACT\n' * 900)
        out = self.run_hook()
        self.assertIn(str(memory), out)
        self.assertNotIn('LARGE FACT', out)
        self.assertIn('overview', out)

    def test_inline_boundary_is_8192_bytes(self):
        memory = self.root / 'PROJECT_MEMORY.md'
        memory.write_text('x' * 8192)
        self.assertIn('<PROJECT_MEMORY.md>', self.run_hook())
        memory.write_text('x' * 8193)
        self.assertNotIn('<PROJECT_MEMORY.md>', self.run_hook())

    def test_missing_file_nudge_can_be_silenced_and_creates_nothing(self):
        self.assertIn('No PROJECT_MEMORY.md', self.run_hook())
        self.assertEqual(self.run_hook(PROJECT_MEMORY_NUDGE='0'), '')
        self.assertEqual(list(self.root.iterdir()), [])

    def test_git_failure_falls_back_to_start_directory(self):
        tools = self.root / 'tools'
        tools.mkdir()
        git = tools / 'git'
        git.write_text('#!/bin/sh\nexit 127\n')
        git.chmod(0o755)
        (self.root / 'PROJECT_MEMORY.md').write_text('FALLBACK FACT\n')
        self.assertIn('FALLBACK FACT', self.run_hook(PATH=str(tools) + os.pathsep + os.environ['PATH']))

    def test_worktree_has_its_own_memory(self):
        self.git('init')
        self.git('-c', 'user.name=Memory Test', '-c', 'user.email=memory@example.invalid',
                 'commit', '--allow-empty', '-m', 'Initial')
        worktree = self.root / 'checkout'
        self.git('worktree', 'add', '-b', 'memory-test', str(worktree))
        (self.root / 'PROJECT_MEMORY.md').write_text('MAIN CHECKOUT\n')
        (worktree / 'PROJECT_MEMORY.md').write_text('WORKTREE FACT\n')
        nested = worktree / 'nested'
        nested.mkdir()
        out = self.run_hook(nested)
        self.assertIn('WORKTREE FACT', out)
        self.assertNotIn('MAIN CHECKOUT', out)

    def test_nested_repository_is_not_parent_repository(self):
        self.git('init')
        (self.root / 'PROJECT_MEMORY.md').write_text('PARENT FACT\n')
        nested = self.root / 'nested-repo'
        nested.mkdir()
        self.git('-C', str(nested), 'init')
        (nested / 'PROJECT_MEMORY.md').write_text('INNER FACT\n')
        out = self.run_hook(nested)
        self.assertIn('INNER FACT', out)
        self.assertNotIn('PARENT FACT', out)


if __name__ == '__main__':
    unittest.main()
