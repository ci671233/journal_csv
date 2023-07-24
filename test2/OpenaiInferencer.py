import openai

class OpenaiInferencer:
    def __init__(self, key):
        openai.api_key = key

    def infer(self, text):
        # 텍스트에서 사사표기 여부를 판별합니다.
        try:
            response = openai.Completion.create(engine="text-davinci-002", prompt=text, max_tokens=60)
        except Exception as e:
            print(f"Error occurred while inferring from OpenAI: {e}")
            return None

        return response.choices[0].text.strip()