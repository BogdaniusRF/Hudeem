import asyncio
import httpx
from mistralai import Mistral
from openai import AsyncOpenAI, completions
import os
from dotenv import load_dotenv
from openai.types import model


#model="gpt-4o-mini"
load_dotenv()
openai_api_key=os.getenv("OPENAI_API_KEY")
proxy=os.getenv("SpaceProxy")
client = AsyncOpenAI(
    api_key=openai_api_key,
    http_client=httpx.AsyncClient(
        transport=httpx.HTTPTransport(
            local_address="0.0.0.0",
            proxy=proxy  # Передаём прокси в transport
        )
    )
)


async def gpt_text(req):
    load_dotenv()
    async with Mistral(
        api_key=os.getenv("MISTRAL_API_KEY", ""),
    ) as mistral:
        completion = await mistral.chat.complete_async(model="mistral-small-latest", messages=[
            {
                "role": "user",
                "content": req,
            },
        ], stream=False)

        # Handle response
        return completion.choices[0].message.content
        print(completion.choices[0].message.content)


async def gpt_embed(req):
    load_dotenv()
    async with Mistral(
        api_key=os.getenv("MISTRAL_API_KEY", ""),
    ) as mistral:
        try:
            completion = await mistral.embeddings.create_async(
                model="mistral-embed",
                inputs=[req]
            )
            embedding = completion.data[0].embedding
            print(f"Сгенерирован вектор длиной: {len(embedding)}")
            return embedding
        except Exception as e:
            raise Exception(f"Ошибка в gpt_embed: {str(e)}")



#####################  For OpenAi testing ##################
async def gpt_openai(req, model):

    completion = await client.chat.completions.create(
        messages=[{"role": "user", "content": req}],
        model=model
    )
    return completion.choices[0].message.content
#####################  For OpenAi testing ##################    
