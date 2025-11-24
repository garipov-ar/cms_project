CMS MVP archive (backend + frontend skeleton)

Backend changes:
- cms_app: models (Category, Document, DocumentVersion, AuditLog)
- serializers, views, urls for basic CRUD and version upload
- settings_additions.txt shows where to apply settings changes

Frontend:
- React + Vite + TypeScript skeleton in frontend/
- Run with: npm install && npm run dev
- The frontend proxies /api to backend at http://localhost:8000 via Vite config.

Note: original TU file used in project is available at local path:
/mnt/data/ТЗ.docx

To install:
1) copy files into your repository root (merge backend/ into existing backend/)
2) add 'cms_app' to INSTALLED_APPS, apply settings from backend/project_settings/settings_additions.txt
3) pip install -r requirements.txt (add entries from backend/requirements_add.txt)
4) python manage.py makemigrations cms_app
5) python manage.py migrate
6) docker-compose up (or run services separately)
7) frontend: cd frontend && npm install && npm run dev
