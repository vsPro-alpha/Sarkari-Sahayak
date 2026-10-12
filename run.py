import uvicorn
import os
import sys

if __name__ == "__main__":
    print("=" * 65)
    print("  🏛️  Sarkari Sahayak & Grievance Drafter (Sarvam AI)")
    print("=" * 65)
    print("  Starting server at: http://127.0.0.1:8000")
    print("  Open your browser at: http://localhost:8000")
    print("=" * 65)
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
