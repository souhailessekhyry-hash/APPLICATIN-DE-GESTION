Azure deployment pitfalls and recommendations:

1) **Ephemeral storage**:
   - App Service's local disk can be reset (deployments, scale, platform updates). Do NOT rely on it for persistent images or DB.
   - Recommendation: use Azure Blob Storage for images and Azure Database for persistent records.

2) **Startup command**:
   - For Linux App Service set startup command: `gunicorn --bind 0.0.0.0 --timeout 600 app:app`
   - For Windows use web.config or a different approach. Prefer Linux plan.

3) **Environment variables & secrets**:
   - Don't commit SECRET_KEY to source. Use App Settings in Azure to set SECRET_KEY, DATABASE_URL, etc.

4) **SQLite limitations**:
   - SQLite is fine for demos, but concurrent writes/scale can break. Use a managed DB for production.

5) **File upload size & timeouts**:
   - App Service front-end may have limits. Set reasonable MAX_CONTENT_LENGTH and handle timeouts.

6) **Permissions & path differences**:
   - Use absolute paths (os.path.join) and ensure folders are created. App Service gives write access to /home.

7) **Scaled instances**:
   - If you scale to multiple instances, uploaded files on one instance are not available on others.

8) **Logging & diagnostics**:
   - Enable App Service logs and use Application Insights for deeper diagnostics.

9) **Static files**:
   - Serving many images from local disk is less scalable; consider CDN + Blob Storage.

10) **Build & Startup time**:
   - Keep startup lightweight. Preinstall dependencies in a custom image if needed.

Quick checklist for a safe Azure deployment:
- [ ] Move images to Blob Storage.
- [ ] Move DB to Azure DB (Postgres/MySQL/SQL).
- [ ] Set startup command to use gunicorn.
- [ ] Set SECRET_KEY and other secrets in App Settings.
- [ ] Test file uploads and storage persistence after a restart.
