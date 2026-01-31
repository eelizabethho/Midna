from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from google import genai
import os
import json
import math
import crime_intel

load_dotenv()
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

api_key = os.getenv("GEMINI_API_KEY", "").encode('ascii', 'ignore').decode('ascii')
client = genai.Client(api_key=api_key) if api_key else None


def load_safety_data():
    """Load safety data from safety_data.json"""
    safety_data = []
    json_path = os.path.join(os.path.dirname(__file__), 'safety_data.json')

    try:
        with open(json_path, 'r') as f:
            data = json.load(f)

        if 'safety_points' in data:
            for point in data['safety_points']:
                if 'coordinates' in point:
                    lng, lat = point['coordinates'][0], point['coordinates'][1]
                else:
                    lat = point['lat']
                    lng = point['lng']
                
                safety_data.append({
                    'lat': float(lat),
                    'lng': float(lng),
                    'incident_count': int(point.get('incident_count', 0)),
                    'lighting': point.get('lighting', 'good').lower().strip()
                })

        print(f"✅ Loaded {len(safety_data)} safety data points from {json_path}")

    except FileNotFoundError:
        print(f"⚠️  Warning: Safety data file not found at {json_path}")
        print("   The server will run but route analysis will have no safety data.")
    except json.JSONDecodeError as e:
        print(f"⚠️  Error: Invalid JSON in safety_data.json: {e}")
    except Exception as e:
        print(f"⚠️  Error loading safety data: {e}")

    return safety_data

SAFETY_DATA = load_safety_data()
crime_intel.register_crime_intel_endpoints(app, SAFETY_DATA, client)


def calculate_distance(lat1, lng1, lat2, lng2):
    """Calculate approximate distance between two coordinates"""
    return math.sqrt((lat1 - lat2)**2 + (lng1 - lng2)**2)


def find_nearby_incidents(route_coords, safety_data, threshold=0.01):
    """Find safety data points near route coordinates"""
    nearby_points = []
    for coord in route_coords:
        lng, lat = coord[0], coord[1]
        for point in safety_data:
            distance = calculate_distance(lat, lng, point['lat'], point['lng'])
            if distance < threshold and point not in nearby_points:
                nearby_points.append(point)
    return nearby_points


def calculate_risk_level(nearby_points):
    """Calculate risk level: safe, moderate, or poor"""
    if not nearby_points:
        return "safe"
    
    total_incidents = sum(p['incident_count'] for p in nearby_points)
    poor_lighting_count = sum(1 for p in nearby_points if p['lighting'] == 'poor')
    
    if total_incidents >= 10 or poor_lighting_count >= 2:
        return "poor"
    elif total_incidents >= 5 or poor_lighting_count >= 1:
        return "moderate"
    else:
        return "safe"


def evaluate_segment(segment_coords, safety_data, threshold=0.01):
    """Evaluate a route segment and return risk level"""
    nearby_points = find_nearby_incidents(segment_coords, safety_data, threshold)
    return calculate_risk_level(nearby_points)


@app.route('/test/hello', methods=['GET'])
def test_hello():
    """Health check endpoint"""
    return jsonify({"message": "Hello! Server is running! 🎉"})


@app.route('/analyze-route', methods=['POST'])
def analyze_route():
    """Analyze routes and return GeoJSON with risk levels per segment"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Empty request body"}), 400

        if 'routes' in data:
            routes = data['routes']
            if not routes or not isinstance(routes, list):
                return jsonify({"error": "Invalid 'routes' format. Expected array."}), 400
        elif 'coordinates' in data:
            routes = [{"coordinates": data['coordinates']}]
        else:
            return jsonify({"error": "Missing 'routes' or 'coordinates' in request"}), 400

        features = []
        for route in routes:
            coordinates = route.get('coordinates', [])
            route_id = route.get('route_id', None)
            
            if not coordinates or len(coordinates) < 2:
                continue
            
            for i in range(len(coordinates) - 1):
                segment_coords = [coordinates[i], coordinates[i + 1]]
                risk_level = evaluate_segment(segment_coords, SAFETY_DATA)
                
                feature = {
                    "type": "Feature",
                    "geometry": {
                        "type": "LineString",
                        "coordinates": segment_coords
                    },
                    "properties": {
                        "risk_level": risk_level
                    }
                }
                
                if route_id:
                    feature["properties"]["route_id"] = route_id
                
                features.append(feature)
        
        return jsonify({
            "type": "FeatureCollection",
            "features": features
        })

    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON in request body"}), 400
    except Exception as e:
        print(f"Error in analyze_route: {e}")
        return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Route Safety Analysis Server")
    print("=" * 60)
    print(f"📍 Server: http://localhost:3001")
    print(f"📝 Endpoints:")
    print(f"   GET  /test/hello")
    print(f"   POST /analyze-route")
    print(f"   POST /crime-intel")
    print("=" * 60)
    app.run(host='0.0.0.0', port=3001, debug=True)
