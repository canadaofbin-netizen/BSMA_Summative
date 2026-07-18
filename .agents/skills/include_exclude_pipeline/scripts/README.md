# BSMA End-to-End Automation Pipeline

This directory contains the Python modules required to automate the paper screening, Excel injection, COM highlighting, and Git backup process with a single command.

## How to use

If you have downloaded a batch of new PDF papers, place them in a folder (e.g., `../new_pdfs`).

Then, open your terminal (Command Prompt or VSCode Terminal) in the `BSMA ANTIGRAVITY` directory and run:

```bash
python pipeline/run_pipeline.py --folder ./new_pdfs --batch_size 50
```

## Modules Breakdown

1. **`run_pipeline.py`**: The master orchestrator.
2. **`module_1_pdf_loader.py`**: Scans the input folder and chunks PDFs into batches.
3. **`module_2_agent_dispatcher.py`**: Connects to the LLM API to process the papers. *(Note: Requires OpenAI/Gemini API key setup in a real production environment. Currently stubbed for architecture demo.)*
4. **`module_3_excel_injector.py`**: Uses `openpyxl` to fast-write the AI results into `BSMA_Master_Coding_Sheet.xlsx` within 1 second.
5. **`module_4_com_highlighter.py`**: Uses `win32com` to gracefully parse the newly inserted text and apply red/bold highlights to keywords.
6. **`module_5_git_sync.py`**: Automatically pushes the changes to GitHub.

## Hybrid Mode (No API Key Required)

If you don't want to use an API key inside Python, you can use the **Agentic Hybrid** method:
1. Upload the new PDFs to the Chat AI (Antigravity).
2. Tell the AI: `"Here are 50 papers. Deploy subagents to screen them according to the rulebook, save the JSON, and run the pipeline from Module 3 to Module 5."`
3. The AI will do the heavy lifting using its native free API access, and then use your local Python scripts to do the Excel/Git work.
