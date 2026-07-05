import requests

# Tu API key (obtenida de GPT_API_free)
API_KEY = "sk-19x8jNrIVah62AknOJZIX4kwCvA2E1fxHyORvvoPEUtzUxIx"

# Endpoint gratuito
url = "https://api.chatanywhere.tech/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "model": "gpt-4o-mini",   # Puedes usar "deepseek-v3", "deepseek-r1" o "gpt-4o-mini"
    "messages": [
        {"role": "system", "content": "Eres un asistente útil."},
        {"role": "user", "content": "Hola, ¿cómo estás?"}
    ],
    "temperature": 0.7,
    "max_tokens": 100
}

response = requests.post(url, json=payload, headers=headers)

print("Status code:", response.status_code)
print("Respuesta:", response.json()["choices"][0]["message"]["content"])