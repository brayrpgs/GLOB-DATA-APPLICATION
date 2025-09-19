# 🌐 GLOB-DATA-APPLICATION API

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)  
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)  
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)  

---

## 📝 Overview

**GLOB-DATA-APPLICATION** is a critical component that serves as the main data source for the entire application.  
It is a **RESTful API** built with **FastAPI**, designed to receive, process, and deliver data from the database to different system modules.  

This module is essential for the information flow, as it is responsible for:

- Extracting data from the main database.  
- Validating the integrity and format of data.  
- Transforming information according to consumer needs.  
- Exposing **RESTful endpoints** for other microservices to consume.  
- Maintaining **data consistency** throughout the application.  

The project follows a methodical approach, emphasizing robust entity design and strict validations to ensure data is correctly processed and normalized.

---

## ✨ Features

- **Data extraction**: Efficient queries from the main database.  
- **Validation & transformation**: Standardized dates, numbers, and boolean values.  
- **RESTful endpoints**: Accessible to other microservices and external clients.  
- **Data integrity**: Prevention of duplicates and invalid entries.  
- **Monitoring & logging**: Error logging, event tracking, and alerts for inconsistencies.  

---

## 🛠️ Technologies Used

- **Backend**: Python 3.12+, FastAPI  
- **Database**: PostgreSQL (or your preferred database)  
- **Containerization**: Docker  

---

## 🚀 Getting Started

### Prerequisites

- [Python 3.12+](https://www.python.org/downloads/)  
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)  

### Local Installation

1. **Clone the repository**

```bash
git clone https://github.com/your-org/GLOB-DATA-APPLICATION.git
Navigate to the API directory

bash
Copy code
cd GLOB-DATA-APPLICATION/api
Install dependencies

bash
Copy code
pip install -r requirements.txt
Run the application

bash
Copy code
uvicorn main:app --reload --host 0.0.0.0 --port 8000
Access the API

Swagger UI: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc

# 🐳 Docker Start
To run the service in Docker:

bash
Copy code
docker build -t glob-data-application .
docker run -d -p 8000:8000 glob-data-application
The API will be available at:
👉 http://localhost:8000

# 📖 API Usage
The Swagger documentation (/docs) includes all available endpoints, request/response models, and possible status codes for each operation.

This makes integration with other microservices and external clients simple and straightforward.

