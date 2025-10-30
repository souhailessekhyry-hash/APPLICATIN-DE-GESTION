# Flask Stock Sample (minimal)

## What this sample does
- Simple Flask app to add products (name, description, price) and optionally upload an image.
- Uses SQLite (products.db) and stores images under `static/uploads/`.
- Minimal UI with two pages: index (list) and add product.

## Run locally
1. Create a virtualenv:
   ```
   python -m venv venv
   source venv/bin/activate  # on Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. Run:
   ```
   python app.py
   ```
3. Open http://127.0.0.1:5000

## Deploying to Azure App Service (Linux)
- Use the `gunicorn` command as the startup command, e.g.:
  ```
  gunicorn --bind 0.0.0.0 --timeout 600 app:app
  ```
- **Important caveats** (see README_SUMMARY.txt in project root for a longer checklist).

## Notes
- Uploaded files and the SQLite database are stored in the App Service's file system, which is ephemeral across scale-out and may be reset on some platform events. For production, use Azure Blob Storage for images and an Azure Database (MySQL/Postgres) or Azure SQL for persistent data.
