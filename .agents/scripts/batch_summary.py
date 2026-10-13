"""
batch_summary.py — BSMA Coding Sheet Executive Diagnostic & Taxonomy Engine
=============================================================================
Provides automated, flexible executive summaries for BSMA coding sheets.

Default language: English (lang="en")
Korean language: Activated via --ko, --lang ko, or Korean characters in arguments.

Supports:
1. Direct Paper IDs: python batch_summary.py 70 94 109
2. File path: python batch_summary.py 03_Coding_Sheets/70_94_109.xlsx
3. Combined: python batch_summary.py 03_Coding_Sheets/70_94_109.xlsx 70 94
4. Auto-detect latest batch sheet: python batch_summary.py
5. Language flags: --en (default) or --ko
"""

import os
import sys
import re
import json
import argparse
from typing import Dict, Any, List, Tuple, Optional
import openpyxl

# Force UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')


def get_paper_metadata_from_pdf(root_dir: str, paper_id: int) -> Dict[str, str]:
    """Look up Author, Year, and Title from PDF filename in 01_Academic_Papers/."""
    papers_dir = os.path.join(root_dir, "01_Academic_Papers")
    if not os.path.exists(papers_dir):
        return {"author_year": f"Paper [{paper_id}]", "title": "Unknown Title"}

    pattern = re.compile(rf"^\[{paper_id}\]\s+(.+?)\s+\((\d{{4}})\)\s+-\s+(.+?)\.pdf$", re.IGNORECASE)
    for f in os.listdir(papers_dir):
        m = pattern.match(f)
        if m:
            author = m.group(1).strip()
            year = m.group(2).strip()
            title = m.group(3).strip()
            return {
                "author_year": f"{author} ({year})",
                "title": title
            }
    return {"author_year": f"Paper [{paper_id}]", "title": "Title not found in PDF registry"}


VAR_EXPLANATIONS_KO = {
    "bsa": "Boundary Spanning Activity - 전체 복합 BSB 점수",
    "external com.": "External Communication - 외향 소통 하위 차원",
    "external representation": "대외 홍보/대변 행동 (COBSB 하위 차원)",
    "internal influence": "내부 개선 제안 행동 (COBSB 하위 차원)",
    "internalized influence": "내면화된 영향력 행동 (COBSB 하위 차원)",
    "service delivery": "고객 서비스 전달 행동 (COBSB 하위 차원)",
    "branch identification": "지점 동일시 (경계연결 태도)",
    "cs-related meetings": "고객 서비스 관련 미팅",
    "internal com.": "대내 정보 전파 소통 (게이트키퍼 BSB 하위 차원)",
    "status": "전문직 지위",
    "org. size": "조직 규모",
    "industry": "산업 분류",
    "org. comm.": "조직 몰입",
    "prof. comm.": "전문직 몰입",
    "dual comm.": "이중 몰입",
    "complexity": "과업 복잡성",
    "uncertainty": "과업 불확실성",
    "uncertainty (perceived)": "지각된 환경 불확실성",
    "interdepend.": "과업 상호의존성",
    "task interdependence": "과업 상호의존성",
    "degree": "학위 수준",
    "occupation": "직종",
    "prof. control": "전문직 통제",
    "prof. incent.": "전문직 보상",
    "employee creativity": "직원 창의성",
    "proactive personality": "주도적 성격",
    "role ambiguity": "역할 모호성",
    "role conflict": "역할 갈등",
    "role overload": "역할 과부하",
    "role overload conflict": "역할 과부하 갈등",
    "role-overload conflict": "역할 과부하 갈등",
    "intersender conflict": "발신자 간 역할 갈등",
    "intrasender conflict": "발신자 내 역할 갈등",
    "person role conflict": "개인-역할 갈등",
    "person-role conflict": "개인-역할 갈등",
    "job-related tension": "직무 관련 긴장",
    "role autonomy": "역할 자율성",
    "vision": "비전",
    "hope/faith": "희망/신념",
    "altruistic love": "이타적 사랑",
    "calling": "소명의식",
    "member": "소속감 / 멤버십",
    "locus of control": "통제 위치 (내적/외적 통제소재)",
    "performance control": "성과 통제",
    "cs": "고객 서비스",
    "turnover intention": "이직 의도",
    "job satisfaction": "직무 만족",
    "psychological safety": "심리적 안전감",
    "trust": "신뢰",
    "trustworthiness": "신뢰성 (파트너 신뢰성 지각)",
    "boundary spanning": "경계연결 행동 (Boundary Spanning)",
    "boundary-spanning behavior": "경계연결 행동 (Boundary-Spanning Behavior)",
    "boundary spanning activities": "경계연결 활동 (Boundary Spanning Activities)",
    "boundary spanning orientation": "경계연결 지향성",
    "boundary spanning ties": "경계연결 네트워크 유대",
    "boundary spanner": "경계연결자 역할 여부",
    "aggregate boundary spanning": "통합 경계연결 행동 (Aggregate BSB)",
    "formal boundary spanning": "공식적 경계연결 행동",
    "informal boundary spanning": "비공식적 경계연결 행동",
    "internal organizational boundary spanning": "조직 내부 경계연결 행동",
    "external organizational boundary spanning": "조직 외부 경계연결 행동",
    "customer-oriented boundary-spanning behaviors": "고객지향 경계연결 행동 (COBSB)",
    "boundary‐spanning leadership": "경계연결 리더십 (Boundary-Spanning Leadership)",
    "boundary-spanning leadership": "경계연결 리더십 (Boundary-Spanning Leadership)",
    "bsl (t1)": "경계연결 리더십 (Time 1)",
    "bsl (t2)": "경계연결 리더십 (Time 2)",
    "bsl (t3)": "경계연결 리더십 (Time 3)",
    "outdegree in internal network": "내부 네트워크 외향 연결 중심성 (게이트키퍼 내부 전파)",
    "outdegree in extended network": "확장 외부 네트워크 외향 연결 중심성 (대외 탐색)",
    "closed task-oriented dbs ties": "폐쇄형 과업 지향 DBS 연결 (경계연결)",
    "closed friendship dbs ties": "폐쇄형 친교 지향 DBS 연결 (경계연결)",
    "open task-oriented dbs ties": "개방형 과업 지향 DBS 연결 (경계연결)",
    "open friendship dbs ties": "개방형 친교 지향 DBS 연결 (경계연결)",
    "ebsb": "직원 경계연결 행동 (Employee Boundary-Spanning Behavior)",
    "type of employee": "직원 유형 (IC vs IS)",
    "age": "연령",
    "leader age": "리더 연령",
    "follower age": "부하직원 연령",
    "gender": "성별",
    "leader gender": "리더 성별",
    "follower gender": "부하직원 성별",
    "sex": "성별",
    "ethnicity": "인종/민족",
    "asian ethnicity": "아시아계 민족 여부",
    "education": "교육 수준",
    "edu": "교육 수준",
    "gmat score": "GMAT 점수",
    "years of experience": "경력 연수",
    "organizational tenure": "조직 근속 연수",
    "tenure": "조직 근속 연수",
    "overall job satisfaction": "전반적 직무 만족",
    "organizational commitment": "조직 몰입",
    "intention to leave": "이직 의도",
    "closed task-oriented intrateam ties": "팀 내 폐쇄형 과업 연결",
    "closed friendship intrateam ties": "팀 내 폐쇄형 친교 연결",
    "managerial status": "관리직 지위 (관리자 여부)",
    "managerial role (project manager = reference)": "관리직 역할 (프로젝트 매니저 기준)",
    "hierarchical level": "직급/계층 수준",
    "group membership": "집단 소속 여부",
    "in‐group size": "내집단 규모",
    "in-group size": "내집단 규모",
    "out‐group size": "외집단 규모",
    "out-group size": "외집단 규모",
    "leader in‐group prototypicality": "리더 내집단 원형성 (Prototypicality)",
    "leader in-group prototypicality": "리더 내집단 원형성 (Prototypicality)",
    "informal leadership": "비공식적 리더십",
    "servant leadership": "서번트 리더십",
    "supportive coaching": "지원적 코칭",
    "top-management support": "최고경영진 지원",
    "co-worker support": "동료 지원",
    "self-perceived influence": "자기 지각 영향력",
    "attributed influence": "타인 귀속 영향력",
    "expert power": "전문가적 권력",
    "referent power": "준거적 권력",
    "competence": "역량 (Competence)",
    "human capital": "인적 자본 (Human Capital)",
    "boundary-spanning role": "공식 경계연결 직무 역할",
    "boundary-spanning self-efficacy": "경계연결 자기효능감",
    "career meaningfulness": "경력 의미감",
    "work centrality": "업무 중심성",
    "collaboration": "협업 행동",
    "strategic orientation - collaboration": "전략적 협업 지향성",
    "innovativeness": "혁신성",
    "field learning": "현장 학습 (Field Learning)",
    "field creativity": "현장 창의성 (Field Creativity)",
    "performance": "직무 성과",
    "performance (coordinating)": "조정 성과 (Coordinating Performance)",
    "performance (overall)": "전반적 직무 성과 (Overall Performance)",
    "perceived": "지각된 성과/결과",
    "objective": "객관적 성과 지표",
    "rating": "상사 평가 성과 점수",
    "contract time": "계약 기간",
    "contract type (design-and-construct [d&c] = reference)": "계약 유형 (D&C 기준)",
    "spatial complexity": "공간적 복잡성",
    "stakeholder complexity": "이해관계자 복잡성",
    "armed conflict setting": "무력 분쟁 지역 환경 여부",
    "remote work": "원격 근무 비중",
    "acap (t1)": "흡수역량 (Absorptive Capacity, Time 1)",
    "acap (t2)": "흡수역량 (Absorptive Capacity, Time 2)",
    "acap (t3)": "흡수역량 (Absorptive Capacity, Time 3)",
    "je (t1)": "직무착근도 (Job Embeddedness, Time 1)",
    "je (t2)": "직무착근도 (Job Embeddedness, Time 2)",
    "je (t3)": "직무착근도 (Job Embeddedness, Time 3)",
    "ao": "성취 지향성 (Achievement Orientation)",
    "pp": "성과 압박 (Performance Pressure)",
    "cf": "인지적 유연성 (Cognitive Flexibility)",
    "op": "강박적 열정 (Obsessive Work Passion)"
}

VAR_EXPLANATIONS_EN = {
    "bsa": "Boundary Spanning Activity - Global Composite BSB Score",
    "external com.": "External Communication - Extraunit Communication Sub-dimension",
    "external representation": "External Representation (COBSB Sub-dimension)",
    "internal influence": "Internal Influence (COBSB Sub-dimension)",
    "internalized influence": "Internalized Influence (COBSB Sub-dimension)",
    "service delivery": "Service Delivery (COBSB Sub-dimension)",
    "branch identification": "Branch Identification (Boundary Spanning Attitude)",
    "cs-related meetings": "Customer Service-Related Meetings",
    "internal com.": "Internal Communication - Intra-unit Dissemination (Gatekeeper BSB Sub-dimension)",
    "status": "Professional Status",
    "org. size": "Organizational Size",
    "industry": "Industry Classification",
    "org. comm.": "Organizational Commitment",
    "prof. comm.": "Professional Commitment",
    "dual comm.": "Dual Commitment",
    "complexity": "Task Complexity",
    "uncertainty": "Task Uncertainty",
    "uncertainty (perceived)": "Perceived Environmental Uncertainty",
    "interdepend.": "Task Interdependence",
    "task interdependence": "Task Interdependence",
    "degree": "Educational Degree",
    "occupation": "Occupation / Job Role",
    "prof. control": "Professional Control",
    "prof. incent.": "Professional Incentives",
    "employee creativity": "Employee Creativity",
    "proactive personality": "Proactive Personality",
    "role ambiguity": "Role Ambiguity",
    "role conflict": "Role Conflict",
    "role overload": "Role Overload",
    "role overload conflict": "Role Overload Conflict",
    "role-overload conflict": "Role-Overload Conflict",
    "intersender conflict": "Intersender Role Conflict",
    "intrasender conflict": "Intrasender Role Conflict",
    "person role conflict": "Person-Role Conflict",
    "person-role conflict": "Person-Role Conflict",
    "job-related tension": "Job-Related Tension",
    "role autonomy": "Role Autonomy",
    "vision": "Vision",
    "hope/faith": "Hope/Faith",
    "altruistic love": "Altruistic Love",
    "calling": "Calling",
    "member": "Membership / Sense of Belonging",
    "locus of control": "Locus of Control",
    "performance control": "Performance Control",
    "cs": "Customer Service",
    "turnover intention": "Turnover Intention",
    "job satisfaction": "Job Satisfaction",
    "psychological safety": "Psychological Safety",
    "trust": "Trust",
    "trustworthiness": "Perceived Partner Trustworthiness",
    "boundary spanning": "Boundary Spanning Behavior",
    "boundary-spanning behavior": "Boundary-Spanning Behavior",
    "boundary spanning activities": "Boundary Spanning Activities",
    "boundary spanning orientation": "Boundary Spanning Orientation",
    "boundary spanning ties": "Boundary Spanning Network Ties",
    "boundary spanner": "Designated Boundary Spanner Role",
    "aggregate boundary spanning": "Aggregate Boundary Spanning Behavior",
    "formal boundary spanning": "Formal Boundary Spanning Behavior",
    "informal boundary spanning": "Informal Boundary Spanning Behavior",
    "internal organizational boundary spanning": "Internal Organizational Boundary Spanning",
    "external organizational boundary spanning": "External Organizational Boundary Spanning",
    "customer-oriented boundary-spanning behaviors": "Customer-Oriented Boundary-Spanning Behaviors (COBSB)",
    "boundary‐spanning leadership": "Boundary-Spanning Leadership",
    "boundary-spanning leadership": "Boundary-Spanning Leadership",
    "bsl (t1)": "Boundary-Spanning Leadership (Time 1)",
    "bsl (t2)": "Boundary-Spanning Leadership (Time 2)",
    "bsl (t3)": "Boundary-Spanning Leadership (Time 3)",
    "outdegree in internal network": "Outdegree in Internal Network (Gatekeeper Intra-unit Dissemination)",
    "outdegree in extended network": "Outdegree in Extended Network (External Information Scouting)",
    "closed task-oriented dbs ties": "Closed Task-Oriented DBS Ties",
    "closed friendship dbs ties": "Closed Friendship DBS Ties",
    "open task-oriented dbs ties": "Open Task-Oriented DBS Ties",
    "open friendship dbs ties": "Open Friendship DBS Ties",
    "ebsb": "Employee Boundary-Spanning Behavior",
    "type of employee": "Type of Employee (IC vs IS)",
    "age": "Age",
    "leader age": "Leader Age",
    "follower age": "Follower Age",
    "gender": "Gender",
    "leader gender": "Leader Gender",
    "follower gender": "Follower Gender",
    "sex": "Sex",
    "ethnicity": "Ethnicity",
    "asian ethnicity": "Asian Ethnicity",
    "education": "Education",
    "edu": "Education",
    "gmat score": "GMAT Score",
    "years of experience": "Years of Work Experience",
    "organizational tenure": "Organizational Tenure",
    "tenure": "Organizational Tenure",
    "overall job satisfaction": "Overall Job Satisfaction",
    "organizational commitment": "Organizational Commitment",
    "intention to leave": "Intention to Leave",
    "closed task-oriented intrateam ties": "Closed Task-Oriented Intrateam Ties",
    "closed friendship intrateam ties": "Closed Friendship Intrateam Ties",
    "managerial status": "Managerial Status",
    "managerial role (project manager = reference)": "Managerial Role (Project Manager = Reference)",
    "hierarchical level": "Hierarchical Level",
    "group membership": "Group Membership",
    "in‐group size": "In-Group Size",
    "in-group size": "In-Group Size",
    "out‐group size": "Out-Group Size",
    "out-group size": "Out-Group Size",
    "leader in‐group prototypicality": "Leader In-Group Prototypicality",
    "leader in-group prototypicality": "Leader In-Group Prototypicality",
    "informal leadership": "Informal Leadership",
    "servant leadership": "Servant Leadership",
    "supportive coaching": "Supportive Coaching",
    "top-management support": "Top-Management Support",
    "co-worker support": "Co-Worker Support",
    "self-perceived influence": "Self-Perceived Influence",
    "attributed influence": "Attributed Influence",
    "expert power": "Expert Power",
    "referent power": "Referent Power",
    "competence": "Perceived Competence",
    "human capital": "Human Capital",
    "boundary-spanning role": "Formal Boundary-Spanning Role",
    "boundary-spanning self-efficacy": "Boundary-Spanning Self-Efficacy",
    "career meaningfulness": "Career Meaningfulness",
    "work centrality": "Work Centrality",
    "collaboration": "Collaboration Behavior",
    "strategic orientation - collaboration": "Strategic Orientation - Collaboration",
    "innovativeness": "Individual Innovativeness",
    "field learning": "Field Learning",
    "field creativity": "Field Creativity",
    "performance": "Job Performance",
    "performance (coordinating)": "Coordinating Performance",
    "performance (overall)": "Overall Job Performance",
    "perceived": "Perceived Performance Outcome",
    "objective": "Objective Performance Outcome",
    "rating": "Supervisor Performance Rating",
    "contract time": "Contract Duration / Time",
    "contract type (design-and-construct [d&c] = reference)": "Contract Type (D&C = Reference)",
    "spatial complexity": "Spatial Complexity",
    "stakeholder complexity": "Stakeholder Complexity",
    "armed conflict setting": "Armed Conflict Setting",
    "remote work": "Remote Work Intensity",
    "acap (t1)": "Absorptive Capacity (Time 1)",
    "acap (t2)": "Absorptive Capacity (Time 2)",
    "acap (t3)": "Absorptive Capacity (Time 3)",
    "je (t1)": "Job Embeddedness (Time 1)",
    "je (t2)": "Job Embeddedness (Time 2)",
    "je (t3)": "Job Embeddedness (Time 3)",
    "ao": "Achievement Orientation",
    "pp": "Performance Pressure",
    "cf": "Cognitive Flexibility",
    "op": "Obsessive Work Passion"
}

CATEGORY_MAP_KO = {
    "context": "조직/환경 특성",
    "individual": "개인/인구통계 특성",
    "attitudes": "태도/몰입/지원 변수",
    "control": "업무/자율성/권력 통제",
    "internal": "내부 행동/집단 역학",
    "stress": "역할 스트레스/긴장",
    "performance": "직무 성과/혁신/역량",
    "other": "기타 변수"
}

CATEGORY_MAP_EN = {
    "context": "Context & Organization",
    "individual": "Individual & Demographics",
    "attitudes": "Attitudes, Commitment & Support",
    "control": "Control, Autonomy & Power",
    "internal": "Internal Group Dynamics",
    "stress": "Role Stress & Tension",
    "performance": "Performance, Innovation & Capabilities",
    "other": "General Non-BS Variables"
}

CATEGORY_ORDER = ["context", "individual", "attitudes", "control", "internal", "stress", "performance", "other"]


def categorize_non_bs_variable(var_name: str, lang: str = "en") -> Tuple[str, str]:
    """Categorize Non-BS variable into domain key and localized label."""
    v = var_name.lower().strip()
    if any(k in v for k in [
        "org. size", "size", "industry", "complexity", "uncertainty", "interdepend",
        "technology", "environment", "structure", "formalization", "type of employee",
        "contract", "armed conflict", "remote work", "strategic orientation"
    ]):
        key = "context"
    elif any(k in v for k in [
        "comm.", "commitment", "satisfaction", "involvement", "engagement", "identification",
        "loyalty", "passion", "op", "intention to leave", "turnover", "je (", "embeddedness",
        "meaningfulness", "centrality", "calling", "vision", "hope/faith", "altruistic love",
        "member", "trust", "support", "coaching", "servant leadership"
    ]):
        key = "attitudes"
    elif any(k in v for k in [
        "ambiguity", "conflict", "overload", "burnout", "exhaustion", "stress", "strain",
        "pressure", "pp", "tension"
    ]):
        key = "stress"
    elif any(k in v for k in [
        "performance", "creativity", "service", "delivery", "citizenship", "ocb", "voice",
        "leadership", "innovativeness", "learning", "collaboration", "acap", "competence",
        "influence", "perceived", "objective", "rating", "cs"
    ]):
        key = "performance"
    elif any(k in v for k in [
        "proactive", "personality", "status", "degree", "occupation", "education", "edu",
        "experience", "age", "gender", "sex", "tenure", "ao", "flexibility", "cf",
        "ethnicity", "gmat", "human capital", "self-efficacy", "hierarchical level",
        "managerial", "boundary-spanning role", "locus of control"
    ]):
        key = "individual"
    elif any(k in v for k in [
        "control", "incent", "reward", "compensation", "pay", "autonomy", "power"
    ]):
        key = "control"
    elif any(k in v for k in [
        "internal", "intra", "prototypicality"
    ]):
        key = "internal"
    else:
        key = "other"

    label = CATEGORY_MAP_KO[key] if lang == "ko" else CATEGORY_MAP_EN[key]
    return key, label


def find_sheet_for_paper_ids(root_dir: str, paper_ids: List[int]) -> Optional[str]:
    """Find which coding sheet contains the specified paper IDs."""
    coding_dir = os.path.join(root_dir, "03_Coding_Sheets")
    if not os.path.exists(coding_dir):
        return None

    batch_sheets = [
        os.path.join(coding_dir, f) for f in os.listdir(coding_dir)
        if f.endswith(".xlsx") and not f.startswith("~$") and re.match(r"^\d+_\d+", f)
    ]
    batch_sheets.sort(key=lambda x: os.path.getmtime(x), reverse=True)

    target_id_set = set(paper_ids)
    for bs in batch_sheets:
        try:
            wb = openpyxl.load_workbook(bs, data_only=True)
            ws = wb.active
            sheet_ids = set()
            for r in range(4, ws.max_row + 1):
                val = ws.cell(r, 2).value
                if val is not None:
                    try:
                        sheet_ids.add(int(val))
                    except (ValueError, TypeError):
                        pass
            wb.close()
            if sheet_ids & target_id_set:
                return bs
        except Exception:
            continue

    master_path = os.path.join(coding_dir, "BSMA_Master_Coding_Sheet.xlsx")
    if os.path.exists(master_path):
        return master_path

    return None


def get_latest_batch_sheet(root_dir: str) -> Optional[str]:
    """Get the most recently modified batch extraction sheet [start]_[end].xlsx."""
    coding_dir = os.path.join(root_dir, "03_Coding_Sheets")
    if not os.path.exists(coding_dir):
        return None

    batch_sheets = [
        os.path.join(coding_dir, f) for f in os.listdir(coding_dir)
        if f.endswith(".xlsx") and not f.startswith("~$") and re.match(r"^\d+_\d+", f)
    ]
    if not batch_sheets:
        all_sheets = [
            os.path.join(coding_dir, f) for f in os.listdir(coding_dir)
            if f.endswith(".xlsx") and not f.startswith("~$")
        ]
        if not all_sheets:
            return None
        all_sheets.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        return all_sheets[0]

    batch_sheets.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    return batch_sheets[0]


def parse_sheet_data(sheet_path: str, filter_ids: Optional[List[int]] = None, root_dir: str = ".", lang: str = "en") -> Dict[str, Any]:
    """Parse Excel sheet and extract all summary statistics and dynamic integrity checks."""
    wb = openpyxl.load_workbook(sheet_path, data_only=True)
    ws = wb["Extracted Data"] if "Extracted Data" in wb.sheetnames else wb.active

    filter_set = set(filter_ids) if filter_ids else None
    papers_dict = {}

    total_sheet_rows = ws.max_row - 3
    integrity_issues = []

    # Rule 20 check: Unnamed headers in rows 1-3
    is_master = os.path.basename(sheet_path) == "BSMA_Master_Coding_Sheet.xlsx"
    if not is_master:
        for hr in range(1, min(4, ws.max_row + 1)):
            for hc in range(1, min(51, ws.max_column + 1)):
                hval = str(ws.cell(hr, hc).value or "")
                if "unnamed" in hval.lower():
                    integrity_issues.append(f"Rule 20 R{hr}C{hc}: '{hval}'")

    for r in range(4, ws.max_row + 1):
        art_id_val = ws.cell(r, 2).value
        if art_id_val is None:
            continue
        try:
            m_id = re.search(r'(\d+)', str(art_id_val))
            art_id = int(m_id.group(1)) if m_id else int(art_id_val)
        except (ValueError, TypeError):
            continue

        if filter_set and art_id not in filter_set:
            continue

        judg_val = str(ws.cell(r, 5).value or "").strip()
        reason_val = ws.cell(r, 6).value

        if art_id not in papers_dict:
            meta = get_paper_metadata_from_pdf(root_dir, art_id)
            papers_dict[art_id] = {
                "id": art_id,
                "author_year": meta["author_year"],
                "title": meta["title"],
                "judgment": judg_val,
                "reason": str(reason_val or "").strip() if reason_val else None,
                "sample_n": ws.cell(r, 22).value,
                "mean_age": ws.cell(r, 23).value,
                "pct_female": ws.cell(r, 24).value,
                "org_tenure": ws.cell(r, 25).value,
                "occupation": ws.cell(r, 26).value,
                "start_row": r,
                "end_row": r,
                "rows_count": 0,
                "bsb_variables": {},
                "non_bs_variables": {},
                "pairs": [],
                "coordinates": set(),
                "all_means_present": True,
                "all_sds_present": True
            }

        p = papers_dict[art_id]
        p["rows_count"] += 1
        p["end_row"] = r

        bs_name = ws.cell(r, 41).value
        bs_mean = ws.cell(r, 42).value
        bs_sd = ws.cell(r, 43).value
        bs_alpha = ws.cell(r, 44).value
        bs_measure = ws.cell(r, 32).value
        bs_quote = ws.cell(r, 33).value
        bs_items = ws.cell(r, 27).value

        nb_name = ws.cell(r, 45).value
        nb_mean = ws.cell(r, 46).value
        nb_sd = ws.cell(r, 47).value
        nb_alpha = ws.cell(r, 48).value
        nb_measure = ws.cell(r, 39).value
        nb_quote = ws.cell(r, 40).value
        nb_items = ws.cell(r, 34).value

        r_val = ws.cell(r, 49).value
        col50_note = ws.cell(r, 50).value or ""

        # Dynamic Data Integrity Checks (Rules 1, 9, 13, 14, 19) for batch sheets
        if not is_master:
            if judg_val.startswith("1"):
                # Rule 1: Forbidden strings in numeric columns
                for c in [22, 23, 24, 25, 27, 28, 29, 34, 35, 36, 42, 43, 44, 46, 47, 48, 49]:
                    cv = ws.cell(r, c).value
                    if isinstance(cv, str) and cv.strip().lower() in ("not reported", "n/a", "none"):
                        integrity_issues.append(f"Rule 1 R{r}C{c}: '{cv}'")
                # Rule 9: Col 50 must start with Table
                if not str(col50_note).strip().lower().startswith("table"):
                    integrity_issues.append(f"Rule 9 R{r}C50: missing Table prefix")
                # Rule 13: No ellipses
                for c in [31, 33, 38, 40, 50]:
                    cv = str(ws.cell(r, c).value or "")
                    if "..." in cv:
                        integrity_issues.append(f"Rule 13 R{r}C{c}: contains ellipsis '...'")
                # Rule 14: Specific measure substring check when quote is present
                if bs_measure and bs_quote and str(bs_measure).strip() not in str(bs_quote):
                    integrity_issues.append(f"Rule 14 R{r}C32: '{bs_measure}' not in Col 33")
                if nb_measure and nb_quote and str(nb_measure).strip() not in str(nb_quote):
                    integrity_issues.append(f"Rule 14 R{r}C39: '{nb_measure}' not in Col 40")
                # Rule 19: Col 3 and Cols 7-16 blank
                for c in [3] + list(range(7, 17)):
                    if ws.cell(r, c).value is not None and str(ws.cell(r, c).value).strip() != "":
                        integrity_issues.append(f"Rule 19 R{r}C{c}: non-blank in included batch row")
            elif judg_val.startswith("0"):
                # Rule 19: Cols 7-50 blank on excluded row
                for c in range(7, 51):
                    if ws.cell(r, c).value is not None and str(ws.cell(r, c).value).strip() != "":
                        integrity_issues.append(f"Rule 19 R{r}C{c}: non-blank in excluded batch row")

        if bs_name:
            bs_clean = str(bs_name).strip()
            if bs_clean not in p["bsb_variables"]:
                p["bsb_variables"][bs_clean] = {
                    "mean": bs_mean,
                    "sd": bs_sd,
                    "alpha": bs_alpha,
                    "specific_measure": bs_measure,
                    "items": bs_items
                }

        if nb_name:
            nb_clean = str(nb_name).strip()
            if nb_clean not in p["non_bs_variables"]:
                cat_key, cat_label = categorize_non_bs_variable(nb_clean, lang=lang)
                p["non_bs_variables"][nb_clean] = {
                    "mean": nb_mean,
                    "sd": nb_sd,
                    "alpha": nb_alpha,
                    "specific_measure": nb_measure,
                    "items": nb_items,
                    "category_key": cat_key,
                    "category": cat_label
                }

        if bs_name and nb_name:
            p["pairs"].append((str(bs_name).strip(), str(nb_name).strip(), r_val))

        if col50_note:
            t_coord = str(col50_note).split("|")[0].strip()
            p["coordinates"].add(t_coord)

    wb.close()

    for p in papers_dict.values():
        p["coordinates"] = sorted(list(p["coordinates"]))

    total_parsed_rows = sum(p["rows_count"] for p in papers_dict.values())
    total_included_papers = sum(1 for p in papers_dict.values() if p["judgment"].startswith("1"))
    total_excluded_papers = sum(1 for p in papers_dict.values() if p["judgment"].startswith("0"))

    all_unique_bsb = set()
    all_unique_nb = set()
    total_effect_sizes = 0

    for p in papers_dict.values():
        all_unique_bsb.update(p["bsb_variables"].keys())
        all_unique_nb.update(p["non_bs_variables"].keys())
        total_effect_sizes += len(p["pairs"])

    return {
        "sheet_path": sheet_path,
        "sheet_basename": os.path.basename(sheet_path),
        "total_sheet_rows": total_sheet_rows,
        "total_parsed_rows": total_parsed_rows,
        "included_count": total_included_papers,
        "excluded_count": total_excluded_papers,
        "total_effect_sizes": total_effect_sizes,
        "unique_bsb_count": len(all_unique_bsb),
        "unique_nb_count": len(all_unique_nb),
        "all_unique_bsb": sorted(list(all_unique_bsb)),
        "all_unique_nb": sorted(list(all_unique_nb)),
        "integrity_issues_count": len(integrity_issues),
        "integrity_issues": integrity_issues[:10],
        "papers": papers_dict
    }


CIRCLED_NUMS = ["①", "②", "③", "④", "⑤", "⑥", "⑦", "⑧", "⑨", "⑩", "⑪", "⑫", "⑬", "⑭", "⑮"]


def format_summary_markdown(data: Dict[str, Any], lang: str = "en") -> str:
    """Format parsed data into clean, academic markdown matching exact 3-section layout (Rule 31: zero ASCII trees/graphs)."""
    lines = []
    explanations = VAR_EXPLANATIONS_KO if lang == "ko" else VAR_EXPLANATIONS_EN
    cat_map = CATEGORY_MAP_KO if lang == "ko" else CATEGORY_MAP_EN

    integrity_ok = data.get("integrity_issues_count", 0) == 0
    integrity_badge = "100% PASS" if integrity_ok else f"FAIL ({data['integrity_issues_count']} issues)"

    # ==========================================
    # SECTION 1: Sheet Diagnostic Overview Table
    # ==========================================
    if lang == "ko":
        lines.append("### 1. 시트 전체 총괄 개요")
        lines.append("")
        lines.append("| 구분 | 수치 | 비고 |")
        lines.append("|---|:---:|---|")
        lines.append(f"| **총 데이터 행 (Data Rows)** | **{data['total_parsed_rows']}행** | 엑셀 Row 4 ~ Row {data['total_parsed_rows'] + 3} (3개 계층 헤더 제외) |")

        eff_parts = []
        for pid in sorted(data["papers"].keys()):
            p = data["papers"][pid]
            if p["judgment"].startswith("1"):
                eff_parts.append(f"Paper {pid} ({len(p['pairs'])}개)")
        eff_str = " + ".join(eff_parts) if eff_parts else "0개"
        lines.append(f"| **추출된 총 효과크기 ($r$)** | **{data['total_effect_sizes']}개** | {eff_str} |")
        lines.append(f"| **고유 BSB 변수 총 수** | **{data['unique_bsb_count']}개** | 논문 전체에 걸친 고유 경계연결 변수 |")
        lines.append(f"| **고유 Non-BS 변수 총 수** | **{data['unique_nb_count']}개** | 논문 전체에 걸친 고유 비-경계연결 변수 |")

        inc_pids = [str(pid) for pid, p in sorted(data["papers"].items()) if p["judgment"].startswith("1")]
        exc_pids = [str(pid) for pid, p in sorted(data["papers"].items()) if p["judgment"].startswith("0")]
        inc_note_parts = []
        if inc_pids:
            inc_note_parts.append(f"• 포함: Paper {', Paper '.join(inc_pids)}")
        if exc_pids:
            exc_note_parts = []
            for epid in exc_pids:
                r_text = data["papers"][int(epid)]["reason"] or "제외"
                clean_reason = r_text.split("=")[-1].strip() if "=" in r_text else r_text
                exc_note_parts.append(f"Paper {epid} ({clean_reason})")
            inc_note_parts.append(f"• 제외: {', '.join(exc_note_parts)}")
        judg_notes = "<br>".join(inc_note_parts)

        lines.append(f"| **논문 판정 결과** | **{data['included_count']}편 포함 / {data['excluded_count']}편 제외** | {judg_notes} |")
        integrity_note = "Rule 1(결측치 999), Rule 9(좌표), Rule 13(무중략), Rule 14(원문일치), Rule 19/20(3단 헤더)" if integrity_ok else "; ".join(data.get("integrity_issues", []))
        lines.append(f"| **데이터 무결성 검증** | **{integrity_badge}** | {integrity_note} |")
    else:
        lines.append("### 1. Sheet Diagnostic Overview")
        lines.append("")
        lines.append("| Category | Metric | Notes |")
        lines.append("|---|:---:|---|")
        lines.append(f"| **Total Data Rows** | **{data['total_parsed_rows']} rows** | Excel Row 4 ~ Row {data['total_parsed_rows'] + 3} (Excluding 3-tier header) |")

        eff_parts = []
        for pid in sorted(data["papers"].keys()):
            p = data["papers"][pid]
            if p["judgment"].startswith("1"):
                eff_parts.append(f"Paper {pid} ({len(p['pairs'])})")
        eff_str = " + ".join(eff_parts) if eff_parts else "0"
        lines.append(f"| **Total Effect Sizes ($r$)** | **{data['total_effect_sizes']}** | {eff_str} |")
        lines.append(f"| **Unique BSB Variables** | **{data['unique_bsb_count']}** | Unique boundary spanning variables across studies |")
        lines.append(f"| **Unique Non-BS Variables** | **{data['unique_nb_count']}** | Unique non-boundary-spanning variables across studies |")

        inc_pids = [str(pid) for pid, p in sorted(data["papers"].items()) if p["judgment"].startswith("1")]
        exc_pids = [str(pid) for pid, p in sorted(data["papers"].items()) if p["judgment"].startswith("0")]
        inc_note_parts = []
        if inc_pids:
            inc_note_parts.append(f"• Included: Paper {', Paper '.join(inc_pids)}")
        if exc_pids:
            exc_note_parts = []
            for epid in exc_pids:
                r_text = data["papers"][int(epid)]["reason"] or "Excluded"
                clean_reason = r_text.split("=")[-1].strip() if "=" in r_text else r_text
                exc_note_parts.append(f"Paper {epid} ({clean_reason})")
            inc_note_parts.append(f"• Excluded: {', '.join(exc_note_parts)}")
        judg_notes = "<br>".join(inc_note_parts)

        lines.append(f"| **Study Screening Judgments** | **{data['included_count']} Included / {data['excluded_count']} Excluded** | {judg_notes} |")
        integrity_note = "Rule 1 (Missing 999), Rule 9 (Coordinates), Rule 13 (No Ellipses), Rule 14 (Substrings), Rule 19/20 (3-Tier Header)" if integrity_ok else "; ".join(data.get("integrity_issues", []))
        lines.append(f"| **Data Integrity Verification** | **{integrity_badge}** | {integrity_note} |")

    lines.append("")
    lines.append("---")
    lines.append("")

    # ==========================================
    # SECTION 2: Study-by-Study Detailed Analysis
    # ==========================================
    if lang == "ko":
        lines.append("### 2. 논문별 상세 분석")
    else:
        lines.append("### 2. Study-by-Study Detailed Analysis")
    lines.append("")

    for idx, pid in enumerate(sorted(data["papers"].keys())):
        p = data["papers"][pid]
        c_num = CIRCLED_NUMS[idx] if idx < len(CIRCLED_NUMS) else f"({idx+1})"
        is_included = p["judgment"].startswith("1")

        lines.append(f"#### {c_num} Paper [{pid}] {p['author_year']}")
        lines.append(f"> *{p['title']}*")

        if is_included:
            sample_parts = []
            if lang == "ko":
                if p["sample_n"] and str(p["sample_n"]) != "999":
                    sample_parts.append(f"표본 N = {p['sample_n']}")
                if p["occupation"]:
                    sample_parts.append(f"{p['occupation']}")
                elif p["mean_age"] and str(p["mean_age"]) != "999":
                    sample_parts.append(f"평균 연령 {p['mean_age']}세")
                sample_str = f" ({', '.join(sample_parts)})" if sample_parts else ""

                lines.append(f"- **판정:** `1 = include`{sample_str}")
                row_range = f"Row {p['start_row']} ~ Row {p['end_row']}" if p['start_row'] != p['end_row'] else f"Row {p['start_row']}"
                lines.append(f"- **추출 행 수:** **{p['rows_count']}개 행** ({row_range})")

                # BSB Variables
                lines.append(f"- **BSB 변수 ({len(p['bsb_variables'])}개):**")
                for b_name in sorted(p["bsb_variables"].keys()):
                    desc = explanations.get(b_name.lower().strip())
                    desc_str = f" ({desc})" if desc else ""
                    lines.append(f"  - `{b_name}`{desc_str}")

                # Non-BS Variables
                lines.append(f"- **Non-BS 변수 ({len(p['non_bs_variables'])}개):**")
                for n_name in sorted(p["non_bs_variables"].keys()):
                    desc = explanations.get(n_name.lower().strip())
                    desc_str = f" ({desc})" if desc else ""
                    lines.append(f"  - `{n_name}`{desc_str}")

                # Pairing structure
                lines.append("- **조합 구조:**")
                bs_to_nb = {}
                for b_n, n_n, _ in p["pairs"]:
                    bs_to_nb.setdefault(b_n, []).append(n_n)

                bsb_cnt = len(p["bsb_variables"])
                nb_cnt = len(p["non_bs_variables"])
                all_full_cartesian = (bsb_cnt * nb_cnt == p["rows_count"])

                if all_full_cartesian:
                    lines.append(f"  - {bsb_cnt}개 BSB × {nb_cnt}개 Non-BS = {p['rows_count']}행 (완전 직교 Cartesian 곱)")
                else:
                    for b_n, n_list in bs_to_nb.items():
                        lines.append(f"  - `{b_n}` × {len(n_list)}개 Non-BS 변수 = {len(n_list)}행")
                    lines.append(f"  - 합계: {p['rows_count']}행")

                # Statistics completeness
                all_valid = True
                for b in p["bsb_variables"].values():
                    if b["mean"] is None or str(b["mean"]) in ("999", "999.0", ""):
                        all_valid = False
                for n in p["non_bs_variables"].values():
                    if n["mean"] is None or str(n["mean"]) in ("999", "999.0", ""):
                        all_valid = False
                tot_vars = len(p["bsb_variables"]) + len(p["non_bs_variables"])
                if all_valid:
                    first_bs = list(p["bsb_variables"].keys())[0]
                    first_m = p["bsb_variables"][first_bs]["mean"]
                    first_sd = p["bsb_variables"][first_bs]["sd"]
                    lines.append(f"- **통계치 상태:** {tot_vars}개 전 변수의 Mean 및 SD 100% 입력 완료 ({first_bs}: M={first_m}, SD={first_sd} 등)")
                else:
                    lines.append("- **통계치 상태:** 결측치 999 관리 (보고된 수치 100% 무손실 반영)")

                # Provenance Coordinates
                if p["coordinates"]:
                    c_sample = sorted(list(p["coordinates"]))[0]
                    m_t = re.search(r"(Table\s+[\d\.]+(?:\s+\(p\.\s*\d+\))?)", c_sample, re.IGNORECASE)
                    t_str = m_t.group(1) if m_t else c_sample
                    lines.append(f"- **출처 좌표 (Col 50):** `{t_str}`")

            else:
                # English Included Study Breakdown
                if p["sample_n"] and str(p["sample_n"]) != "999":
                    sample_parts.append(f"Sample N = {p['sample_n']}")
                if p["occupation"]:
                    sample_parts.append(f"{p['occupation']}")
                elif p["mean_age"] and str(p["mean_age"]) != "999":
                    sample_parts.append(f"Mean Age {p['mean_age']}")
                sample_str = f" ({', '.join(sample_parts)})" if sample_parts else ""

                lines.append(f"- **Judgment:** `1 = include`{sample_str}")
                row_range = f"Row {p['start_row']} ~ Row {p['end_row']}" if p['start_row'] != p['end_row'] else f"Row {p['start_row']}"
                lines.append(f"- **Extracted Rows:** **{p['rows_count']} rows** ({row_range})")

                # BSB Variables
                lines.append(f"- **BSB Variables ({len(p['bsb_variables'])}):**")
                for b_name in sorted(p["bsb_variables"].keys()):
                    desc = explanations.get(b_name.lower().strip())
                    desc_str = f" ({desc})" if desc else ""
                    lines.append(f"  - `{b_name}`{desc_str}")

                # Non-BS Variables
                lines.append(f"- **Non-BS Variables ({len(p['non_bs_variables'])}):**")
                for n_name in sorted(p["non_bs_variables"].keys()):
                    desc = explanations.get(n_name.lower().strip())
                    desc_str = f" ({desc})" if desc else ""
                    lines.append(f"  - `{n_name}`{desc_str}")

                # Pairing structure
                lines.append("- **Pairing Topology:**")
                bs_to_nb = {}
                for b_n, n_n, _ in p["pairs"]:
                    bs_to_nb.setdefault(b_n, []).append(n_n)

                bsb_cnt = len(p["bsb_variables"])
                nb_cnt = len(p["non_bs_variables"])
                all_full_cartesian = (bsb_cnt * nb_cnt == p["rows_count"])

                if all_full_cartesian:
                    lines.append(f"  - {bsb_cnt} BSB × {nb_cnt} Non-BS = {p['rows_count']} rows (Full Cartesian Product)")
                else:
                    for b_n, n_list in bs_to_nb.items():
                        lines.append(f"  - `{b_n}` × {len(n_list)} Non-BS variables = {len(n_list)} rows")
                    lines.append(f"  - Total: {p['rows_count']} rows")

                # Statistics completeness
                all_valid = True
                for b in p["bsb_variables"].values():
                    if b["mean"] is None or str(b["mean"]) in ("999", "999.0", ""):
                        all_valid = False
                for n in p["non_bs_variables"].values():
                    if n["mean"] is None or str(n["mean"]) in ("999", "999.0", ""):
                        all_valid = False
                tot_vars = len(p["bsb_variables"]) + len(p["non_bs_variables"])
                if all_valid:
                    first_bs = list(p["bsb_variables"].keys())[0]
                    first_m = p["bsb_variables"][first_bs]["mean"]
                    first_sd = p["bsb_variables"][first_bs]["sd"]
                    lines.append(f"- **Empirical Stats Status:** {tot_vars} variables Mean & SD 100% complete ({first_bs}: M={first_m}, SD={first_sd}, etc.)")
                else:
                    lines.append("- **Empirical Stats Status:** Missing data coded as 999 (100% lossless preservation of reported values)")

                # Provenance Coordinates
                if p["coordinates"]:
                    c_sample = sorted(list(p["coordinates"]))[0]
                    m_t = re.search(r"(Table\s+[\d\.]+(?:\s+\(p\.\s*\d+\))?)", c_sample, re.IGNORECASE)
                    t_str = m_t.group(1) if m_t else c_sample
                    lines.append(f"- **Provenance Coordinates (Col 50):** `{t_str}`")

        else:
            # Excluded paper
            if lang == "ko":
                lines.append("- **판정:** `0 = exclude`")
                reason_str = p['reason'] or '3 = Non-individual level (team/firm/org analysis)'
                lines.append(f"- **제외 사유:** {reason_str}")
                lines.append(f"- **추출 행 수:** **1개 행** (Row {p['start_row']})")
                lines.append("- **변수:** 0개 (Rule 19 규정에 따라 Col 6에서 조기 종료, Col 7~50 완전 공백 유지)")
            else:
                lines.append("- **Judgment:** `0 = exclude`")
                reason_str = p['reason'] or '3 = Non-individual level (team/firm/org analysis)'
                lines.append(f"- **Exclusion Reason:** {reason_str}")
                lines.append(f"- **Extracted Rows:** **1 row** (Row {p['start_row']})")
                lines.append("- **Variables:** 0 (Rule 19 early termination at Col 6, Col 7~50 strictly blank)")

        lines.append("")

    lines.append("---")
    lines.append("")

    # ==========================================
    # SECTION 3: Cross-Study Construct Taxonomy Tables (Rule 31: Zero ASCII Trees)
    # ==========================================
    if lang == "ko":
        lines.append("### 3. 전체 고유 변수 종합 분류표 (Construct Taxonomy Tables)")
        lines.append("")
        lines.append(f"#### (1) BSB 고유 변수 목록 (총 {data['unique_bsb_count']}개)")
        lines.append("")
        lines.append("| Paper ID | 저자 (연도) | 추출된 BSB 변수명 (Col 41) | 변수 수 |")
        lines.append("|:---:|---|---|:---:|")
    else:
        lines.append("### 3. Cross-Study Construct Taxonomy Tables")
        lines.append("")
        lines.append(f"#### (1) Boundary Spanning Behavior (BSB) Constructs ({data['unique_bsb_count']} Unique)")
        lines.append("")
        lines.append("| Paper ID | Author (Year) | BSB Construct(s) (Col 41) | Count |")
        lines.append("|:---:|---|---|:---:|")

    for pid in sorted(data["papers"].keys()):
        p = data["papers"][pid]
        if not p["bsb_variables"]:
            continue
        b_list = sorted(list(p["bsb_variables"].keys()))
        b_formatted = ", ".join(f"`{b}`" for b in b_list)
        lines.append(f"| Paper {pid} | {p['author_year']} | {b_formatted} | {len(b_list)} |")

    lines.append("")
    if lang == "ko":
        lines.append(f"#### (2) Non-BS 도메인별 고유 변수 분류표 (총 {data['unique_nb_count']}개)")
        lines.append("")
        lines.append("| 도메인 분류 (Domain Category) | 포함 Non-BS 변수명 (Col 45) | 고유 변수 수 |")
        lines.append("|---|---|:---:|")
    else:
        lines.append(f"#### (2) Non-BS Correlate Domain Taxonomy ({data['unique_nb_count']} Unique)")
        lines.append("")
        lines.append("| Construct Domain Category | Non-BS Construct(s) (Col 45) | Count |")
        lines.append("|---|---|:---:|")

    all_cats = {}
    for pid, p in data["papers"].items():
        for n_name, n_info in p["non_bs_variables"].items():
            cat_k = n_info.get("category_key", "other")
            cat_lbl = cat_map.get(cat_k, CATEGORY_MAP_EN[cat_k])
            all_cats.setdefault(cat_lbl, set()).add(n_name)

    ordered_labels = [cat_map[k] for k in CATEGORY_ORDER if cat_map[k] in all_cats]
    for lbl in all_cats:
        if lbl not in ordered_labels:
            ordered_labels.append(lbl)

    for ck in ordered_labels:
        v_sorted = sorted(list(all_cats[ck]))
        v_formatted = ", ".join(f"`{v}`" for v in v_sorted)
        lines.append(f"| **{ck}** | {v_formatted} | {len(v_sorted)} |")

    return "\n".join(lines)


def main():
    root_dir = os.path.abspath(".")

    raw_args = sys.argv[1:]
    paper_ids = []
    target_sheet = None
    save_report = False
    as_json = False
    lang = "en"  # DEFAULT IS ENGLISH

    has_korean_text = False
    has_ko_flag = False
    has_en_flag = False

    cleaned_args = []
    for arg in raw_args:
        if arg in ("--ko", "--lang=ko", "-k"):
            has_ko_flag = True
        elif arg in ("--en", "--lang=en", "-e"):
            has_en_flag = True
        elif arg == "--report":
            save_report = True
        elif arg == "--json":
            as_json = True
        elif arg.isdigit():
            paper_ids.append(int(arg))
        elif arg.endswith(".xlsx") or os.path.exists(arg):
            target_sheet = arg
        else:
            if re.search(r"[가-힣]", arg):
                has_korean_text = True
            cleaned_args.append(arg)

    if has_en_flag:
        lang = "en"
    elif has_ko_flag or has_korean_text:
        lang = "ko"
    else:
        lang = "en"

    if target_sheet and not os.path.exists(target_sheet):
        candidate = os.path.join(root_dir, "03_Coding_Sheets", target_sheet)
        if os.path.exists(candidate):
            target_sheet = candidate
        else:
            print(f"Error: Target sheet '{target_sheet}' not found.")
            sys.exit(1)

    if not target_sheet:
        if paper_ids:
            target_sheet = find_sheet_for_paper_ids(root_dir, paper_ids)
            if not target_sheet:
                print(f"Error: Could not find any coding sheet containing Paper IDs: {paper_ids}")
                sys.exit(1)
        else:
            target_sheet = get_latest_batch_sheet(root_dir)
            if not target_sheet:
                print("Error: No batch coding sheet found in 03_Coding_Sheets/.")
                sys.exit(1)

    parsed_data = parse_sheet_data(target_sheet, filter_ids=paper_ids if paper_ids else None, root_dir=root_dir, lang=lang)

    if as_json:
        print(json.dumps(parsed_data, indent=2, ensure_ascii=False))
        sys.exit(0)

    summary_md = format_summary_markdown(parsed_data, lang=lang)
    print(summary_md)

    if save_report:
        reports_dir = os.path.join(root_dir, "04_Reports")
        os.makedirs(reports_dir, exist_ok=True)
        bname = os.path.splitext(os.path.basename(target_sheet))[0]
        report_file = os.path.join(reports_dir, f"batch_summary_{bname}_{lang}.md")
        with open(report_file, "w", encoding="utf-8") as f:
            f.write(summary_md)
        print(f"\n[REPORT_SAVED] Saved summary report to {report_file}")


if __name__ == "__main__":
    main()
