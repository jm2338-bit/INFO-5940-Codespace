# Assignment 1 - Change Log

## 2025-10-25

* **Issue:** Encountered `ValueError: numpy.dtype size changed, may indicate binary incompatibility` when running the Streamlit app.
* **Fix:** Explicitly added `numpy==1.26.4` to `requirements.txt` to pin the version. Re-ran `pip install -r requirements.txt` to apply the fix.