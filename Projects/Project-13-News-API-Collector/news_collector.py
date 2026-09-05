import os
import json
from pathlib import Path
import requests
from dotenv import load_dotenv

# ============================================================
# PROJECT 13 - NEWS API DATA COLLECTOR
# ============================================================
# Learning Concepts:
# 1. Environment variables (.env) & API Key security
# 2. HTTP GET requests using the 'requests' library
# 3. Parsing JSON string into Python dictionary using json.loads()
# 4. Extracting and transforming nested data fields
# 5. Converting Python data back into formatted JSON using json.dumps()
# ============================================================


def collect_news():
    print("=" * 40)
    print("NEWS API COLLECTOR")
    print("=" * 40)

    # --------------------------------------------------------
    # STEP 1: LOAD & VALIDATE API KEY
    # --------------------------------------------------------
    # Locate the .env file in the same folder as this script
    script_dir = Path(__file__).parent
    env_path = script_dir / ".env"
    load_dotenv(dotenv_path=env_path)

    api_key = os.getenv("NEWS_API_KEY")

    # Beginner-friendly validation: ensure API key exists and is not the placeholder
    if not api_key or api_key.strip() == "" or api_key.strip() == "YOUR_API_KEY_HERE":
        print("\n[Configuration Error] NewsAPI key is missing!")
        print("Please follow these steps:")
        print("1. Open the '.env' file in 'Projects/Project-13-News-API-Collector/'")
        print("2. Replace 'YOUR_API_KEY_HERE' with your actual NewsAPI key:")
        print("   NEWS_API_KEY=your_actual_key_here")
        print("3. Re-run this program.")
        print("\nGet a free key at: https://newsapi.org/register")
        print("=" * 40)
        return

    # --------------------------------------------------------
    # STEP 2: CONFIGURE THE GET REQUEST
    # --------------------------------------------------------
    # Official NewsAPI v2 top-headlines endpoint
    endpoint = "https://newsapi.org/v2/top-headlines"

    # Query parameters - easy to modify later
    country = "us"
    page_size = 20

    params = {
        "country": country,
        "pageSize": page_size,
        "apiKey": api_key,
    }

    print("\nFetching top headlines...")

    # --------------------------------------------------------
    # STEP 3: SEND GET REQUEST (requests library)
    # --------------------------------------------------------
    try:
        response = requests.get(endpoint, params=params, timeout=10)
    except requests.exceptions.Timeout:
        print("[Network Error] The request timed out. Please check your internet connection.")
        return
    except requests.exceptions.ConnectionError:
        print("[Network Error] Could not connect to NewsAPI. Check your network or DNS settings.")
        return
    except requests.exceptions.RequestException as error:
        print(f"[Network Error] An unexpected network error occurred: {error}")
        return

    # --------------------------------------------------------
    # STEP 4: INTERPRET RESPONSE AS JSON (json.loads)
    # --------------------------------------------------------
    # Here we demonstrate json.loads():
    # Converting the raw JSON string (response.text) into a Python dictionary
    try:
        data = json.loads(response.text)
    except json.JSONDecodeError as error:
        print(f"[JSON Error] Failed to parse API response as JSON: {error}")
        return

    # --------------------------------------------------------
    # STEP 5: HANDLE API-LEVEL RESPONSES & ERRORS
    # --------------------------------------------------------
    # Check if the API returned an error status code or status == 'error'
    if response.status_code != 200 or data.get("status") != "ok":
        error_code = data.get("code", "unknown_error")
        error_message = data.get("message", f"HTTP Status {response.status_code}")
        print(f"\n[API Error] Request unsuccessful!")
        print(f"Status Code : {response.status_code}")
        print(f"Error Code  : {error_code}")
        print(f"Message     : {error_message}")
        return

    print("\nRequest successful.")

    # --------------------------------------------------------
    # STEP 6: RESPONSE PARSING & FIELD EXTRACTION
    # --------------------------------------------------------
    raw_articles = data.get("articles", [])
    if not isinstance(raw_articles, list):
        print("[Data Error] Unexpected response structure: 'articles' list is missing.")
        return

    articles_count = len(raw_articles)
    print(f"Articles received: {articles_count}")

    cleaned_articles = []
    for article in raw_articles:
        # Extract source name safely
        source_data = article.get("source") or {}
        source_name = source_data.get("name") or "Unknown"

        # Extract only the clean, useful fields
        extracted = {
            "source": source_name,
            "author": article.get("author") or "Unknown",
            "title": article.get("title") or "No Title",
            "description": article.get("description") or "No Description",
            "url": article.get("url") or "",
            "publishedAt": article.get("publishedAt") or "",
        }
        cleaned_articles.append(extracted)

    # Build the final structured dictionary
    structured_news = {
        "status": "ok",
        "totalResults": len(cleaned_articles),
        "articles": cleaned_articles,
    }

    # --------------------------------------------------------
    # STEP 7: SAVE STRUCTURED DATA TO news.json (json.dumps)
    # --------------------------------------------------------
    # Here we demonstrate json.dumps():
    # Converting the Python dictionary into a formatted JSON string with indentation
    output_filepath = script_dir / "news.json"
    print("\nSaving articles to news.json...")

    try:
        formatted_json = json.dumps(structured_news, indent=4)
        output_filepath.write_text(formatted_json, encoding="utf-8")
    except OSError as error:
        print(f"[File Error] Failed to write to {output_filepath}: {error}")
        return

    print("Done.")
    print("News data saved successfully.")

    # --------------------------------------------------------
    # STEP 8: DISPLAY A SUMMARY IN TERMINAL
    # --------------------------------------------------------
    print("\n" + "=" * 40)
    print("SUMMARY OF TOP HEADLINES")
    print("=" * 40)
    print(f"Total articles saved: {len(cleaned_articles)}")

    # Show the first few article titles as a quick preview
    preview_limit = min(5, len(cleaned_articles))
    print(f"\nFirst {preview_limit} Headline Previews:")
    for index, article in enumerate(cleaned_articles[:preview_limit], start=1):
        print(f"{index}. {article['title']}")
        print(f"   Source: {article['source']} | Published: {article['publishedAt']}")

    print("=" * 40)


if __name__ == "__main__":
    collect_news()
