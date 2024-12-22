from flask import Flask, jsonify
from server.util import get_property_type, load_saved_artifacts

app = Flask(__name__)

@app.route('/get_property_type')
def property_type_route():
    # Ensure artifacts are loaded
    if not get_property_type():
        load_saved_artifacts()
    
    # Get property types and remove the 'property type_' prefix
    property_types = [pt.replace('property type_', '') for pt in get_property_type()] if get_property_type() else []
    
    return jsonify(property_types)

if __name__ == '__main__':
    # Load artifacts before starting the server
    load_saved_artifacts()
    app.run(debug=True)
