# HSAD Intent G-Eval

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🎯 프로젝트 개요

HSAD Intent G-Eval은 **가상화폐 거래소 도메인**에서 사용자 발화의 의도(intent) 레이블링 품질을 자동으로 평가하는 **LLM 기반 자동 평가 프레임워크**입니다.

### 핵심 문제 해결
- **도메인 특화 평가**: 가상화폐 거래소 도메인에서 브랜드/서비스와 상품(코인)을 정확히 구분
- **평가 자동화**: 수동 레이블 검증의 시간과 비용 절감
- **일관성 향상**: LLM을 활용한 객관적이고 재현 가능한 평가

### 주요 특징
- 🤖 **Azure OpenAI GPT-4** 기반 평가
- 📊 **구조화된 출력**: Pydantic 모델을 통한 일관된 결과
- 🔄 **다중 반복 평가**: 평가 신뢰도 검증
- 📁 **유연한 출력**: JSON 및 Excel 형식 지원
- 📈 **정규화된 점수**: 1-3점 척도를 0-1 범위로 표준화

## 🚀 빠른 시작

### 사전 요구사항
- Python 3.13 이상
- Azure OpenAI API 액세스 권한
- uv (권장) 또는 pip

### 설치

1. 저장소 클론
```bash
git clone https://github.com/your-org/hsad-intent-geval.git
cd hsad-intent-geval
```

2. 가상환경 생성 (권장)
```bash
# uv 사용 시
uv venv
source .venv/bin/activate  # Linux/Mac
# 또는
.venv\Scripts\activate  # Windows

# 기본 Python venv 사용 시
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 또는
.venv\Scripts\activate  # Windows
```

3. 의존성 설치
```bash
# uv 사용 시
uv pip sync

# pip 사용 시
pip install -r requirements.txt
```

4. 환경 변수 설정
`.env` 파일을 프로젝트 루트에 생성:
```env
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=your-gpt4-deployment-name
AZURE_OPENAI_API_VERSION=2024-02-01
AZURE_OPENAI_API_KEY=your-api-key-here
```

## 📖 사용법

### 기본 실행
```bash
python main.py
```

대화형 프롬프트에서 다음을 입력:
- **평가 반복 횟수**: 기본값 5 (Enter 키로 기본값 사용)
- **출력 형식**: `json` 또는 `excel` (기본값: json)

### 입력 데이터 형식

`data/eval_dataset.xlsx` 파일에 다음 컬럼이 필요합니다:

| 컬럼명 | 설명 | 예시 |
|--------|------|------|
| `context` | 대화 맥락 | "사용자가 비트코인 거래에 대해 문의" |
| `user_utterances` | 사용자 발화 | "비트코인 매수하고 싶어요" |
| `intent_label` | 평가할 의도 레이블 | "coin_trading_buy" |

### 프로그래밍 방식 사용

```python
from src.geval import geval_async_main
import asyncio

# 커스텀 설정으로 실행
results = asyncio.run(geval_async_main(
    input_file="data/custom_dataset.xlsx",
    num_runs=3,
    output_format="json"
))

# 결과 처리
for iteration in results["iterations"]:
    print(f"Iteration {iteration['iteration']}: {iteration['average_score']:.2f}")
```

## 📊 평가 기준

### 점수 체계
- **3점 (우수)**: 의도가 정확히 파악되고 브랜드/상품 구분이 명확
- **2점 (보통)**: 기본적인 의도는 파악했으나 세부사항이 부족  
- **1점 (미흡)**: 의도 파악이 부정확하거나 누락됨

### 점수 정규화
최종 점수는 0-1 범위로 정규화: `normalized_score = (score - 1) / 2`

## 📁 프로젝트 구조

```
hsad-intent-geval/
├── 📂 data/               # 평가 데이터셋
│   └── eval_dataset.xlsx
├── 📂 results/            # 평가 결과 저장
│   ├── *.json
│   └── *.xlsx
├── 📂 src/
│   ├── geval.py          # 비동기 실행 래퍼
│   └── 📂 geval_framework/
│       ├── data_model.py      # Pydantic 데이터 모델
│       ├── llm_as_a_judge.py  # 핵심 평가 로직
│       └── metric_prompt.py   # 평가 프롬프트
├── main.py               # 엔트리 포인트
├── .env                  # 환경 변수 (git ignored)
├── requirements.txt      # pip 의존성
└── pyproject.toml        # uv 프로젝트 설정
```