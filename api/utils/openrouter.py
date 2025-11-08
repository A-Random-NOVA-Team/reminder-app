import os

import httpx
from pydantic import BaseModel, Field

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    print(
        "Warning: OPENROUTER_API_KEY environment variable not set. Using default score."
    )
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODEL = "openai/gpt-4o-mini"
# -----------------------------------------------------------------


class TaskDifficultySchema(BaseModel):
    """Schema for the LLM to follow for task difficulty output."""

    difficulty_score: int = Field(
        ge=0,
        le=100,
        description="The estimated difficulty score of the task, where 0 is trivial and 100 is extremely hard.",
    )
    reasoning: str | None = Field(
        None, description="Brief explanation of why this difficulty was chosen."
    )


## 📞 OpenRouter API Caller Function


async def estimate_task_difficulty_full(
    task_name: str, task_description: str, task_deadline: str | None = None
) -> TaskDifficultySchema:
    """
    Calls OpenRouter non-streaming API to get a structured difficulty score (0-100)
    and reasoning, returning the full parsed Pydantic object.
    """

    # Define a default response in case the API key is missing or the API fails
    DEFAULT_SCORE = 30
    DEFAULT_REASONING = "LLM API call failed or key is missing. Default score applied."

    if not OPENROUTER_API_KEY:
        return TaskDifficultySchema(
            difficulty_score=DEFAULT_SCORE, reasoning=DEFAULT_REASONING
        )

    system_prompt = f"""
    You are an expert task analyzer. Your only job is to assess the difficulty
    of a user-provided task and return the result in a strict JSON format that
    conforms to the provided schema.

    The difficulty must be a score from **0 (Trivial)** to **100 (Extremely Difficult)**.
    The score must be an integer.

    Make sure to ONLY respond with a JSON object matching the schema:
    {{
        "difficulty_score": int,
        "reasoning": str | null
    }}

    The task is:
    Name: "{task_name}"
    Description: "{task_description}"
    Deadline: "{task_deadline if task_deadline else 'No deadline provided'}"
    """

    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": "Analyze the task and determine its difficulty score (0-100) and provide reasoning.",
            },
        ],
        "response_format": {"type": "json_object"},
        "stream": False,
        "temperature": 0.1,
    }

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "http://localhost:8000/docs",  # TODO!
        "X-Title": "Task Difficulty API",
        "Content-Type": "application/json",
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                OPENROUTER_BASE_URL, headers=headers, json=payload
            )
            response.raise_for_status()
            response_data = response.json()
            json_content = response_data["choices"][0]["message"]["content"]
            # Hopefully this is a JSON string conforming to TaskDifficultySchema
            parsed_data = TaskDifficultySchema.model_validate_json(json_content)

            return parsed_data

    except httpx.HTTPStatusError as e:
        print(f"OpenRouter API HTTP Error {e.response.status_code}: {e.response.text}")
        return TaskDifficultySchema(
            difficulty_score=DEFAULT_SCORE,
            reasoning=f"OpenRouter API failed with status {e.response.status_code}.",
        )
    except Exception as e:
        print(f"Error calling OpenRouter or parsing response: {e}")
        return TaskDifficultySchema(
            difficulty_score=DEFAULT_SCORE,
            reasoning=f"Internal error during LLM call: {e.__class__.__name__}.",
        )
