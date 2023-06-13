
"""Main application file"""

from app.app import app
from flask import Response


# assign the server to run in docker and support debugging in vs code
server = app.server


@app.server.route("/health")
def health():
    return Response(status=200)


if __name__ == "__main__":
    app.run_server(port=8050, debug=True)





