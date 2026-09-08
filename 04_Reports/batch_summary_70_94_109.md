### 1. 시트 전체 총괄 개요

| 구분 | 수치 | 비고 |
|---|:---:|---|
| **총 데이터 행 (Data Rows)** | **40행** | 엑셀 Row 4 ~ Row 43 (3개 계층 헤더 제외) |
| **추출된 총 효과크기 ($r$)** | **39개** | Paper 70 (27개) + Paper 94 (12개) |
| **고유 BSB 변수 총 수** | **5개** | 논문 전체에 걸친 고유 경계연결 변수 |
| **고유 Non-BS 변수 총 수** | **18개** | 논문 전체에 걸친 고유 비-경계연결 변수 |
| **논문 판정 결과** | **2편 포함 / 1편 제외** | • 포함: Paper 70, Paper 94<br>• 제외: Paper 109 (Non-individual level (team/firm/org analysis)) |
| **데이터 무결성 검증** | **100% PASS** | Rule 1(결측치 999), Rule 20(3단 헤더), Rule 27(무손실 파리티) |

---

### 2. 논문별 상세 분석

#### ① Paper [70] Sexton (1995)
> *Dual commitment and boundary spanning activity of R&D professionals*
- **판정:** `1 = include` (표본 N = 253, R&D technical professionals)
- **추출 행 수:** **27개 행** (Row 4 ~ Row 30)
- **BSB 변수 (2개):**
  - `BSA` (Boundary Spanning Activity - 전체 복합 BSB 점수)
  - `External Com.` (External Communication - 외향 소통 하위 차원)
- **Non-BS 변수 (14개):**
  - `Complexity` (과업 복잡성)
  - `Degree` (학위 수준)
  - `Dual Comm.` (이중 몰입)
  - `Industry` (산업 분류)
  - `Interdepend.` (과업 상호의존성)
  - `Internal Com.` (내향 소통 — 내부 부서 내 소통으로 NB 분류)
  - `Occupation` (직종)
  - `Org. Comm.` (조직 몰입)
  - `Org. Size` (조직 규모)
  - `Prof. Comm.` (전문직 몰입)
  - `Prof. Control` (전문직 통제)
  - `Prof. Incent.` (전문직 보상)
  - `Status` (전문직 지위)
  - `Uncertainty` (과업 불확실성)
- **조합 구조:**
  - `BSA` × 13개 Non-BS 변수 = 13행 (BSA 자체의 구성 요소인 Internal Com. 제외)
  - `External Com.` × 14개 Non-BS 변수 (Internal Com. 포함) = 14행
  - 합계: 27행
- **통계치 상태:** 16개 전 변수의 Mean 및 SD 100% 입력 완료 (BSA: M=50.51, SD=21.54 등)
- **출처 좌표 (Col 50):** `Table 3.9 (p. 65)`

#### ② Paper [94] Chien et al. (2021)
> *Hotel frontline service employees’ creativity and customer-oriented boundary-spanning*
- **판정:** `1 = include` (표본 N = 382, Hotel frontline service employees)
- **추출 행 수:** **12개 행** (Row 31 ~ Row 42)
- **BSB 변수 (3개):**
  - `External Representation` (대외 홍보/대변 행동)
  - `Internal Influence` (내부 개선 제안 행동)
  - `Service Delivery` (고객 서비스 전달 행동)
- **Non-BS 변수 (4개):**
  - `Employee Creativity` (직원 창의성)
  - `Proactive Personality` (주도적 성격)
  - `Role Ambiguity` (역할 모호성)
  - `Role Conflict` (역할 갈등)
- **조합 구조:**
  - 3개 BSB × 4개 Non-BS = 12행 (완전 직교 Cartesian 곱)
- **통계치 상태:** 7개 전 변수의 Mean 및 SD 100% 입력 완료 (External Representation: M=5.46, SD=0.8 등)
- **출처 좌표 (Col 50):** `Table 2 (p. 28)`

#### ③ Paper [109] Cummings (2004)
> *Work Groups, Structural Diversity, and Knowledge Sharing in a Global Organization*
- **판정:** `0 = exclude`
- **제외 사유:** 3 = Non-individual level (team/firm/org analysis)
- **추출 행 수:** **1개 행** (Row 43)
- **변수:** 0개 (Rule 19 규정에 따라 Col 6에서 조기 종료, Col 7~50 완전 공백 유지)

---

### 3. 전체 고유 변수 종합 마스터 리스트

```text
[BSB Variables — 총 5개]
├── Paper 70: BSA, External Com.
└── Paper 94: External Representation, Internal Influence, Service Delivery

[Non-BS Variables — 총 18개]
├── 조직/환경 특성: Complexity, Industry, Interdepend., Org. Size, Uncertainty
├── 개인/인구통계 특성: Degree, Occupation, Proactive Personality, Status
├── 태도/몰입 변수: Dual Comm., Org. Comm., Prof. Comm.
├── 업무/조직 통제: Prof. Control, Prof. Incent.
├── 내부 행동/소통: Internal Com.
├── 역할 스트레스: Role Ambiguity, Role Conflict
└── 직무 성과: Employee Creativity
```