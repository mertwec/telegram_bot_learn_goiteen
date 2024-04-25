from dotenv import load_dotenv
import os


load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE_DIR, 'app', 'data', 'films.json')
