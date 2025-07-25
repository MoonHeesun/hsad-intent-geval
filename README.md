# HSAD Intent G-Eval

가상화폐 거래소 관련 사용자 발화의 의도(intent) 레이블링 품질을 자동으로 평가하는 LLM 기반 평가 프레임워크입니다.

## 개요

이 프로젝트는 G-Eval 프레임워크를 기반으로 하여, GPT-4를 평가자로 활용해 의도 분류 레이블의 품질을 자동으로 평가합니다. 특히 가상화폐 거래소 도메인에서 브랜드/서비스와 상품(코인)을 정확히 구분하는 능력을 중점적으로 평가합니다.

## 주요 기능

- **LLM 기반 자동 평가**: Azure OpenAI GPT-4를 사용한 의도 레이블 품질 평가
- **구조화된 출력**: instructor 라이브러리를 통한 일관된 평가 결과 생성
- **다중 반복 실행**: 평가의 일관성 검증을 위한 n회 반복 평가 지원
- **유연한 출력 형식**: JSON 및 Excel 형식으로 결과 저장 가능
- **정규화된 점수**: 1-3점 척도 평가를 0-1 범위로 정규화

## 설치

### 요구사항

- Python 3.13 이상
- Azure OpenAI API 액세스

### 의존성 설치

```bash
# uv를 사용하는 경우
uv pip install -r pyproject.toml

# 또는 pip를 사용하는 경우
pip install dotenv instructor openai openpyxl pandas pydantic
```

### 환경 설정

`.env` 파일을 프로젝트 루트에 생성하고 다음 환경 변수를 설정합니다:

```env
AZURE_OPENAI_ENDPOINT=your_azure_endpoint
AZURE_OPENAI_DEPLOYMENT=your_deployment_name
AZURE_OPENAI_API_VERSION=your_api_version
AZURE_OPENAI_API_KEY=your_api_key
```

## 사용법

### 기본 실행

```bash
python main.py
```

실행 시 다음 정보를 입력하게 됩니다:
- 평가 반복 횟수 (기본값: 5)
- 결과 저장 형식: json 또는 excel (기본값: json)

### 데이터 형식

평가할 데이터는 `data/eval_dataset.xlsx` 파일에 다음 컬럼을 포함해야 합니다:
- `context`: 대화 맥락
- `user_utterances`: 사용자 발화
- `intent_label`: 평가할 의도 레이블

## 프로젝트 구조

```
hsad-intent-geval/
├── data/               # 평가 데이터셋
├── results/            # 평가 결과 저장
├── src/
│   ├── geval.py       # 비동기 실행 래퍼
│   └── geval_framework/
│       ├── data_model.py      # Pydantic 데이터 모델
│       ├── llm_as_a_judge.py  # 핵심 평가 로직
│       └── metric_prompt.py   # 평가 프롬프트
└── main.py            # 엔트리 포인트
```

## 평가 기준

평가는 1-3점 척도로 이루어지며, 다음 기준을 따릅니다:

- **3점 (우수)**: 의도가 정확히 파악되고 브랜드/상품 구분이 명확
- **2점 (보통)**: 기본적인 의도는 파악했으나 세부사항이 부족
- **1점 (미흡)**: 의도 파악이 부정확하거나 누락됨

최종 점수는 0-1 범위로 정규화됩니다: `(점수 - 1) / 2`

## 출력 예시

평가 결과는 다음과 같은 구조로 저장됩니다:

```json
{
  "iterations": [
    {
      "iteration": 1,
      "results": [...],
      "average_score": 0.75
    }
  ],
  "overall_average": 0.76,
  "timestamp": "2025-07-24T16:49:59"
}
```

## 라이선스

이 프로젝트는 내부 사용을 위해 개발되었습니다.
