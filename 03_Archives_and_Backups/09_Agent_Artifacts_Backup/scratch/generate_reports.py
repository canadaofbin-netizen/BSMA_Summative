import os

reports_dir = r'g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\03_Shadow_Reports'
os.makedirs(reports_dir, exist_ok=True)

# ----------------
# 1. Akaho 2024
# ----------------
akaho_md = """# Akaho 2024 Shadow Report
| Effect Size ID | Inclusion-Exclusion Judgment | Reason for Exclusion |
|---|---|---|
| BSMA0004.1.1 | 0 = Exclude | 4 = Non-primary study / Theoretical paper proposing a hypothesis rather than testing empirical correlations. |
"""
with open(os.path.join(reports_dir, 'Akaho_2024_Shadow_Report.md'), 'w', encoding='utf-8') as f:
    f.write(akaho_md)

# ----------------
# 2. Marrone 2007 (Level 1 Matrix: 6x6)
# ----------------
# N = 190, 186, 190, 182, 177, 186
# Matrix:
# 1. Boundary-spanning behavior (Mean 2.91, SD 0.70)
# 2. Boundary-spanning role (Mean 3.09, SD 0.82)
# 3. Boundary-spanning self-efficacy (Mean 4.07, SD 0.69)
# 4. Asian ethnicity (Mean 0.31, SD 0.46)
# 5. GMAT score (Mean 653.90, SD 57.89)
# 6. Role overload (Mean 2.47, SD 0.85)
# Alphas: none reported on diagonal, use 999.

marrone_vars = [
    ("Boundary-spanning behavior", 190, 2.91, 0.70, 999),
    ("Boundary-spanning role", 186, 3.09, 0.82, 999),
    ("Boundary-spanning self-efficacy", 190, 4.07, 0.69, 999),
    ("Asian ethnicity", 182, 0.31, 0.46, 999),
    ("GMAT score", 177, 653.90, 57.89, 999),
    ("Role overload", 186, 2.47, 0.85, 999)
]

marrone_corrs = {
    (2,1): .40,
    (3,1): .25, (3,2): .25,
    (4,1): -.23, (4,2): .08, (4,3): .05,
    (5,1): -.19, (5,2): .14, (5,3): .16, (5,4): .18,
    (6,1): -.04, (6,2): .02, (6,3): .25, (6,4): .13, (6,5): .01
}

marrone_md = """# Marrone 2007 Shadow Report
| Effect Size ID | Measure Descriptors | Variable 1 | Variable 2 | Sample Size | Mean 1 | SD 1 | Alpha 1 | Mean 2 | SD 2 | Alpha 2 | r |
|---|---|---|---|---|---|---|---|---|---|---|---|
"""
effect_id = 1
for i in range(1, 7):
    for j in range(1, i):
        v1 = marrone_vars[i-1]
        v2 = marrone_vars[j-1]
        r = marrone_corrs[(i, j)]
        # For N, taking the smaller of the two Ns to be conservative
        n = min(v1[1], v2[1])
        row = f"| BSMA0005.1.{effect_id} | USA | {v1[0]} | {v2[0]} | {n} | {v1[2]} | {v1[3]} | {v1[4]} | {v2[2]} | {v2[3]} | {v2[4]} | {r} |\n"
        marrone_md += row
        effect_id += 1

with open(os.path.join(reports_dir, 'Marrone_2007_Shadow_Report.md'), 'w', encoding='utf-8') as f:
    f.write(marrone_md)

# ----------------
# 3. Liu 2024 (12x12 Matrix)
# ----------------
liu_vars = [
    ("Expatriates’ boundary-spanning", 5.27, 0.74, 0.96),
    ("Functional boundary-spanning", 5.51, 0.77, 0.91),
    ("Linguistic boundary-spanning", 5.04, 1.03, 0.94),
    ("Cultural boundary-spanning", 5.22, 0.83, 0.95),
    ("Mutual trust", 5.25, 0.68, 0.90),
    ("Cognition-based mutual trust", 5.38, 0.64, 0.80),
    ("Affect-based mutual trust", 5.11, 0.81, 0.87),
    ("Role stressors", 3.64, 0.97, 0.93),
    ("Expatriates’ subsidiary identification", 5.30, 0.95, 0.92),
    ("Coworkers’ MNE identification", 5.08, 1.06, 0.90),
    ("Expatriates’ emotional exhaustion", 3.63, 1.49, 0.97),
    ("Expatriates’ outgroup categorization", 4.35, 0.97, 0.83)
]
liu_matrix = [
    [], # 1
    [0.79], # 2
    [0.84, 0.42], # 3
    [0.94, 0.64, 0.74], # 4
    [0.71, 0.55, 0.55, 0.70], # 5
    [0.63, 0.53, 0.47, 0.62, 0.94], # 6
    [0.70, 0.51, 0.57, 0.70, 0.95, 0.78], # 7
    [0.42, 0.40, 0.27, 0.40, 0.14, 0.09, 0.17], # 8
    [0.45, 0.36, 0.36, 0.43, 0.46, 0.42, 0.46, 0.18], # 9
    [0.52, 0.35, 0.45, 0.52, 0.57, 0.54, 0.53, 0.03, 0.27], # 10
    [-0.01, 0.19, -0.15, -0.05, -0.19, -0.12, -0.24, 0.38, -0.21, -0.21], # 11
    [0.25, 0.36, 0.06, 0.22, 0.08, 0.09, 0.07, 0.44, 0.12, -0.03, 0.28] # 12
]

liu_md = """# Liu 2024 Shadow Report
| Effect Size ID | Measure Descriptors | Variable 1 | Variable 2 | Sample Size | Mean 1 | SD 1 | Alpha 1 | Mean 2 | SD 2 | Alpha 2 | r |
|---|---|---|---|---|---|---|---|---|---|---|---|
"""
effect_id = 1
for i in range(1, 13):
    for j in range(1, i):
        v1 = liu_vars[i-1]
        v2 = liu_vars[j-1]
        r = liu_matrix[i-1][j-1]
        # N for Liu 2024: The text says "responses from 61 team leaders and 292 team members were valid finally" -> using 292 for N
        row = f"| BSMA0006.1.{effect_id} | China | {v1[0]} | {v2[0]} | 292 | {v1[1]} | {v1[2]} | {v1[3]} | {v2[1]} | {v2[2]} | {v2[3]} | {r} |\n"
        liu_md += row
        effect_id += 1

with open(os.path.join(reports_dir, 'Liu_2024_Shadow_Report.md'), 'w', encoding='utf-8') as f:
    f.write(liu_md)

print("Shadow reports generated successfully!")
