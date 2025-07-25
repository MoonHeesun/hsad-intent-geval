from src.geval_framework.metric_prompt import (
    SYSTEM_PROMPT,
    ANNOTATION_EVAL_INSTRUCTION_PROMPT,
)
from src.geval_framework.data_model import MetricResult, GEvalResponse
import instructor
from openai import AzureOpenAI
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv(override=True)


class Evaluator:
    def _build_prompt(self, context: str, user_utterances: str, intent_label: str):
        """Build prompt"""
        return ANNOTATION_EVAL_INSTRUCTION_PROMPT.format(
            context=context, user_utterances=user_utterances, intent_label=intent_label
        )

    def _get_instructor_client(self):
        """Get instructor client for structured output"""
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        if azure_endpoint is None:
            raise ValueError("AZURE_ENDPOINT 환경변수가 설정되지 않았습니다.")

        client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            azure_deployment="gpt-4.1",
            api_version="2024-12-01-preview",
            azure_endpoint=azure_endpoint,
        )
        return instructor.from_openai(client)

    def _load_dataset(self):
        """Load dataset"""
        dataset = pd.read_excel("data/eval_dataset.xlsx")

        required_columns = ["context", "user_utterances", "intent_label"]
        missing_columns = [
            col for col in required_columns if col not in dataset.columns
        ]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")

        return dataset

    def evaluate(self, client, prompt: str):
        """Evaluate the prompt"""
        return client.chat.completions.create(
            model="gpt-4.1",
            response_model=MetricResult,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.5,
            max_tokens=1024,
        )

    async def run(self):
        """Evaluate entire dataset"""
        dataset = self._load_dataset()
        client = self._get_instructor_client()

        all_results = []
        total_score = 0
        for idx, row in dataset.iterrows():
            prompt = self._build_prompt(
                context=row["context"],
                user_utterances=row["user_utterances"],
                intent_label=row["intent_label"],
            )

            result = self.evaluate(client=client, prompt=prompt)
            normalized_score = result.score / 3.0  # Normalize 1-5 to 0-1
            total_score += normalized_score

            all_results.append(
                {
                    "index": idx,
                    "context": row["context"],
                    "user_utterances": row["user_utterances"],
                    "intent_label": row["intent_label"],
                    "metric_score": result.score,
                    "metric_explanation": result.reasoning,
                }
            )

            avg_score = total_score / len(all_results) if all_results else 0.0

        return GEvalResponse(
            metric_score=avg_score,
            metric_explanation=f"Evaluated {len(all_results)} samples with average score: {avg_score:.2f}",
            detailed_results=all_results,
        )
