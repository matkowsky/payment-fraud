"""move_check.py must pass a word-for-word move and fail a loss, a reworded move and a dropped citation."""
import importlib.util
from pathlib import Path
spec = importlib.util.spec_from_file_location('mc', Path(__file__).resolve().parent / 'move_check.py')
mc = importlib.util.module_from_spec(spec); spec.loader.exec_module(mc)

ms = 'Alpha holds in 7 of 9 cases [@Aa2020]. Beta follows Section 5.1 and Supplement S4. Gamma stays here.\n'
sup = 'Old supplement text [@Bb2021].\n'
kept = 'Gamma stays here.\n'

# Word-for-word move, with the two permitted reference forms.
moved, edited, added, problems, _ = mc.compare(ms, kept, sup, sup + 'Alpha holds in 7 of 9 cases [@Aa2020]. Beta follows manuscript Section 5.1 and S4.\n')
assert len(moved) == 2 and not edited and not added and not problems, problems
# Removed and not moved.
assert mc.compare(ms, kept, sup, sup)[3]
# Reworded in the supplement.
assert mc.compare(ms, kept, sup, sup + 'Alpha holds in most cases [@Aa2020]. Beta follows manuscript Section 5.1 and S4.\n')[3]
# Citation dropped from an edited sentence.
m, e, a, p, _ = mc.compare(ms, 'Alpha holds in 7 of 9 cases. Gamma stays here.\n', sup, sup + 'Beta follows manuscript Section 5.1 and S4.\n')
assert e and any('Aa2020' in x for x in p), p
# Number changed in an edited sentence.
m, e, a, p, _ = mc.compare(ms, 'Alpha holds in 8 of 9 cases [@Aa2020]. Gamma stays here.\n', sup, sup + 'Beta follows manuscript Section 5.1 and S4.\n')
assert e and any('number 7' in x for x in p), p
# An edit that keeps every citation and number is reported, not failed.
m, e, a, p, _ = mc.compare(ms, 'Alpha holds in 7 of 9 cases [@Aa2020; @Bb2021]. Gamma stays here.\n', sup, sup + 'Beta follows manuscript Section 5.1 and S4.\n')
assert e and not p, p
# Declared as covered: the quotation must exist and carry the removed sentence's numbers.
sup2 = sup + 'In 7 of 9 cases alpha is true [@Aa2020]. Beta follows manuscript Section 5.1 and S4.\n'
ok = [{'removed': 'Alpha holds in 7 of 9 cases [@Aa2020].', 'covered_by': ['In 7 of 9 cases alpha is true [@Aa2020].']}]
m, e, a, p, c = mc.compare(ms, kept, sup, sup2, ok)
assert c and not p, p
bad_quote = [{'removed': ok[0]['removed'], 'covered_by': ['In most cases alpha is true.']}]
assert mc.compare(ms, kept, sup, sup2, bad_quote)[3]
sup3 = sup + 'Alpha is often true [@Aa2020]. Beta follows manuscript Section 5.1 and S4.\n'
no_number = [{'removed': ok[0]['removed'], 'covered_by': ['Alpha is often true [@Aa2020].']}]
assert any('number' in x for x in mc.compare(ms, kept, sup, sup3, no_number)[3])
not_removed = [{'removed': 'Gamma stays here.', 'covered_by': ['Old supplement text [@Bb2021].']}]
assert any('not removed' in x for x in mc.compare(ms, kept, sup, sup2, ok + not_removed)[3])
# A removed sentence may also be covered by a sentence that stays in the manuscript.
ms2 = 'Gamma stays here. Gamma remains, to repeat.\n'
m_, e_, a_, p_, c_ = mc.compare(ms2, 'Gamma stays here.\n', sup, sup, [{'removed': 'Gamma remains, to repeat.', 'covered_by': ['Gamma stays here.']}])
assert c_ and not p_, p_
# Renumbering: labels change all at once, without chaining, and a moved caption matches its new label.
m = {'Table 1': 'Supplement Table S1.1', 'Table 4': 'Table 1'}
assert mc.renumber('Table 4 and Table 1, not Table 12.', m) == 'Table 1 and Supplement Table S1.1, not Table 12.'
assert mc.as_supplement('**Supplement Table S1.1. Title.**') == '**Table S1.1. Title.**'
print('OK')
