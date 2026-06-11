# -*- coding: utf-8 -*-
from app import create_app

app = create_app()

if __name__ == "__main__":
    # Útil para pruebas locales; en producción corre con gunicorn
    app.run(host="127.0.0.1", port=5002, debug=False)
