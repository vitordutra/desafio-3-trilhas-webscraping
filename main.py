import sys
from streamlit_app import main
import streamlit.cli as stcli

if __name__ == "__main__":
    sys.argv = ["streamlit", "run", "./streamlit_app/app.py"]
    sys.exit(stcli.main())
