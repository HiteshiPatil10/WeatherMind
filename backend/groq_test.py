import os
from dotenv import load_dotenv

# debug import to show clear error if package missing or API changed
try:
    from groq import Groq, BadRequestError
except Exception as e:
    print("Failed to import Groq:", repr(e))
    raise

load_dotenv()  # loads .env from current working directory

api_key = os.getenv("GROQ_API_KEY")
print("GROQ_API_KEY present?", bool(api_key))

if not api_key:
    raise RuntimeError("GROQ_API_KEY not found. Add it to your .env or environment variables.")

# read model from env so you can change without editing code
model = os.getenv("GROQ_MODEL")
if not model:
    raise RuntimeError("GROQ_MODEL not set. Set GROQ_MODEL in your .env to a supported model (see https://console.groq.com/docs/deprecations).")

client = Groq(api_key=api_key)

try:
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": "Say hello in one line"}]
    )
    print(response.choices[0].message.content)
except BadRequestError as e:
    # model decommission / invalid request info will be here
    print("Groq API returned BadRequestError:", e)
    raise
except Exception as e:
    import traceback
    traceback.print_exc()
    print("Error calling Groq API:", repr(e))
