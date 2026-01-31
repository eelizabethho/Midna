from flask import jsonify, request
import google.generativeai as genai
import os
import json


def register_crime_intel_endpoints(app, safety_data, gemini_client):
    """Register crime intelligence endpoints"""
    
    @app.route('/crime-intel', methods=['POST'])
    def crime_intel():
        """Crime intelligence and trends analysis endpoint"""
        try:
            data = request.get_json()
            
            if not data:
                return jsonify({"error": "Empty request body"}), 400
            
            area = data.get('area', '')
            time_window = data.get('time_window', 'last_7_days')
            
            stats = aggregate_safety_stats(safety_data)
            
            api_key = os.getenv("GEMINI_API_KEY", "")
            if api_key and gemini_client:
                insights = generate_ai_insights(api_key, safety_data, stats, area, time_window)
            else:
                insights = generate_basic_insights(safety_data, stats, area)
            
            return jsonify({
                "summary": insights.get("summary", "No summary available"),
                "trend": insights.get("trend", "No trend data available"),
                "alerts": insights.get("alerts", []),
                "stats": stats
            })
            
        except Exception as e:
            print(f"Error in crime_intel endpoint: {e}")
            return jsonify({"error": "Internal server error"}), 500


def aggregate_safety_stats(safety_data):
    """Aggregate statistics from safety data"""
    if not safety_data:
        return {
            "total_incidents": 0,
            "avg_incidents_per_location": 0,
            "poor_lighting_count": 0,
            "moderate_lighting_count": 0,
            "good_lighting_count": 0,
            "total_locations": 0
        }
    
    total_incidents = sum(p.get('incident_count', 0) for p in safety_data)
    total_locations = len(safety_data)
    poor_lighting_count = sum(1 for p in safety_data if p.get('lighting') == 'poor')
    moderate_lighting_count = sum(1 for p in safety_data if p.get('lighting') == 'moderate')
    good_lighting_count = sum(1 for p in safety_data if p.get('lighting') == 'good')
    avg_incidents = total_incidents / total_locations if total_locations > 0 else 0
    
    return {
        "total_incidents": total_incidents,
        "avg_incidents_per_location": round(avg_incidents, 2),
        "poor_lighting_count": poor_lighting_count,
        "moderate_lighting_count": moderate_lighting_count,
        "good_lighting_count": good_lighting_count,
        "total_locations": total_locations
    }


def generate_ai_insights(api_key, safety_data, stats, area, time_window):
    """Generate AI insights using Gemini"""
    try:
        prompt = f"""Analyze the following safety data for {area} ({time_window}) and provide insights.

Safety Statistics:
- Total incidents: {stats['total_incidents']}
- Average incidents per location: {stats['avg_incidents_per_location']}
- Locations with poor lighting: {stats['poor_lighting_count']}
- Locations with moderate lighting: {stats['moderate_lighting_count']}
- Locations with good lighting: {stats['good_lighting_count']}
- Total locations analyzed: {stats['total_locations']}

Location Details:
"""
        for i, point in enumerate(safety_data[:10]):
            prompt += f"- Location {i+1}: {point.get('incident_count', 0)} incidents, lighting: {point.get('lighting', 'unknown')}\n"
        
        prompt += """
Please provide:
1. A brief summary (2-3 sentences) of the overall safety situation
2. A trend observation (e.g., "30% increase on Fridays" or "Higher incidents in poorly lit areas")
3. 3-5 short alert bullet points highlighting key safety concerns

Format your response as JSON:
{
    "summary": "...",
    "trend": "...",
    "alerts": ["...", "...", "..."]
}
"""
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-pro-002')
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()
        
        return json.loads(response_text)
        
    except Exception as e:
        print(f"Error generating AI insights: {e}")
        return generate_basic_insights(safety_data, stats, area)


def generate_basic_insights(safety_data, stats, area):
    """Generate basic insights without AI (fallback)"""
    if stats['total_incidents'] == 0:
        summary = f"{area} shows no reported incidents in the current dataset."
    elif stats['total_incidents'] < 10:
        summary = f"{area} has relatively low incident counts with {stats['total_incidents']} total incidents across {stats['total_locations']} locations."
    elif stats['total_incidents'] < 30:
        summary = f"{area} shows moderate safety concerns with {stats['total_incidents']} incidents reported across {stats['total_locations']} locations."
    else:
        summary = f"{area} has significant safety concerns with {stats['total_incidents']} incidents reported across {stats['total_locations']} locations."
    
    if stats['poor_lighting_count'] > stats['good_lighting_count']:
        trend = f"Poor lighting conditions observed at {stats['poor_lighting_count']} locations, which may correlate with higher incident rates."
    elif stats['avg_incidents_per_location'] > 5:
        trend = f"Above-average incident rate of {stats['avg_incidents_per_location']} incidents per location indicates areas requiring attention."
    else:
        trend = f"Average incident rate of {stats['avg_incidents_per_location']} incidents per location."
    
    alerts = []
    if stats['poor_lighting_count'] > 0:
        alerts.append(f"{stats['poor_lighting_count']} location(s) with poor lighting conditions identified")
    if stats['total_incidents'] > 20:
        alerts.append(f"High total incident count: {stats['total_incidents']} incidents across all locations")
    
    high_incident_locations = [p for p in safety_data if p.get('incident_count', 0) >= 5]
    if high_incident_locations:
        alerts.append(f"{len(high_incident_locations)} location(s) with 5+ incidents require immediate attention")
    if stats['moderate_lighting_count'] > 0:
        alerts.append(f"{stats['moderate_lighting_count']} location(s) with moderate lighting may benefit from improvements")
    if not alerts:
        alerts.append("No critical alerts at this time")
    
    return {
        "summary": summary,
        "trend": trend,
        "alerts": alerts
    }
