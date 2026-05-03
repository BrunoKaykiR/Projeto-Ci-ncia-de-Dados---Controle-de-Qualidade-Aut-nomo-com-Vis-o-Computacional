# To run this code you need to install the following dependencies:
# pip install google-genai

import os
from google import genai
from google.genai import types


def generate():
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = "gemini-3-flash-preview"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="""INSERT_INPUT_HERE"""),
            ],
        ),
    ]
    tools = [
        types.Tool(googleSearch=types.GoogleSearch(
        )),
    ]
    generate_content_config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            thinking_level="HIGH",
        ),
        tools=tools,
        system_instruction=[
            types.Part.from_text(text="""Você é um sistema autônomo de Visão Computacional para controle de qualidade na Indústria 4.0. Sua tarefa é analisar imagens de garrafas de vidro em uma esteira de envase. Você deve classificar a imagem em uma destas 4 categorias: 'good' (íntegra), 'broken_large' (quebra estrutural severa), 'broken_small' (pequenas lascas ou fissuras) ou 'contamination' (sujeira ou líquidos estranhos no fundo). Responda APENAS com o nome exato da categoria em minúsculo."""),
        ],
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        if text := chunk.text:
            print(text, end="")

if __name__ == "__main__":
    generate()


