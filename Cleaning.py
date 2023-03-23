import requests
import re
import cleanco

GET_URL = "http://localhost:5000/companies"
POST_URL = "http://localhost:5000/companies"

response = requests.get(GET_URL)
companies = response.json()["companies"]

cleanedCompanies = {}
for company in companies:

    name = re.sub(r',.*', '', company["name"])
    name = re.sub(r'\(.*\)', '', name)
    name = re.sub(r'\"', '', name)
    name = re.sub(r'\s-\s', ' ', name)
    name = cleanco.basename(name)
    name = name.title()
    name = re.sub(r'\b([A-Z]+)\b', lambda match: match.group(1).upper(), name)

    cleanedCompanies = {
        name: {
        "country_iso": company["country_iso"],
        "city": company["city"],
        "nace": company["nace"],
        "website": company["website"]
        }
    }

    response = requests.post(POST_URL, json=cleanedCompanies)

    if response.json()["success"]:
        print(f"Successfully added {cleanedCompanies} to MongoDB!")
    else:
        print(f"Failed to add {cleanedCompanies} to MongoDB.")
    if response.status_code != 201:
        print(f"Error: {response.content}")
    else:
        print(f"{name} added to the database.")

print("CLEANING FINISHED")
