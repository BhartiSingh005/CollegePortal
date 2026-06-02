# CollegePortal - AIML Predictive Placement Dashboard

CollegePortal is an industry-standard, full-stack enterprise web application designed to track student academic logs and predict placement likelihood using an Asynchronous AIML evaluation pipeline. The system utilizes a decoupled architecture featuring a robust Django REST Framework (DRF) backend secured by JWT authentication and a responsive, high-performance vanilla JavaScript frontend interface.

## 🚀 Key Features

- **Decoupled Full-Stack Architecture:** Complete separation of concerns between the API data gateway and the client interface presentation layer.
- **Secure JWT Authentication:** All data endpoints are protected by industry-standard JSON Web Token (SimpleJWT) Bearer access and refresh token verification gates.
- **Dynamic AIML Predictive Engine:** Processes student performance feature vectors (CGPA, Attendance, Backlogs, Coding Platform Ratings) using a live machine learning model pipeline (`.pkl`) with a symmetrical rule-based algorithmic fallback configuration.
- **Persistent Analytics Logging:** Chronologically tracks and archives all user calculation inputs and classification results inside a structured database, filterable by individual authenticated profiles.
- **Production System Hardening (Phase 5):** Implements defensive backend validation boundary criteria (e.g., matching realistic metric limits) and a global exception management framework to eliminate raw server error leaks.
- **Cross-Origin Resource Sharing (CORS):** Fully integrated middleware enabling secure cross-origin transfers between isolated frontend assets and the server gateway.

---

## 📂 System Architecture & Directory Structure

```text
CollegePortal/
│
├── core/                       # Core Django Framework Settings Root
│   ├── __init__.py
│   ├── settings.py             # Global App Registry, CORS, SimpleJWT, and DB mappings
│   ├── urls.py                 # Core routing configurations
│   └── wsgi.py
│
├── api/                        # Modular App Data Engine Backend
│   ├── migrations/             # Database structural state schema histories
│   ├── exceptions.py           # Phase 5 Custom Global Exception Middleware Handlers
│   ├── models.py               # PlacementPrediction and Academic log tables
│   ├── serializers.py          # Data payload serializers mapping queries to JSON
│   ├── urls.py                 # Clean REST API endpoints router gateway
│   └── views.py                # Protected API controller business logic views
│
├── frontend/                   # Client Layer UI Applications
│   ├── login.html              # Secure student authorization entrance
│   ├── index.html              # Central tracking analytics panel workspace grid
│   ├── style.css               # Theme styling definitions
│   └── app.js                  # Asynchronous Fetch API controller engine
│
├── manage.py
└── requirements.txt            # System dependencies manifest
