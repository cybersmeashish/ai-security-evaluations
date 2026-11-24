import sys,unittest,json
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/"tools"))
from cache_scope import declared_reuse_eligible
class ScopeTests(unittest.TestCase):
 def rows(self):return json.loads((R/"fixtures/pairs.json").read_text())["pairs"]
 def test_same_scope_positive(self):
  p=next(p for p in self.rows() if p["id"]=="equivalent-exact");self.assertTrue(declared_reuse_eligible(p["a"],p["b"]))
 def test_case_or_subject_change_denied(self):
  for p in self.rows():
   if p["id"] in ("different-case","different-subject"):self.assertFalse(declared_reuse_eligible(p["a"],p["b"]))
 def test_epoch_and_release_change_denied(self):
  for p in self.rows():
   if p["id"] in ("different-epoch","different-release"):self.assertFalse(declared_reuse_eligible(p["a"],p["b"]))
 def test_critical_values_change_denied(self):
  for p in self.rows():
   if p["id"] in ("negation","amount","account-number"):self.assertFalse(declared_reuse_eligible(p["a"],p["b"]))
 def test_material_bypass_denied(self):
  p=next(p for p in self.rows() if p["id"]=="material-cache-bypass");self.assertFalse(declared_reuse_eligible(p["a"],p["b"]))
 def test_missing_scope_or_boolean_epoch_denied(self):
  p=next(p for p in self.rows() if p["id"]=="equivalent-exact");a=p["a"];b=dict(p["b"],scope=dict(p["b"]["scope"],epoch=True));self.assertFalse(declared_reuse_eligible(a,b));self.assertFalse(declared_reuse_eligible(a,{}))
