import json
import pickle

__property_type = None
__district = None
__county = None
__data_columns = None
__model = None
__xgb_imp = None

def get_property_type():
    return __property_type

def get_district():
    return __district

def get_county():
    return __county

def get_xgb_imp():
    return __xgb_imp

def load_saved_artifacts():
    print("loading saved artifacts...start")
    global __property_type
    global __district
    global __county
    global __data_columns
    global __model
    
    artifacts_path = "./server/artifacts"
    
    try:
        with open(f"{artifacts_path}/columns.json", "r") as f:
            json_data = json.load(f)
            if 'data_columns' not in json_data:
                raise ValueError("data_columns not found in columns.json")
            __data_columns = json_data['data_columns']
            __property_type = __data_columns[1:5]
            __district = __data_columns[5:347]
            __county = __data_columns[347:]
    except FileNotFoundError:
        print(f"Error: Could not find columns.json")
        return False
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in columns.json")
        return False
    except Exception as e:
        print(f"Error loading columns.json: {str(e)}")
        return False

    try:
        # Try .pkl extension first, then .pickle if not found
        try:
            with open(f"{artifacts_path}/home_prices_model.pkl", "rb") as f:
                __model = pickle.load(f)
        except FileNotFoundError:
            with open(f"{artifacts_path}/home_prices_model.pickle", "rb") as f:
                __model = pickle.load(f)
    except FileNotFoundError:
        print(f"Error: Could not find model file (tried both .pkl and .pickle)")
        return False
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        return False
        
    try:
        with open(f"{artifacts_path}/xgb_imp.pkl", "rb") as f:
            global __xgb_imp
            __xgb_imp = pickle.load(f)
    except FileNotFoundError:
        print(f"Warning: Could not find xgb_imp.pkl")
    except Exception as e:
        print(f"Warning: Error loading XGBoost importance file: {str(e)}")

    print("loading saved artifacts...done")
    return True

if __name__ == '__main__':
    load_saved_artifacts()
    print("Property Types:", get_property_type())
    print("Districts:", get_district())
    print("Counties:", get_county())
    print("XGBoost Importance:", get_xgb_imp())
