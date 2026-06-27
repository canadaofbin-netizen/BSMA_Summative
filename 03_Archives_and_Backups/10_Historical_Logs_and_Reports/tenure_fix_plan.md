# [Goal Description]

Correct a severe data entry error regarding the "Tenure" variable in Liu et al. (2018). The previous coder conflated Mean and SD from Table 1, and subsequently made an arbitrary mathematical conversion (months to years) to generate `1.56`, violating core extraction rules.

## Proposed Changes

1. **Table Over Text Execution:** The author's Table 1 explicitly states Tenure has Mean = 2.83 and SD = 18.77. Even though this seems conceptually backwards (and contradicts the text's 20.83), our `04_general_exceptions.md` rule strictly mandates **Table Over Text**.
2. **No Arbitrary Conversions:** We must extract the exact number as reported in the table (2.83) rather than dividing by 12. 
3. **Excel Correction:** Update Column 25 (Org Tenure) for rows 16-22 to `2.83`. Update Column 47 (SD) for the Tenure row to `18.77` if it was extracted as a correlate (which it wasn't, it's just a demographic here).
