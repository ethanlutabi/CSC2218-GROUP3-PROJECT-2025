
# main.py

import uvicorn
from presentation.api import app

if __name__ == "__main__":
    uvicorn.run(
        "main:app",        # module_name:variable_name
        host="127.0.0.1",  # or "0.0.0.0" to listen on all interfaces
        port=8000,
        reload=True        # auto-reload on code changes
    )
