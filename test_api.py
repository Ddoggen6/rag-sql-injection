import requests

API_KEY = "k-19x8jNrIVah62AknOJZIX4kwCvA2E1fxHyORvvoPEUtzUxIx"  # cámbialo
url = "https://api.chatanywhere.tech/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "model": "gpt-4o-mini",
    "messages": [
        {"role": "system", "content": "Eres un asistente útil."},
        {"role": "user", "content": "Di 'Hola, funciona' en una sola línea."}
    ],
    "max_tokens": 20
}

try:
    response = requests.post(url, json=payload, headers=headers)
    print("Status:", response.status_code)
    print("Respuesta:", response.json()["choices"][0]["message"]["content"])
except Exception as e:
    print("Error:", e)
