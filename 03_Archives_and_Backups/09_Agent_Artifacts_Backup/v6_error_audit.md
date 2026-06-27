# v6.xlsx Error Audit: Column Mapping Mistakes

I compared the **actual Excel column headers** (rows 1–3) against the **inserted data** for BSMA0006 (Liu), BSMA0007 (Akaho), and BSMA0008 (Marrone). Here is every mistake I found.

---

## Correct Column Map (from Excel headers)

| Col | Header (Row 3) | What should go here |
|-----|----------------|---------------------|
| 7 | Abstract | Full abstract text |
| 8 | Title | Paper title |
| 9 | Publication Name | Journal name |
| 10 | Authors | Author names |
| 11 | Year | Publication year |
| 19 | Country | Country name |
| 20 | Country (specify) | Country detail |
| 21 | International Context | 1 = No / 2 = Yes |
| 27 | Number of Items (BS) | e.g. 6 |
| 32 | Specific Measure Used (BS) | e.g. "Marrone et al. (2007)" |

---

## Errors Found (All 3 Papers)

### Error 1: Authors → Col 8 (Title) instead of Col 10 (Authors)
| Paper | Col 8 (Title) got | Should have got |
|-------|--------------------|-----------------|
| Liu | `Ting Liu, Tomoki Sekiguchi...` (AUTHORS) | Paper title |
| Marrone | `Jennifer A. Marrone, Paul E. Tesluk...` (AUTHORS) | Paper title |

> [!CAUTION]
> **Authors were written to the Title column.** The script used `row[7]` (0-indexed) = Col 8 for authors, but Col 8 is "Title". Authors belong in **Col 10** (`row[9]`).

### Error 2: Year → Col 9 (Publication Name) instead of Col 11 (Year)
| Paper | Col 9 (Publication Name) got | Should have got |
|-------|-------------------------------|-----------------|
| Liu | `2024` (YEAR) | Journal name |
| Marrone | `2007` (YEAR) | Journal name |

> [!CAUTION]
> **Year was written to Publication Name column.** The script used `row[8]` = Col 9, but Col 9 is "Publication Name". Year belongs in **Col 11** (`row[10]`).

### Error 3: Country → Col 27 (Number of Items) instead of Col 19 (Country)
| Paper | Col 27 (Number of Items, BS) got | Should have got |
|-------|-----------------------------------|-----------------|
| Liu | `China` (COUNTRY) | Number of items, e.g. `3` |
| Marrone | `USA` (COUNTRY) | Number of items |

> [!CAUTION]
> **Country was written to the BS "Number of Items" column.** The script used `row[26]` = Col 27, but Col 27 is "Number of Items" under Measure Descriptors. Country belongs in **Col 19** (`row[18]`).

### Error 4: "1 = No" → Col 21 (International Context) — value format wrong
| Paper | Col 21 got | Should have got |
|-------|------------|-----------------|
| Liu | `1 = No` | `1 = No (domestic only)` |

> [!WARNING]
> The existing data uses the full format `1 = No (domestic only)`. Also, Liu 2024 involves expatriates across multiple countries (China, Laos, Vietnam, Philippines), so this should arguably be `2 = Yes (international)`.

### Error 5: Akaho Effect Size ID mismatch
| Field | Got | Should be |
|-------|-----|-----------|
| Article ID (Col 2) | `BSMA0007` | `BSMA0007` ✓ |
| Effect Size ID (Col 4) | `BSMA0004.1.1` | `BSMA0007.1.1` |

> [!CAUTION]
> The Shadow Report hard-coded `BSMA0004.1.1` as the Effect Size ID. The inserter script blindly copied it instead of auto-generating the correct ID `BSMA0007.1.1`.

### Error 6: Marrone Effect Size IDs mismatch
| Field | Got | Should be |
|-------|-----|-----------|
| Article ID (Col 2) | `BSMA0008` | `BSMA0008` ✓ |
| Effect Size ID (Col 4) | `BSMA0005.1.X` | `BSMA0008.1.X` |

> [!CAUTION]
> Same issue as Akaho — the Shadow Report used a stale `BSMA0005` prefix. The inserter should have overridden this with the correct `BSMA0008` prefix.

### Error 7: Missing columns that existing data has
The existing BSMA0001 row populates these columns, but our inserted rows leave them all blank:

| Col | Header | Existing data example | Our data |
|-----|--------|----------------------|----------|
| 7 | Abstract | Full abstract text | ❌ Empty |
| 8 | Title | Full paper title | ❌ Has authors instead |
| 9 | Publication Name | "Behavioral Sciences" | ❌ Has year instead |
| 17 | Study Design | "1 = Cross-sectional" | ❌ Empty |
| 19 | Country | "South Korea" | ❌ Empty (went to Col 27) |
| 27–33 | BS Measure Descriptors | Items, Min, Max, Report Type, Specific Measure | ❌ Empty (Col 27 has country) |
| 34–40 | Non-BS Measure Descriptors | Items, Min, Max, Report Type, Specific Measure | ❌ Empty |

---

## Root Cause Summary

The v6 inserter script used **0-indexed array positions** that were off by several columns from the actual Excel headers. The core mapping bugs:

```
WRONG (script)          → CORRECT
row[7]  = authors       → row[9]  = authors  (Col 10)
row[8]  = year          → row[10] = year     (Col 11)
row[26] = country       → row[18] = country  (Col 19)
row[20] = intl context  → row[20] = intl context (Col 21) ✓ but wrong value
row[21] = N             → row[21] = N        (Col 22) ✓
row[22] = mean age      → row[22] = mean age (Col 23) ✓
row[23] = % female      → row[23] = % female (Col 24) ✓
row[24] = tenure        → row[24] = tenure   (Col 25) ✓
row[25] = occupation    → row[25] = occupation(Col 26) ✓
```

The offset errors start at Col 7 (Abstract) where the script skips it, causing authors/year to shift into the wrong slots. And country was mapped to a completely wrong section.

---

## Fix Plan

I need to rewrite the column mapping to match the actual Excel structure exactly. Want me to proceed with the fix?
