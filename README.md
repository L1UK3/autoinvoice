A simple microservice that automatically generates, saves and sends invoices to my supervisor via email.

## Initial structure:

app/
│
├── __init__.py
├── routes/
│   ├── auth.py          # Login/logout, session handling
│   └── protected.py     # All protected routes
│
├── templates/
│   ├── index.html       # Login page
│   └── invoice_template.html  # Invoice PDF template
│
├── static/
│   └── style.css        # CSS styles
│
├── .env                 # Environment variables
├── pyproject.toml       # Project dependencies
└── README.md

