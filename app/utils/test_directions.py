import requests
import json

API_KEY = "AIzaSyDf34ue6DB4ukLmPqY09YJsZ4FXW_vs98Y"

def get_directions(origin, destination, mode="driving"):
    url = "https://maps.googleapis.com/maps/api/directions/json"
    
    params = {
        "origin": origin,
        "destination": destination,
        "mode": mode,
        "alternatives": "true",  # Fetch alternative routes
        "key": API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data["status"] != "OK":
        return json.dumps({"error": data["status"]}, indent=4)

    num_routes = len(data.get("routes", []))
    print(f"Number of routes returned for {mode}: {num_routes}")

    result = []

    for i, route in enumerate(data["routes"]):
        print(f"\nDEBUG: Route {i + 1} Summary -> {route.get('summary', 'No summary')}")  

        # Ensure we process all routes even if no legs are found
        if "legs" not in route or len(route["legs"]) == 0:
            print(f"DEBUG: Route {i + 1} has NO LEGS! Adding as empty.")
            result.append({"route_number": i + 1, "summary": route.get("summary", "No summary"), "legs": []})
            continue  # Move to next route

        for j, leg in enumerate(route["legs"]):
            route_details = {
                "route_number": i + 1,
                "leg_number": j + 1,
                "summary": route.get("summary", "No summary"),
                "start_address": leg["start_address"],
                "end_address": leg["end_address"],
                "distance": leg["distance"]["text"],
                "duration": leg["duration"]["text"],
                "steps": []
            }

            for step in leg["steps"]:
                instruction = step["html_instructions"]
                instruction = instruction.replace("<b>", "").replace("</b>", "").replace("<wbr/>", "")
                instruction = instruction.replace('<div style="font-size:0.9em">', " ").replace('</div>', "")

                step_data = {
                    "instruction": instruction,
                    "distance": step["distance"]["text"],
                    "duration": step["duration"]["text"],
                    "start_location": step["start_location"],
                    "end_location": step["end_location"]
                }
                
                route_details["steps"].append(step_data)

            result.append(route_details)

    # Save the result to a file
    with open('directions_output.json', 'w') as f:
        json.dump(result, f, indent=4)

    print("Output saved to directions_output.json")

# Example usage
origin = "Swargate, Pune, Maharashtra, India"
destination = "Katraj, Pune, Maharashtra, India"

get_directions(origin, destination, mode="walking")
