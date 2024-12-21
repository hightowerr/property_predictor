import json
import pickle
from typing import List, Optional, Union
from pathlib import Path

__property_type: Optional[List[str]] = None
__district: Optional[List[str]] = None
__county: Optional[List[str]] = None
__data_columns: Optional[List[str]] = None
__model: Optional[object] = None
__xgb_imp: Optional[object] = None

def get_property_type():
    return __property_type

def get_district():
    return __district

def get_county():
    return __county

def get_xgb_imp():
    return __xgb_imp

def load_saved_artifacts() -> bool:
    """
    Load saved artifacts from the artifacts directory.
    
    Returns:
        bool: True if artifacts loaded successfully, False otherwise
    """
    print("loading saved artifacts...start")
    global __property_type, __district, __county, __data_columns, __model, __xgb_imp
    
    artifacts_path = Path("./server/artifacts")
    
    try:
        # Load columns
        columns_file = artifacts_path / "columns.json"
        with columns_file.open("r") as f:
            json_data = json.load(f)
            if 'data_columns' not in json_data:
                raise ValueError("data_columns not found in columns.json")
            __data_columns = json_data['data_columns']
            __property_type = __data_columns[1:5]
            __district = __data_columns[5:347]
            __county = __data_columns[347:]
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
        print(f"Error loading columns.json: {e}")
        return False

    # Try loading model with multiple extensions
    model_extensions = ["home_prices_model.pkl", "home_prices_model.pickle"]
    model_loaded = False
    for ext in model_extensions:
        model_file = artifacts_path / ext
        try:
            with model_file.open("rb") as f:
                __model = pickle.load(f)
                model_loaded = True
                break
        except FileNotFoundError:
            continue
        except Exception as e:
            print(f"Error loading model {ext}: {e}")
            return False

    if not model_loaded:
        print("Error: Could not find model file")
        return False

    # Optional: Load XGBoost importance
    xgb_file = artifacts_path / "xgb_imp.pkl"
    try:
        with xgb_file.open("rb") as f:
            __xgb_imp = pickle.load(f)
    except FileNotFoundError:
        print("Warning: Could not find xgb_imp.pkl")
    except Exception as e:
        print(f"Warning: Error loading XGBoost importance file: {e}")

    print("loading saved artifacts...done")
    return True

if __name__ == '__main__':
    load_saved_artifacts()
    print("Property Types:", get_property_type())
    print("Districts:", get_district())
    print("Counties:", get_county())
    print("XGBoost Importance:", get_xgb_imp())
