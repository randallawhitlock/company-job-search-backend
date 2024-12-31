from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all origins (for development)

# Replace with your actual API key and CSE ID
GOOGLE_CSE_API_KEY = os.environ.get("GOOGLE_CSE_API_KEY")
GOOGLE_CSE_ID = os.environ.get("GOOGLE_CSE_ID")

@app.route("/search")
def search():
    keyword = request.args.get("keyword")
    if not keyword:
        return jsonify({"error": "Keyword is required"}), 400

    base_url = "https://www.googleapis.com/customsearch/v1"
    results = []

    for site_pattern in [
        "boards.greenhouse.io",
        "jobs.lever.co",
        "*.wd1.myworkdayjobs.com",
        "*.wd3.myworkdayjobs.com",
        "*.wd5.myworkdayjobs.com",
        "*.taleo.net",
        "careers.*.icims.com",
        "jobs.jobvite.com",
        "careers.smartrecruiters.com",
        "career*.successfactors.com",
        "*.brassring.com",
        "*.bamboohr.com/careers",
        "*.ashbyhq.com/careers",
        "apply.workable.com",
        "*.recruitee.com",
    ]:
        url = (
            f"{base_url}?key={GOOGLE_CSE_API_KEY}&cx={GOOGLE_CSE_ID}"
            f"&q={keyword} inurl:{site_pattern}"
        )

        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for bad status codes
            data = response.json()

            if "items" in data:
                for item in data["items"]:
                    results.append(
                        {
                            "title": item["title"],
                            "link": item["link"],
                            "source": site_pattern,
                        }
                    )
        except requests.exceptions.RequestException as e:
            print(f"Error searching {site_pattern}: {e}")
            return jsonify({"error": f"Error searching {site_pattern}"}), 500

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)  # Use a production server in deployment