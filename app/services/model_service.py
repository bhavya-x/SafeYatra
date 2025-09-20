import pandas as pd
import json
from geopy.distance import geodesic
from shapely.geometry import Point, LineString
from pymongo import MongoClient
from datetime import datetime

def calculate_route_safety(routes_json, age, gender):
    # Connect to MongoDB
    client = MongoClient("mongodb+srv://bhavyajain035:password1234@cluster0.qs1fe.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    db = client["safe_yatra"]
    collection_ml = db["ML_output"]
    
    # Load clusters from MongoDB
    df_clusters = pd.DataFrame(list(collection_ml.find({}, {"_id": 0})))
    
    def parse_corner_points(corner_points_str):
        points = corner_points_str.split(";")
        return [tuple(map(float, p.split(","))) for p in points]
    
    df_clusters["Corner_Points"] = df_clusters["Corner_Points"].apply(parse_corner_points)
    
    # Get current hour
    user_time = datetime.now().hour
    
    # Convert inputs to required format
    gender_code = "M" if gender.lower() == "male" else "F"
    age_code = "A" if age >= 18 else "C"
    time_code = "D" if 6 <= user_time < 20 else "N"
    
    # Determine cluster column
    if gender_code == "M" and age_code == "A" and time_code == "D":
        cluster_col = "ClusterDangerLevel_M_A_D"
    elif gender_code == "M" and age_code == "A" and time_code == "N":
        cluster_col = "ClusterDangerLevel_M_A_N"
    elif gender_code == "M" and age_code == "C" and time_code == "D":
        cluster_col = "ClusterDangerLevel_M_C_D"
    elif gender_code == "M" and age_code == "C" and time_code == "N":
        cluster_col = "ClusterDangerLevel_M_C_N"
    elif gender_code == "F" and age_code == "A" and time_code == "D":
        cluster_col = "ClusterDangerLevel_F_A_D"
    elif gender_code == "F" and age_code == "A" and time_code == "N":
        cluster_col = "ClusterDangerLevel_F_A_N"
    elif gender_code == "F" and age_code == "C" and time_code == "D":
        cluster_col = "ClusterDangerLevel_F_C_D"
    else:
        cluster_col = "ClusterDangerLevel_F_C_N"
    
    def compute_step_danger(step, clusters, cluster_col):
        step_start = (step["start_location"]["lng"], step["start_location"]["lat"])
        step_end = (step["end_location"]["lng"], step["end_location"]["lat"])
        step_line = LineString([step_start, step_end])
        
        total_danger_adjustment = 0
        clusters_passed = {}
        
        for _, cluster in clusters.iterrows():
            center_lat, center_lon = map(float, cluster['Center_Point'].split(', '))
            center_point = (center_lon, center_lat)
            distance = step_line.distance(Point(center_point)) * 111_139
            
            if distance <= 250 and center_point not in clusters_passed:
                distance_factor = 1 / (1 + distance / 1000)
                danger_adjustment = cluster[cluster_col] * distance_factor
                clusters_passed[center_point] = (distance, danger_adjustment)
                total_danger_adjustment += danger_adjustment
        
        return total_danger_adjustment
    
    def compute_route_danger(route, cluster_col):
        total_danger_score = sum(compute_step_danger(step, df_clusters, cluster_col) for step in route["legs"][0]["steps"])
        num_steps = len(route["legs"][0]["steps"])
        
        if num_steps == 0:
            return 0  # No steps = No danger
        
        max_possible_score = 300 * num_steps
        if any(compute_step_danger(step, df_clusters, cluster_col) > 300 for step in route["legs"][0]["steps"]):
            danger_level = 100
        else:
            danger_level = (total_danger_score / max_possible_score) * 100
            danger_level = min(100, danger_level)
        
        safety_score = 100 - danger_level
        return safety_score
    
    route_safety_scores = [(route["route_number"], compute_route_danger(route, cluster_col)) for route in routes_json]
    
    sorted_routes = sorted(route_safety_scores, key=lambda x: x[1], reverse=True)
    
    rank_mapping = {route_num: rank + 1 for rank, (route_num, _) in enumerate(sorted_routes)}
    
    output_data = [{"rank": rank_mapping[route_num], "safety_score": score} for route_num, score in route_safety_scores]
    
    return json.dumps(output_data, indent=4)