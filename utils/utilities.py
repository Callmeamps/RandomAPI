import os
from dotenv import load_dotenv

from openai import OpenAI
from langchain.utilities import SerpAPIWrapper

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY')

search = SerpAPIWrapper()

chatgpt = "gpt-3.5-turbo-1106"

client = OpenAI(api_key=OPENAI_API_KEY)

def completion(system, user):
        request = client.chat.completions.create(
        model=chatgpt,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ]
    )
        res = request.choices[0].message
        return res

def json_completion(system, user, seed=None):
        request = client.chat.completions.create(
        model=chatgpt,
        seed=seed,
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": f"{system}\nYour response must be in JSON."},
            {"role": "user", "content": user}
        ]
    )
        res = request.choices[0].message
        return res

def image_gen(prompt, model="dall-e-3", _number=1):
    response = client.images.generate(
        model=model,
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=_number,
        )

    image_url = response.data[0].url
    return image_url

if __name__ == '__main__':
    pass
