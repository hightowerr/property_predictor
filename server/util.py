import json
import pickle
from typing import List, Optional
from pathlib import Path

__property_type: Optional[List[str]] = None
__district: Optional[List[str]] = None
__county: Optional[List[str]] = None
__model: Optional[object] = None
__xgb_imp: Optional[object] = None

def get_property_type() -> Optional[List[str]]:
    return __property_type

def get_district() -> Optional[List[str]]:
    return __district

def get_county() -> Optional[List[str]]:
    return __county

def get_xgb_imp() -> Optional[object]:
    return __xgb_imp

def load_saved_artifacts() -> bool:
    """Load saved artifacts from the artifacts directory."""
    global __property_type, __district, __county, __model, __xgb_imp
    
    artifacts_path = Path("./server/artifacts")
    
    try:
        with (artifacts_path / "columns.json").open("r") as f:
            json_data = json.load(f)
            data_columns = json_data['data_columns']
            __property_type = data_columns[1:5]
            __district = data_columns[5:347]
            __county = data_columns[347:]
    except Exception as e:
        print(f"Error loading columns: {e}")
        return False

    model_files = ["home_prices_model.pkl", "home_prices_model.pickle"]
    for model_file in model_files:
        try:
            with (artifacts_path / model_file).open("rb") as f:
                __model = pickle.load(f)
                break
        except FileNotFoundError:
            continue
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
    else:
        print("Error: Could not find model file")
        return False

    try:
        with (artifacts_path / "xgb_imp.pkl").open("rb") as f:
            __xgb_imp = pickle.load(f)
    except FileNotFoundError:
        print("Warning: Could not find xgb_imp.pkl")
    except Exception as e:
        print(f"Warning: Error loading XGBoost importance: {e}")

    return True
