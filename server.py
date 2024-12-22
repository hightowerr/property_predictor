from flask import Flask, jsonify, request
from server.util import get_property_type, load_saved_artifacts, get_estimated_price

app = Flask(__name__)

@app.route('/get_property_type')
def property_type_route():
    # Ensure artifacts are loaded
    if not get_property_type():
        load_saved_artifacts()
    
    # Get property types and remove the 'property type_' prefix
    property_types = [pt.replace('property type_', '') for pt in get_property_type()] if get_property_type() else []
    
    return jsonify(property_types)

@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():
    # Ensure artifacts are loaded
    if not get_property_type():
        load_saved_artifacts()
    
    # Get parameters from the request
    Year = request.args.get('Year', type=int)
    District = request.args.get('District')
    property_type = request.args.get('property_type')
    County = request.args.get('County')
    
    # Validate input parameters
    if not all([Year, District, property_type, County]):
        return jsonify({"error": "Missing required parameters"}), 400
    
    try:
        # Predict home price
        estimated_price = get_estimated_price(Year, District, property_type, County)
        return jsonify({"estimated_price": estimated_price})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred"}), 500

if __name__ == '__main__':
    # Load artifacts before starting the server
    load_saved_artifacts()
    app.run(debug=True)
