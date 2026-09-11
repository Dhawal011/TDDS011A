> ## 🚀 Quick Start — New Windows Laptop
>
> **Requirements:** Python 3.11+ and Git
>
> Open PowerShell and run:
>
> ```powershell
> cd desktop
> git clone https://github.com/Dhawal011/TDDS011A.git
> cd TDDS011A
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> .\setup_windows.ps1
> .\run_project.bat
> ```
>
> After the application starts, open the dashboard:
>
> **http://localhost:8501**
>
> **FastAPI:** http://127.0.0.1:8000
>
> **Swagger API:** http://127.0.0.1:8000/docs
>
> The setup script automatically creates the virtual environment, installs dependencies, loads the historical dataset, trains the ML model, creates the database and loads demonstration data.
>
> No project folder or database needs to be copied manually. The GitHub repository contains the required source code, datasets and setup files.

# Blood Donor Intelligence System

### An API-Based Decision Support Platform for Donor Matching, Demand Forecasting and Shortage Risk Analysis

---

## 1. Project Overview

The Blood Donor Intelligence System is a Python-based healthcare decision-support prototype designed to assist blood banks and hospitals in managing blood donors, blood requests, inventory and future blood demand.

The system combines traditional rule-based donor matching with machine learning-based demand forecasting.

Instead of treating donor matching as only a database search problem, the system provides an integrated platform containing:

- Donor management
- Blood request management
- Blood inventory management
- Blood-group compatibility matching
- Distance-based donor ranking
- Urgency-aware donor prioritization
- Historical blood-demand analysis
- Machine-learning-based demand forecasting
- Estimated shortage-risk analysis
- REST APIs using FastAPI
- Interactive dashboard using Streamlit

The project is developed as an academic decision-support prototype and is not intended to replace clinical blood-bank procedures or professional medical judgment.

---

# 2. Problem Statement

Blood banks need to maintain sufficient blood supplies while responding quickly to hospital requests.

Several challenges can occur:

1. Difficulty identifying suitable nearby donors.
2. Increasing demand for specific blood groups.
3. Limited visibility into historical demand patterns.
4. Risk of unexpected shortages.
5. Manual coordination between donors, hospitals and blood inventories.
6. Lack of a unified API-based system connecting these processes.

This project addresses these challenges by developing a centralized intelligent system that combines donor management, matching, inventory monitoring and machine-learning-based demand forecasting.

---

# 3. Objectives

The major objectives of the project are:

- To develop a REST API for blood donor management.
- To manage hospital blood requests through APIs.
- To maintain blood inventory information.
- To identify compatible donors for a blood request.
- To rank donors using distance and request urgency.
- To analyze historical blood demand and supply.
- To develop a machine-learning model for demand forecasting.
- To estimate future shortage risk using predicted demand and available inventory.
- To provide an interactive dashboard for system monitoring.
- To create a portable application that can be deployed on another Windows computer.

---

# 4. System Architecture

```text
                    ┌────────────────────────┐
                    │   Streamlit Dashboard  │
                    │     User Interface     │
                    └────────────┬───────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │       FastAPI          │
                    │       REST API         │
                    └────────────┬───────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                  │
              ▼                  ▼                  ▼
       Donor Management    Blood Requests      Inventory
              │                  │                  │
              └──────────────────┼──────────────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │   Matching Service     │
                    │ Compatibility +        │
                    │ Distance + Urgency      │
                    └────────────┬───────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │   ML Prediction Service │
                    └────────────┬───────────┘
                                 │
                    ┌────────────┴────────────┐
                    ▼                         ▼
          Demand Forecasting          Shortage Risk
                    │                         │
                    └────────────┬────────────┘
                                 ▼
                    ┌────────────────────────┐
                    │     SQLite Database    │
                    └────────────────────────┘
