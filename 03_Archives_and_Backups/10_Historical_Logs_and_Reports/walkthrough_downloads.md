# Walkthrough: Automated Open Access PDF Downloads

This document summarizes the results of the Python script designed to bypass Zotero and download Open Access PDFs directly to your Google Drive.

## 1. What was done
- Created a Python script (`download_pdfs.py`) that read all valid DOIs from `List_of_Articles.xlsx`.
- Interfaced with the **Unpaywall API** to check the open-access status of 683 articles.
- Streamed the actual PDF binary files to a new folder: `G:\My Drive\UCL\BSMA\SUMMATIVE\PDFs`.
- Generated a detailed result tracking sheet: `Download_Result.xlsx`.

## 2. Validation Results
- **Total Valid DOIs Processed**: 683
- **Successfully Downloaded PDFs**: 49 (7.1%)
- **Failed (Paywall/Blocked)**: 634

> [!NOTE]
> The success rate (49 items) accurately reflects the strict limitations of bypassing institutional authentication. These 49 papers are fully open to the public without any subscriptions.

## 3. Next Steps (Manual Downloads)
You will need to manually download the remaining papers that failed due to publisher paywalls.

1. Open `Download_Result.xlsx`.
2. Filter the "Download Status" column for cells containing `Failed`.
3. Open your Naver Whale browser, ensure you are logged into UCL, and use the Zotero Connector extension to capture the paywalled PDFs.
