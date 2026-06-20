"""
Tests for spec-trace — the one-spec convention linter.

Two layers:
  Unit tests        — isolated checks using temp directories and fixture files
  Integration tests — run against the actual features/ worked examples in this repo
"""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
SCRIPT = REPO_ROOT / 'spec-trace'
FEATURES_DIR = REPO_ROOT / 'features'


def run_check(features_dir: Path):
    """Run 'spec-trace check' against a directory. Returns (exit_code, stdout)."""
    result = subprocess.run(
        [sys.executable, str(SCRIPT), 'check', '--features-dir', str(features_dir)],
        capture_output=True,
        text=True,
    )
    return result.returncode, result.stdout


# ---------------------------------------------------------------------------
# Helpers for building fixture files
# ---------------------------------------------------------------------------

def write_requirements(folder: Path, ids=('F1-S1',), approved=False):
    lines = []
    for id_ in ids:
        lines += [f'### {id_}', 'Given x', 'When y', 'Then z', '']
    if approved:
        lines.append('<!-- Reviewer note (product reviewer): Approved. -->')
    (folder / 'requirements.md').write_text('\n'.join(lines))


def write_validation(folder: Path, ids=('F1-S1',), approved=False):
    lines = []
    for id_ in ids:
        lines += [f'## {id_} → test_{id_.lower().replace("-", "_")}', 'TODO', '']
    if approved:
        lines.append('<!-- Tech lead note: Approved. -->')
    (folder / 'validation.md').write_text('\n'.join(lines))


def write_plan(folder: Path, ids=('F1-S1',)):
    body = '- Component satisfies ' + ', '.join(ids)
    (folder / 'plan.md').write_text(body + '\n')


# ---------------------------------------------------------------------------
# C4: folder numbering
# ---------------------------------------------------------------------------

class TestNumbering(unittest.TestCase):

    def test_single_feature_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            f = d / '01-alpha'; f.mkdir()
            write_requirements(f)
            code, out = run_check(d)
            self.assertEqual(code, 0, msg=out)

    def test_two_contiguous_features_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            for n, name in [('01', 'alpha'), ('02', 'beta')]:
                f = d / f'{n}-{name}'; f.mkdir()
                write_requirements(f)
            code, out = run_check(d)
            self.assertEqual(code, 0, msg=out)

    def test_gap_in_numbering_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            for n, name in [('01', 'alpha'), ('03', 'gamma')]:
                f = d / f'{n}-{name}'; f.mkdir()
                write_requirements(f)
            code, out = run_check(d)
            self.assertEqual(code, 1)
            self.assertIn('numbering gap', out)

    def test_duplicate_number_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            for name in ['alpha', 'beta']:
                f = d / f'01-{name}'; f.mkdir()
                write_requirements(f)
            code, out = run_check(d)
            self.assertEqual(code, 1)
            self.assertIn('duplicate', out)


# ---------------------------------------------------------------------------
# C5: gate state
# ---------------------------------------------------------------------------

class TestGates(unittest.TestCase):

    def test_validation_without_req_approval_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            f = d / '01-feat'; f.mkdir()
            write_requirements(f, approved=False)
            write_validation(f, approved=False)
            code, out = run_check(d)
            self.assertEqual(code, 1)
            self.assertIn('gate 1', out)

    def test_plan_without_val_approval_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            f = d / '01-feat'; f.mkdir()
            write_requirements(f, approved=True)
            write_validation(f, approved=False)
            write_plan(f)
            code, out = run_check(d)
            self.assertEqual(code, 1)
            self.assertIn('gate 2', out)

    def test_req_approved_no_validation_passes(self):
        """A feature with approved requirements.md but no validation.md is valid mid-flow."""
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            f = d / '01-feat'; f.mkdir()
            write_requirements(f, approved=True)
            code, out = run_check(d)
            self.assertEqual(code, 0, msg=out)

    def test_full_approval_chain_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            f = d / '01-feat'; f.mkdir()
            write_requirements(f, approved=True)
            write_validation(f, approved=True)
            write_plan(f)
            code, out = run_check(d)
            self.assertEqual(code, 0, msg=out)


# ---------------------------------------------------------------------------
# C1: coverage (requirements.md → validation.md)
# ---------------------------------------------------------------------------

class TestCoverage(unittest.TestCase):

    def test_missing_stub_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            f = d / '01-feat'; f.mkdir()
            write_requirements(f, ids=('F1-S1', 'F1-S2'), approved=True)
            write_validation(f, ids=('F1-S1',), approved=True)  # F1-S2 missing
            code, out = run_check(d)
            self.assertEqual(code, 1)
            self.assertIn('F1-S2', out)
            self.assertIn('no stub', out)

    def test_all_stubs_present_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            f = d / '01-feat'; f.mkdir()
            write_requirements(f, ids=('F1-S1', 'F1-S2'), approved=True)
            write_validation(f, ids=('F1-S1', 'F1-S2'), approved=True)
            code, out = run_check(d)
            self.assertEqual(code, 0, msg=out)

    def test_no_validation_skips_coverage_check(self):
        """Coverage check is skipped when validation.md does not exist yet."""
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            f = d / '01-feat'; f.mkdir()
            write_requirements(f, ids=('F1-S1', 'F1-S2'), approved=False)
            code, out = run_check(d)
            self.assertEqual(code, 0, msg=out)


# ---------------------------------------------------------------------------
# C2: orphans (validation.md / plan.md → requirements.md)
# ---------------------------------------------------------------------------

class TestOrphans(unittest.TestCase):

    def test_orphan_id_in_plan_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            f = d / '01-feat'; f.mkdir()
            write_requirements(f, ids=('F1-S1',), approved=True)
            write_validation(f, ids=('F1-S1',), approved=True)
            write_plan(f, ids=('F1-S1', 'F1-S99'))  # F1-S99 is not in requirements
            code, out = run_check(d)
            self.assertEqual(code, 1)
            self.assertIn('F1-S99', out)
            self.assertIn('orphan', out)

    def test_orphan_id_in_validation_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            f = d / '01-feat'; f.mkdir()
            write_requirements(f, ids=('F1-S1',), approved=True)
            write_validation(f, ids=('F1-S1', 'F1-S99'), approved=True)
            code, out = run_check(d)
            self.assertEqual(code, 1)
            self.assertIn('F1-S99', out)
            self.assertIn('orphan', out)

    def test_cross_feature_reference_passes(self):
        """An ID from Feature 1 referenced in Feature 2's plan is valid."""
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            f1 = d / '01-feat'; f1.mkdir()
            write_requirements(f1, ids=('F1-S1',), approved=True)
            write_validation(f1, ids=('F1-S1',), approved=True)
            f2 = d / '02-feat'; f2.mkdir()
            write_requirements(f2, ids=('F2-S1',), approved=True)
            write_validation(f2, ids=('F2-S1',), approved=True)
            # plan references both F1-S1 and F2-S1 — both exist
            (f2 / 'plan.md').write_text('- Component satisfies F2-S1 (extends F1-S1)\n')
            code, out = run_check(d)
            self.assertEqual(code, 0, msg=out)


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

class TestEdgeCases(unittest.TestCase):

    def test_empty_features_dir_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            code, out = run_check(Path(tmp))
            self.assertEqual(code, 0, msg=out)
            self.assertIn('PASS', out)

    def test_template_folder_is_ignored(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            t = d / '_template'; t.mkdir()
            # Template has placeholder content — should not be linted
            (t / 'requirements.md').write_text('### F<n>-S1\nGiven x\nWhen y\nThen z\n')
            code, out = run_check(d)
            self.assertEqual(code, 0, msg=out)

    def test_missing_features_dir_exits_with_error(self):
        code, out = run_check(Path('/nonexistent/path/features'))
        self.assertEqual(code, 1)


# ---------------------------------------------------------------------------
# Integration: the actual worked examples in this repo
# ---------------------------------------------------------------------------

class TestWorkedExamples(unittest.TestCase):
    """
    Run spec-trace against the real features/ directory.
    These tests make the worked examples self-verifying — if someone edits a
    feature file and breaks the convention, CI catches it here.
    """

    def test_repo_features_pass(self):
        """The full features/ directory always satisfies spec-trace."""
        code, out = run_check(FEATURES_DIR)
        self.assertEqual(code, 0, msg=out)

    def test_feature_and_scenario_count(self):
        """Two features, six scenarios total (F1: 3, F2: 3)."""
        _, out = run_check(FEATURES_DIR)
        self.assertIn('2 feature(s)', out)
        self.assertIn('6 scenario(s)', out)

    def test_feature1_all_files_present(self):
        """Feature 1 is fully complete — all three files exist."""
        f1 = FEATURES_DIR / '01-infection-spread'
        self.assertTrue((f1 / 'requirements.md').exists())
        self.assertTrue((f1 / 'validation.md').exists())
        self.assertTrue((f1 / 'plan.md').exists())

    def test_feature1_both_gates_approved(self):
        """Feature 1 has both product reviewer and tech lead approvals."""
        import re
        approved = re.compile(r'<!--.*?Approved.*?-->', re.DOTALL | re.IGNORECASE)
        f1 = FEATURES_DIR / '01-infection-spread'
        req_text = (f1 / 'requirements.md').read_text()
        val_text = (f1 / 'validation.md').read_text()
        self.assertRegex(req_text, approved,
                         msg='Feature 1 requirements.md missing product reviewer approval')
        self.assertRegex(val_text, approved,
                         msg='Feature 1 validation.md missing tech lead approval')

    def test_feature2_awaiting_product_gate(self):
        """Feature 2 is correctly mid-flow: requirements.md exists, gate not yet passed."""
        f2 = FEATURES_DIR / '02-supply-scavenging'
        self.assertTrue((f2 / 'requirements.md').exists())
        self.assertFalse((f2 / 'validation.md').exists(),
                         msg='validation.md should not exist — gate not approved yet')
        self.assertFalse((f2 / 'plan.md').exists())

    def test_feature2_gate_would_be_caught(self):
        """
        If someone created validation.md for Feature 2 without approval,
        spec-trace catches it. Uses a temp copy so the real files are untouched.
        """
        f2_req = (FEATURES_DIR / '02-supply-scavenging' / 'requirements.md').read_text()
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            feat = d / '01-supply-scavenging'; feat.mkdir()
            (feat / 'requirements.md').write_text(f2_req)
            # Bypass the gate — create validation.md without approval in requirements
            (feat / 'validation.md').write_text('## F2-S1 → test_x\nTODO\n')
            code, out = run_check(d)
            self.assertEqual(code, 1)
            self.assertIn('gate 1', out)


if __name__ == '__main__':
    unittest.main()
