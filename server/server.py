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

@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():
    try:
        year = int(request.form['year'])
        district = request.form['district']
        property_type = request.form['property_type']
        county = request.form['county']

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
        return jsonify({'error': 'Something went wrong! ' + str(e)}), 500

if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction...")
    util.load_saved_artifacts()
    app.run(debug=False)