# Implementation Plan: Subagent-Assisted Measure Extraction

## Goal Description
You correctly pointed out that manually extracting the measure descriptors (Items, Min, Max, Report Type, Specific Measure) for *every single non-boundary-spanning variable* is tedious and prone to omission, which is exactly why the subagent architecture was established. 

Now that the server restart is complete and API quotas have reset, I will deploy subagents to parallelize this granular data extraction for the Liu (2024) and Marrone (2007) papers and inject the missing data into Columns 34-39.

## Proposed Workflow

### 1. Launch Extraction Subagents
I will invoke two parallel subagents (one for Liu 2024, one for Marrone 2007). 
Their specific prompt will be to read the `Measures` section of their assigned PDF and return a structured JSON mapping for every variable present in the correlation matrix:
```json
{
  "Variable Name": {
    "Number of Items": 8,
    "Min Score": 1,
    "Max Score": 7,
    "Report Type": "1 = Self-report",
    "Report Type Note": "Rated by expatriate",
    "Specific Measure Used": "Chen et al. (2001)"
  }
}
```

### 2. Subagent Data Processing
Once the subagents return the JSON mappings for all variables (e.g., *Mutual Trust, Role Stressors, Emotional Exhaustion* for Liu; *Role Overload, Self-Efficacy* for Marrone), I will collect and verify the JSON data.

### 3. Excel Injection (v8 Generation)
I will write a Python script that loads `BSMA_Actual Coding Sheet_v7.xlsx`, iterates through every row we just created, looks up the `Non-BS Variable Name` (Col 45) in the subagent's JSON mapping, and populates Columns 34-39 accordingly. 
The output will be saved as `BSMA_Actual Coding Sheet_v8.xlsx`.

## User Review Required
> [!IMPORTANT]
> **Subagent Delegation**
> Deploying subagents will ensure we capture the precise scale information for every single variable without manual fatigue. Please click **Proceed** to authorize the launch of the subagents for this task.
