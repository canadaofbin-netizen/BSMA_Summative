import json
import sys
sys.path.append(r".agents\scripts")
from universal_excel_inserter import insert_data

data = {
    "article_id": "278",
    "title": "The Effects of Centrifugal and Centripetal Forces on Product Development Speed and Quality",
    "author": "Kwaku Atuahene-Gima",
    "year": 2003,
    "inclusion_status": 0,
    "exclusion_code": 3,
    "exclusion_reason": "Non-individual level (team/firm/org analysis). Verbatim Evidence: \"I asked two team members in each participating project to provide a single consensual rating for the measures of these forces. I selected the team members upon the advice of senior managers who deemed them as being highly knowledgeable about their projects.\" (Measures and Validation)"
}

insert_data("BSMA_Master_Coding_Sheet.xlsx", data)
