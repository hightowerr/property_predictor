import pickle
from pathlib import Path

def test_model():
    try:
        artifacts_path = Path(__file__).parent / "artifacts"
        with (artifacts_path / "xgb_imp.pkl").open("rb") as f:
            model = pickle.load(f)
            print("Model loaded successfully")
            print("Model type:", type(model))
            print("Model attributes:", dir(model))
    except Exception as e:
        print(f"Error loading model: {e}")

if __name__ == "__main__":
    test_model()
