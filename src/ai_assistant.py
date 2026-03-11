import json
from openai import OpenAI

client = OpenAI()


def ask_gpt(question, dataset_context, analysis_type="general"):

    system_prompt = """
You are an expert data quality analyst.

Return your response STRICTLY as JSON with this structure:

{
 "executive_summary": "...",
 "direct_answer": "...",
 "findings": ["..."],
 "recommendations": ["..."],
 "next_steps": ["..."]
}

Keep answers concise and professional.
"""

    prompt = f"""
DATASET CONTEXT
{dataset_context}

USER QUESTION
{question}

ANALYSIS TYPE
{analysis_type}
"""

    response = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )

    text = response.output_text

    try:
        return json.loads(text)
    except:
        return {
            "executive_summary": text,
            "direct_answer": text,
            "findings": [],
            "recommendations": [],
            "next_steps": []
        }
