import json
import pickle
import numpy as np
from typing import List, Optional
from pathlib import Path

__property_type: Optional[List[str]] = None
__district: Optional[List[str]] = None
__county: Optional[List[str]] = None
#__model: Optional[object] = None
__xgb_imp: Optional[object] = None

def get_property_type() -> Optional[List[str]]:
    return __property_type

def get_district() -> Optional[List[str]]:
    return __district

def get_county() -> Optional[List[str]]:
    return __county

def get_xgb_imp() -> Optional[object]:
    return __xgb_imp

def get_estimated_price(Year, District, property_type, County):
    print(f"Received inputs - Year: {Year}, District: {District}, Property Type: {property_type}, County: {County}")
    
    # Convert inputs to match the format in columns.json
    property_type = f"property type_{property_type.lower()}"
    District = f"district_{District.lower()}"  # Add district_ prefix
    County = f"county_{County.lower()}"       # Add county_ prefix too for consistency
    
    print(f"Converted inputs - Property Type: {property_type}, District: {District}, County: {County}")
    print(f"Available property types: {__property_type}")
    print(f"Available districts: {__district}")
    print(f"Available counties: {__county}")
    
    # Validate inputs against known values
    if property_type not in __property_type:
        raise ValueError(f"Invalid property_type. Must be one of: {[pt.replace('property type_', '') for pt in __property_type]}")
    if District not in __district:
        raise ValueError(f"Invalid District. Must be one of: {[d.replace('district_', '') for d in __district]}")
    if County not in __county:
        raise ValueError(f"Invalid County. Must be one of: {[c.replace('county_', '') for c in __county]}")
    
    print("Input validation passed")
    
    # Get the feature names from columns.json
    X_columns = ['Year'] + [f'Property Type_{pt}' for pt in __property_type] + \
                [f'District_{d}' for d in __district] + \
                [f'County_{c}' for c in __county]
    
    # Create a zero array with same length as training features
    x = np.zeros(len(X_columns))
    
    # Set Year (first column)
    x[0] = Year
    
    # Create feature names for the categorical inputs
    property_feature = f"Property Type_{property_type}"
    district_feature = f"District_{District}"
    county_feature = f"County_{County}"
    
    # Find and set indices for categorical features
    for i, col in enumerate(X_columns):
        if col == property_feature:
            x[i] = 1
        elif col == district_feature:
            x[i] = 1
        elif col == county_feature:
            x[i] = 1
    
    # Get prediction (returns log price)
    if __xgb_imp is None:
        raise ValueError("Model not loaded")
    
    print("Making prediction with input array:", x)
    log_price = __xgb_imp.predict([x])[0]
    print("Predicted log price:", log_price)
    
    # Convert from log price to actual price and convert to native Python float
    final_price = float(np.exp(log_price))
    print("Final predicted price:", final_price)
    return final_price

def load_saved_artifacts() -> bool:
    """Load saved artifacts from the artifacts directory."""
    global __property_type, __district, __county, __xgb_imp
    
    artifacts_path = Path(__file__).parent / "artifacts"
    
    try:
        with (artifacts_path / "columns.json").open("r") as f:
            json_data = json.load(f)
            data_columns = json_data['data_columns']
            
            # Find the indices for proper slicing
            property_type_end = 5  # After 'year' and 4 property types
            district_start = property_type_end
            
            # Find where districts end (where counties begin)
            for i, col in enumerate(data_columns[district_start:], start=district_start):
                if col.startswith('county_'):
                    district_end = i
                    break
            
            __property_type = data_columns[1:property_type_end]
            __district = data_columns[district_start:district_end]
            __county = data_columns[district_end:]
            
            print(f"Loaded {len(__property_type)} property types")
            print(f"Loaded {len(__district)} districts")
            print(f"Loaded {len(__county)} counties")
            
    except Exception as e:
        print(f"Error loading columns: {e}")
        return False

    try:
        with (artifacts_path / "xgb_imp.pkl").open("rb") as f:
            __xgb_imp = pickle.load(f)
        print("loaded xgb_imp.pkl")
    except FileNotFoundError:
        print("Error: Could not find xgb_imp.pkl")
        return False
    except Exception as e:
        print(f"Error loading XGBoost importance: {e}")
        return False

    return __xgb_imp is not None

if __name__ == "__main__":
    print("Loading saved artifacts...")
    success = load_saved_artifacts()
    
    if success:
        print("\nLoaded Artifacts:")
        print("Property Types:", get_property_type())
        print("Number of Districts:", len(get_district()) if get_district() else "None")
        print("Number of Counties:", len(get_county()) if get_county() else "None")
        #print("Model loaded:", get_model() is not None)
        print("XGBoost Importance loaded:", get_xgb_imp() is not None)
    else:
        print("Failed to load artifacts.")
    
    print(get_estimated_price(Year=2024, District="luton", property_type="o", County="bedfordshire"))
