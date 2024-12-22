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

def get_model() -> Optional[object]:
    return __model

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

    try:
        with (artifacts_path / "xgb_imp.pkl").open("rb") as f:
            __xgb_imp = pickle.load(f)
    except FileNotFoundError:
        print("Warning: Could not find xgb_imp.pkl")
    except Exception as e:
        print(f"Warning: Error loading XGBoost importance: {e}")

    try:
        with (artifacts_path / "xgb_model.pkl").open("rb") as f:
            __model = pickle.load(f)
    except FileNotFoundError:
        print("Warning: Could not find xgb_model.pkl")
    except Exception as e:
        print(f"Warning: Error loading XGBoost model: {e}")

    return True

if __name__ == "__main__":
    print("Loading saved artifacts...")
    success = load_saved_artifacts()
    
    if success:
        print("\nLoaded Artifacts:")
        print("Property Types:", get_property_type())
        print("Number of Districts:", len(get_district()) if get_district() else "None")
        print("Number of Counties:", len(get_county()) if get_county() else "None")
        print("Model loaded:", get_model() is not None)
        print("XGBoost Importance loaded:", get_xgb_imp() is not None)
    else:
        print("Failed to load artifacts.")
