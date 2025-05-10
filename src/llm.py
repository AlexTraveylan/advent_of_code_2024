import openai
from pydantic import BaseModel

from src.settings import Settings
from src.utils import extract_statement

settings = Settings()


class ResponseFormat(BaseModel):
    response_code_formatted_to_be_copied_in_ide: str
    explanation: str


client = openai.OpenAI(api_key=settings.openai_api_key)


def generate_response_code(statement: str) -> ResponseFormat:
    prompt = f"""
    Langage : Python
    Tu es un assistant qui génère du code pour un problème d'Advent of Code.
    Voici le problème :
    {statement}
    """

    response = client.beta.chat.completions.parse(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format=ResponseFormat,
        timeout=10,
    )

    parsed_response = response.choices[0].message.parsed

    if parsed_response is None:
        raise ValueError("No response from the LLM")

    return parsed_response


if __name__ == "__main__":
    part_1 = extract_statement(1, 1)
    part_2 = extract_statement(1, 2)

    code = generate_response_code(
        f"Part 1:\n{part_1}\n\nPart 2:\n{part_2}. YOU HAVE TO GENERATE THE CODE FOR PART 2 ONLY."
    ).response_code_formatted_to_be_copied_in_ide
    with open("code.py", "w") as f:
        f.write(code)
