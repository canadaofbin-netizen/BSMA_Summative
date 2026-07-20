import sys
import os
sys.path.append(r"g:\My Drive\UCL\BSMA\BSMA ANTIGRAVITY\05_Pipeline\1_Include_Exclude_Loop")
from langgraph_main import build_graph
import openpyxl

def main():
    print("Initializing pipeline...")
    pipeline = build_graph()
    
    # Test on a small batch to save time/tokens
    test_articles = ["BSMA0001", "BSMA0002", "BSMA0003", "BSMA0004", "BSMA0005"]
    
    for article_id in test_articles:
        print(f"\n--- Running pipeline for {article_id} ---")
        initial_state = {
            "article_id": article_id,
            "pdf_text": f"Mock PDF text for {article_id}. This is an individual level study with boundary spanning.",
            "verdict_json": None,
            "auditor_feedback": None,
            "is_approved": False,
            "iteration_count": 0,
            "status_msg": "Started"
        }
        
        try:
            final_state = pipeline.invoke(initial_state)
            print(f" Completed {article_id}: {final_state['status_msg']}")
        except Exception as e:
            print(f" Error processing {article_id}: {e}")

if __name__ == "__main__":
    main()
