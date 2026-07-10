# Auto-Invoice: Implementation Plan & Checklist

This document details the step-by-step plan for building the automated weekly invoice generator and sender. 

---

## 🛠️ Step 1: Environment & Dependency Setup
We need to set up the necessary packages. You've already installed `playwright` and `python-dotenv`.
- [ ] Add remaining backend dependencies to your `pyproject.toml`:
  - `jinja2` (for rendering the HTML invoice and email templates)
  - `apscheduler` (for scheduling the weekly background scrape job)
  - `sqlite3` / `sqlmodel` (to store cookies and generated invoice metadata)
  - `itsdangerous` (to secure dashboard sessions/cookies)
- [ ] Run `playwright install chromium` on your system to download the headless browser binaries.
- [ ] Set up the `.env` template with these configurations:
  ```env
  ADMIN_PASSWORD=your_secure_dashboard_password
  OUTLOOK_EMAIL=your_outlook_email@outlook.com
  OUTLOOK_PASSWORD=your_outlook_app_password
  PERSONAL_EMAIL=your_notification_email@domain.com
  SUPERVISOR_EMAIL=supervisor_email@domain.com
  HOURLY_RATE=50.00
  SQUARE_TARGET_URL=https://squareup.com/dashboard/
  SESSION_SECRET_KEY=generate_a_random_secret_string
  ```

---

## 🔐 Step 2: Database & Cookie Store (`app/database.py`)
To bypass 2FA/Passkeys, we must store and load session cookies. We'll use a simple SQLite database.
- [ ] Write `app/database.py` with tables/functions to:
  - Initialize the SQLite database.
  - Save session cookies (serialized as JSON).
  - Retrieve the active session cookies.
  - Store generated invoice metadata (invoice ID, billing period, total hours, total wages, status: `DRAFT` / `APPROVED` / `SENT`).

---

## 🕸️ Step 3: Square Teams Scraper (`app/scraper.py`)
The Playwright script that logs in using cookies and extracts the shift details.
- [ ] Write `app/scraper.py`:
  - Launch Playwright headlessly.
  - Inject the saved cookies into the browser context.
  - Navigate to the Square timecards/shifts URL.
  - Check if we are successfully logged in (redirected to login = cookies expired).
  - Locate the week's shifts, extract:
    - Shift dates
    - Start & End times
    - Regular/Overtime hours worked
  - Return the structured data or save it as a draft invoice in the database.
  - Handle cookie-expiration alerts (emailing you if login fails).

---

## 📄 Step 4: HTML-to-PDF Invoice Generator (`app/invoice_generator.py`)
Replicates your spreadsheet design as an HTML page and prints it to PDF.
- [ ] Create an HTML/CSS template that matches your CSV template layout.
- [ ] Write `app/invoice_generator.py`:
  - Load the HTML template.
  - Populate the placeholder fields (your name, dates, hourly rate, shift rows, total amount, bank details).
  - Use Playwright headlessly to open this populated HTML page in-memory.
  - Call `page.pdf(...)` to output a clean, pixel-perfect PDF file in the storage directory.

---

## ✉️ Step 5: Outlook SMTP Mailer (`app/mailer.py`)
Sends emails using Python's standard `smtplib`.
- [ ] Write `app/mailer.py`:
  - `send_review_notification(invoice_id)`: Emails you a link to review the draft invoice in the FastAPI web UI.
  - `send_invoice_to_supervisor(pdf_path)`: Emails the final PDF to your supervisor (CC'ing you).
  - `send_cookie_refresh_warning()`: Emails you when Square session cookies are expired or missing.

---

## 📅 Step 6: Weekly Scheduler (`app/scheduler.py`)
Configures the job scheduler to fetch data on Sundays.
- [ ] Write `app/scheduler.py`:
  - Initialize `APScheduler` (BackgroundScheduler).
  - Schedule the scraping function to run every Sunday.
  - Ensure the scheduler starts and stops gracefully with the FastAPI application lifecycle.

---

## 🖥️ Step 7: Web Dashboard & Routes (`app/routes/`)
Provides the control panel for password login, pasting cookies, and approving invoices.
- [ ] **Auth Route** (`app/routes/public.py`):
  - Simple login form with password protection.
  - Sets a secure cookie using `itsdangerous`.
- [ ] **Dashboard Routes** (`app/routes/protected.py`):
  - `/dashboard`: Main screen. Shows cookie status, list of draft/sent invoices, and a manual "Run Scraper Now" button.
  - `/update-cookies`: Text area to paste JSON session cookies (pasted from browser extension).
  - `/invoice/{id}`: Detailed page showing shift details and a PDF preview.
  - `/invoice/{id}/approve`: Button that triggers the email to the supervisor and marks the invoice as `SENT`.

---

## ☁️ Step 8: Dockerization & Hugging Face Deployment
Prepares the project for 24/7 free cloud execution.
- [ ] Write a `Dockerfile` that:
  - Installs Python.
  - Installs Playwright system dependencies.
  - Runs `playwright install chromium`.
  - Exposes port `7860` and launches Uvicorn.
- [ ] Deploy to Hugging Face Spaces:
  - Create a new Space (Docker template).
  - Add your `.env` variables under **Settings > Variables and secrets**.
  - Push the code to the space's repository.
