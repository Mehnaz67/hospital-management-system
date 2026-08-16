import os
import sys

# Add the project root directory to the system path so Flask can find models.py, templates, and static files
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

# Expose the WSGI handler for Vercel serverless execution
app = app