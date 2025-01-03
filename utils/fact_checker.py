import requests
import json

# API key for ClaimBuster
API_KEY = "9936dfa4d6f342119108a5dcc60e19b5"

# Function to check the factuality of a claim
def fact_check(claim):
    """
    Sends a claim to the ClaimBuster API and returns the factuality score.
    """
    # API endpoint
    api_endpoint = f"https://idir.uta.edu/claimbuster/api/v2/score/text/{claim}"
    request_headers = {"x-api-key": API_KEY}
    
    # Send the GET request
    response = requests.get(url=api_endpoint, headers=request_headers)
    
    # Handle the response
    if response.status_code == 200:
        response_data = response.json()
        if "results" in response_data:
            score = response_data["results"]["score"]
            interpretation = interpret_score(score)
            return {
                "score": score,
                "interpretation": interpretation,
                "suggestion": suggest_correction(claim) if score < 0.5 else None,
            }
        else:
            return {"error": "No results available in the response"}
    else:
        return {
            "error": f"Failed to fetch from ClaimBuster. Status code: {response.status_code}",
            "details": response.text,
        }

# Helper function to interpret the score
def interpret_score(score):
    if score > 0.75:
        return "The claim is likely true."
    elif score < 0.25:
        return "The claim is likely false."
    else:
        return "The claim needs further verification."

# Suggest a correction for low-confidence claims
def suggest_correction(claim):
    return "Further verification is needed to provide a correct answer for this claim."
