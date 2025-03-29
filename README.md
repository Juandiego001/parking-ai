# 🚗SecureGate: Smart Parking with License Plate Recognition

## 📌 Project Overview
This project implements a vehicle license plate recognition system for a smart parking lot. It uses YOLO for plate detection and Azure OCR to extract characters from them. The information is then validated and stored in a PostgreSQL database through an API built with Flask. The frontend is developed using Vue.js for an interactive user interface.

```
📁 parking-ai
│── 📁 backend
│   │── 📁 core/              # Main backend logic
│   │   │── 📁 controllers/   # Handles API requests and responses
│   │   │── 📁 implements/    # Implementations of interfaces or base classes
│   │   │── 📁 schemas/       # Data validation schemas (e.g., Pydantic)
│   │   │── 📁 services/      # Business logic and database interactions
│   │   │── __init__.py       # Initializes the `core` module
│   │   │── app.py            # Backend setup and initialization
│   │   │── models.py         # Database models (ORM definitions)
│   │   └── utils.py          # Helper functions and utilities
|   |
│   │── 📁 core_model/         # Module handling detection and OCR
│   │   │── app.py             # Exposes the model as an API
│   │   │── detection.py       # License plate detection logic using YOLO
│   │   │── ocr.py             # OCR processing to extract text from plates
│   │   └── requirements.txt   # Dependencies for this module
|
│   │── best.pt            # YOLO model weights
│   │── log.cfg            # Logging configuration file
│   │── requirements.txt   # Backend dependencies
│   └── run.py             # Main script to run the backend
│
│── 📁 docs              # Project documentation
│   │── db.md             # Database documentation
│   │── db_mysql.sql      # SQL script for MySQL
│   └── db_postgres.sql   # SQL script for PostgreSQL
|
│── 📁 frontend
│   │── 📁 components/      # Vue components
│   │── 📁 layouts/         # Layout templates
│   │── 📁 mixins/          # Reusable logic for components
│   │── 📁 pages/           # Nuxt.js pages
│   │── 📁 plugins/         # Custom plugins
│   │── 📁 public/          # Static assets
│   │── 📁 server/          # API routes and middleware
│   │── .gitignore          # Git ignore file
│   │── README.md           # Frontend documentation
│   │── nuxt.config.ts      # Nuxt.js configuration
│   │── package-lock.json   # Dependency lockfile
│   │── package.json        # Dependencies and scripts
│   └── tsconfig.json       # TypeScript configuration
|
└──
|── 📁 model
|   └── CompuNube_V2.ipynb    # YOLO's model
|
└── README.md    # Project documentation
```

## 🔧 Technologies Used
- Python (Flask for the API)
- YOLO (license plate detection)
- Azure Vision OCR (character recognition)
- PostgreSQL (database to store plate information)
- Vue.js / Nuxt.js (frontend framework)
- Docker (Deploy the Database)

## ✏️ System Architecture

This project follows a client-server architecture with the following flow:

1. The Vue.js frontend allows users to upload images of vehicle plates.
2. The images are sent to the Flask backend, where YOLO detects the license plate region.
3. The detected region is processed using Azure OCR to extract the text.
4. The recognized plate number is validated and stored in the MySQL database.
5. The frontend displays real-time results and allows users to search for past records.
