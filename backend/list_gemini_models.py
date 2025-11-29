"""
Utility script to list Gemini models available for your API key.

Usage (from project root, in your venv):

    cd backend
    python list_gemini_models.py
"""
import os

from dotenv import load_dotenv
import google.generativeai as genai


def main() -> None:
    # Ensure we load backend/.env like the app does
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY is not set in the environment.")
        print("   Set it in backend/.env and run again.")
        return

    genai.configure(api_key=api_key)

    print("🔍 Available Gemini models for this API key")
    print("   (showing only those that support generateContent)\n")

    try:
        for m in genai.list_models():
            methods = getattr(m, "supported_generation_methods", []) or []
            if "generateContent" in methods or "generate_content" in methods:
                print(f"- {m.name}  |  methods={methods}")
    except Exception as e:
        print(f"❌ Error listing models: {e}")


if __name__ == "__main__":
    main()


