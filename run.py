import os
from app import create_app
from waitress import serve

app = create_app()


#if __name__ == "__main__":
 #   app.run(debug=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)


