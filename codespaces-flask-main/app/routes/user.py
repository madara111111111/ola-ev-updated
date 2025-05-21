from codespaces_flask_main.app import create_app

app = create_app()

# Use a relative path for the CSV so it works on Render and other Linux hosts
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SALES_CSV = os.path.join(BASE_DIR, "ola_ev_sales_2020_2024.csv")
sales_df = pd.read_csv(SALES_CSV)