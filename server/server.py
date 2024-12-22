from flask import Flask, request, jsonify
import util

app = Flask(__name__)

@app.route('/api/property-types', methods=['GET'])
def get_property_types():
    response = jsonify({
        'property_types': util.get_property_type()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/api/districts', methods=['GET'])
def get_districts():
    response = jsonify({
        'districts': util.get_district()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/api/counties', methods=['GET'])
def get_counties():
    response = jsonify({
        'counties': util.get_county()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/predict_home_price', methods=['GET', 'POST'])
def predict_home_price():
    try:
        # Support both GET and POST requests
        year = int(request.args.get('Year') or request.form.get('year'))
        district = request.args.get('District') or request.form.get('district')
        property_type = request.args.get('property_type') or request.form.get('property_type')
        county = request.args.get('County') or request.form.get('county')

        # Validate relationships
        mapping = util.get_district_county_mapping()
        if county not in mapping['district'].get(district.lower(), []):
            return jsonify({'error': f'Invalid district-county combination: {district} - {county}'}), 400

        response = jsonify({
            'estimated_price': util.get_estimated_price(
                Year=year,
                District=district,
                property_type=property_type,
                County=county
            )
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        import traceback
        return jsonify({
            'error': 'Something went wrong!', 
            'details': str(e),
            'traceback': traceback.format_exc()
        }), 500

if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction...")
    util.load_saved_artifacts()
    app.run(debug=False)
