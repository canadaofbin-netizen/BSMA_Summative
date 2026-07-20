"""
Unit tests for swarm_inject_v3.py security layers.
Tests contamination detection, truncation detection, and JSON repair.
"""
import sys
sys.path.insert(0, r"g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\.agents\skills\include_exclude_pipeline\scripts")

from swarm_inject_v3 import check_contamination, detect_truncation, attempt_json_repair, normalize_keys, validate_schema

# ============================================================
# TEST 1: Contamination Detection
# ============================================================
print("=" * 60)
print("TEST 1: Contamination Detection")
print("=" * 60)

# 1a: Clean text - should pass
clean = "This paper uses qualitative interviews. [Abstract] \"We conducted semi-structured interviews with 33 rural journalists.\""
result = check_contamination(clean, "TEST_CLEAN")
assert result == [], f"FAIL: Clean text flagged: {result}"
print("  1a: Clean text → PASS (no contamination)")

# 1b: System tag bleed - should catch
dirty1 = 'Excluded because qualitative study. </SYSTEM_MESSAGE>'
result = check_contamination(dirty1, "TEST_DIRTY1")
assert len(result) > 0, "FAIL: System tag not detected"
print(f"  1b: System tag bleed → PASS (detected: {result})")

# 1c: Escaped newline bleed - should catch
dirty2 = 'Some evidence\\nwith escaped newlines'
result = check_contamination(dirty2, "TEST_DIRTY2")
assert len(result) > 0, "FAIL: Escaped newline not detected"
print(f"  1c: Escaped newline → PASS (detected: {result})")

# 1d: step_index bleed - should catch
dirty3 = 'Evidence text "step_index": 5'
result = check_contamination(dirty3, "TEST_DIRTY3")
assert len(result) > 0, "FAIL: step_index not detected"
print(f"  1d: JSON key bleed → PASS (detected: {result})")

# ============================================================
# TEST 2: Truncation Detection
# ============================================================
print("\n" + "=" * 60)
print("TEST 2: Truncation Detection")
print("=" * 60)

# 2a: Complete JSON - no truncation
complete = '{"BSMA_ID": "BSMA0001", "Verdict": 0, "Exclusion_Code": 1, "Reasoning": "test", "Verbatim_Evidence": "test"}'
result = detect_truncation(complete, "TEST_COMPLETE")
assert result == [], f"FAIL: Complete JSON flagged: {result}"
print("  2a: Complete JSON → PASS (no truncation)")

# 2b: Missing closing brace - truncation
truncated1 = '{"BSMA_ID": "BSMA0001", "Verdict": 0, "Exclusion_Code": 1, "Reasoning": "test", "Verbatim_Evidence": "some long text that got cut off'
result = detect_truncation(truncated1, "TEST_TRUNCATED1")
assert len(result) > 0, "FAIL: Truncation not detected"
print(f"  2b: Missing brace → PASS (detected: {result})")

# 2c: Missing Verdict field - truncation
truncated2 = '{"BSMA_ID": "BSMA0001"'
result = detect_truncation(truncated2, "TEST_TRUNCATED2")
assert len(result) > 0, "FAIL: Missing Verdict not detected"
print(f"  2c: Missing Verdict → PASS (detected: {result})")

# ============================================================
# TEST 3: JSON Auto-Repair
# ============================================================
print("\n" + "=" * 60)
print("TEST 3: JSON Auto-Repair")
print("=" * 60)

# 3a: Truncated at Verbatim_Evidence - should repair
truncated_json = '{"BSMA_ID": "BSMA0042", "Verdict": 0, "Exclusion_Code": 1, "Reasoning": "Qualitative study", "Verbatim_Evidence": "Some evidence that got cut off here'
data = attempt_json_repair(truncated_json, "TEST_REPAIR1")
assert data is not None, "FAIL: Repair returned None"
assert data["Verdict"] == 0, "FAIL: Verdict lost"
assert data["Exclusion_Code"] == 1, "FAIL: Exclusion_Code lost"
assert "[TRUNCATED BY TOKEN LIMIT]" in data["Verbatim_Evidence"], "FAIL: Truncation marker not added"
print(f"  3a: Truncated evidence → PASS (Verdict={data['Verdict']}, Code={data['Exclusion_Code']})")
print(f"       Evidence ends with: ...{data['Verbatim_Evidence'][-40:]}")

# 3b: Truncated before Verdict - should fail repair
truncated_early = '{"BSMA_ID": "BSMA0042", "Ver'
data = attempt_json_repair(truncated_early, "TEST_REPAIR2")
assert data is None, "FAIL: Should have failed (missing critical fields)"
print("  3b: Truncated before Verdict → PASS (correctly returned None)")

# ============================================================
# TEST 4: Key Normalization
# ============================================================
print("\n" + "=" * 60)
print("TEST 4: Key Normalization (Alias Mapping)")
print("=" * 60)

old_format = {"BSMA_ID": "BSMA0001", "status": "0 = Exclude", "reason_code": 1, "reason_summary": "Qualitative", "verbatim": "Some quote"}
normalized = normalize_keys(old_format)
assert "Verdict" in normalized, "FAIL: status not mapped to Verdict"
assert "Exclusion_Code" in normalized, "FAIL: reason_code not mapped"
assert "Verbatim_Evidence" in normalized, "FAIL: verbatim not mapped"
print(f"  4a: Old format keys → PASS (mapped to: {list(normalized.keys())})")

# ============================================================
# ALL TESTS PASSED
# ============================================================
print("\n" + "=" * 60)
print("ALL TESTS PASSED ✅")
print("=" * 60)
