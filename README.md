<h1 align="center"> Fotuna FX Decision Intelligence Engine </h1>
<p align="center"> An Enterprise-Grade Machine Learning Ecosystem for Predictive Forex Analytics and Automated Decision Synthesis </p>

<p align="center">
  <img alt="Build" src="https://img.shields.io/badge/Build-Passing-brightgreen?style=for-the-badge">
  <img alt="Issues" src="https://img.shields.io/badge/Issues-0%20Open-blue?style=for-the-badge">
  <img alt="Contributions" src="https://img.shields.io/badge/Contributions-Welcome-orange?style=for-the-badge">
  <img alt="License" src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge">
</p>
<!-- 
  **Note:** These are static placeholder badges. Replace them with your project's actual badges.
  You can generate your own at https://shields.io
-->

## 📑 Table of Contents
- [Overview](#-overview)
- [Key Features](#-key-features)
- [Tech Stack & Architecture](#-tech-stack--architecture)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Usage](#-usage)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🌟 Overview

### Hook
Fotuna FX Decision Intelligence Engine is a sophisticated, multi-modal machine learning platform designed to synthesize disparate global macro signals into high-precision foreign exchange forecasts and actionable trading decisions.

### The Problem
> Global currency markets, particularly in emerging economies with dual-rate systems like the USD/NGN pair, are influenced by an overwhelming volume of fragmented data. Traditional analysis fails to account for the interplay between unofficial market scrapers, prediction market sentiment (Polymarket), energy sector fluctuations (EIA), and global news narratives simultaneously. This leads to information asymmetry, delayed responses to market shifts, and inconsistent decision-making in volatile environments.

### The Solution
Fotuna FX addresses these challenges by implementing a comprehensive "Intelligence-in-Depth" architecture. It automates the entire lifecycle of FX analysis—from scraping unofficial market rates and ingesting prediction market probabilities to sentiment analysis via NLP and ensemble modeling. By combining Long Short-Term Memory (LSTM) networks for sequence modeling and XGBoost for gradient-boosted decision trees, overseen by a specialized Meta-Learner, Fotuna provides a unified decision engine that outputs not just predictions, but calibrated trade signals and position-sizing logic.

### Architecture Overview
The system is built on a high-performance **Microservices** and **REST API** foundation. It leverages **FastAPI** for low-latency serving, **PyTorch** and **Transformers** for state-of-the-art NLP, and a robust data pipeline that handles everything from raw ingestion to standardized feature engineering. The backend is supported by **PostgreSQL** for relational feature storage and **Redis** for efficient data handling, all encapsulated within a **Docker** environment for seamless deployment.

---

## ✨ Key Features

### 🤖 Hybrid Machine Learning Ensemble
*   **Sequential Intelligence (LSTM):** Captures time-series dependencies in FX fluctuations using the `FXLSTMModel`, allowing the system to understand historical momentum and cyclical patterns.
*   **Gradient Boosted Precision (XGBoost):** Utilizes `FXXGBoostModel` to process structural features and non-linear relationships between macro-economic indicators.
*   **Meta-Learner Synthesis:** The `FXMetaLearner` acts as the master arbiter, weighing inputs from multiple models to provide a final, high-confidence decision signal.

### 📡 Multi-Modal Data Ingestion & Scrapers
*   **Automated Scrapers:** Dedicated `nairatoday_scraper` extracts real-world unofficial market rates, providing visibility into parallel market premiums.
*   **Prediction Market Integration:** Direct connectors for **Polymarket** and **Bayse** APIs capture collective intelligence and crowd-sourced probabilities regarding economic events.
*   **Macro-Economic Feeds:** Ingests critical energy data from the **EIA API** and official exchange rates via the **Fixer API**.

### 🧠 Advanced NLP & Sentiment Analysis
*   **Global News Processing:** Integrated News and GDELT 2.0 filters process thousands of headlines to extract macro-relevant sentiment.
*   **Semantic Preprocessing:** Uses `transformers` and `sentence-transformers` to convert raw text into dense vector representations, enabling the model to "read" market anxiety or optimism.

### 🏗️ Robust Engineering Pipeline
*   **Feature Adapter & Builder:** Automatically transforms raw API responses into standardized model features through the `feature_builder` and `feature_adapter`.
*   **Walk-Forward Validation:** Implements `WalkForwardEngine` for backtesting, ensuring that model performance is validated against time-accurate data splits without look-ahead bias.
*   **Automated Normalization:** A specialized `Normalizer` suite ensures that oil prices, sentiment scores, and market probabilities are scaled correctly for neural network consumption.

### ⚡ Enterprise Decision Engine
*   **Actionable Outputs:** Beyond simple forecasting, the `DecisionEngine` provides logic for position sizing and trade execution based on model confidence and market volatility.
*   **Inference Service:** A production-ready `inference_service` optimized for real-time application integration via FastAPI.

---

## 🛠️ Tech Stack & Architecture

### Verified Technical Stack

| Technology | Purpose | Why it was Chosen |
| :--- | :--- | :--- |
| **FastAPI** | Core API Framework | Provides high-performance, asynchronous endpoints for inference and system health monitoring. |
| **PyTorch** | Deep Learning Framework | Powers the LSTM models and sentiment transformer architectures with GPU acceleration. |
| **XGBoost** | Gradient Boosting | Handles structured feature data with extreme efficiency and handles missing values inherently. |
| **Transformers** | NLP / Sentiment | Leverages state-of-the-art BERT/RoBERTa models for high-accuracy text analysis. |
| **PostgreSQL** | Primary Database | Ensures ACID-compliant storage for historical features and model metadata. |
| **Redis** | Caching & State | Facilitates rapid data access for the inference service and scheduler tasks. |
| **Docker** | Containerization | Guarantees environment parity across development, testing, and production. |
| **Optuna** | Hyperparameter Tuning | Automates the optimization of model parameters to maximize predictive accuracy. |

---

## 📁 Project Structure

```
axrylic-ice-Helios-ML-Engine/
├── 📄 Dockerfile                    # Containerization configuration
├── 📄 README.md                      # Project documentation
├── 📄 requirements.txt               # Python dependency manifest
├── 📁 app/                           # FastAPI Application Layer
│   ├── 📄 main.py                    # API Entry point
│   ├── 📁 api/                       # REST Route definitions
│   │   └── 📄 routes.py              # API endpoints (GET /)
│   ├── 📁 core/                      # Core system utilities
│   │   ├── 📄 config.py              # System configuration management
│   │   └── 📄 logger.py              # Standardized logging service
│   ├── 📁 models/                    # Pydantic data schemas
│   │   └── 📄 schemas.py             # Request/Response models
│   ├── 📁 services/                  # Business logic layer
│   │   ├── 📄 decision_engine.py      # Trade logic and sizing
│   │   ├── 📄 feature_builder.py     # Real-time feature construction
│   │   └── 📄 inference_service.py   # Model prediction orchestration
│   └── 📁 utils/                     # Application helpers
│       └── 📄 helpers.py             # General utility functions
├── 📁 configs/                       # Configuration files
│   └── 📄 settings.yaml              # Application & Model settings
├── 📁 data_ingestion/                # External Data Acquisition
│   ├── 📁 apis/                      # API Connectors
│   │   ├── 📄 bayse_api.py           # Bayse events integration
│   │   ├── 📄 eia_api.py             # Energy Information Admin data
│   │   ├── 📄 fixer_api.py           # Official FX rate integration
│   │   ├── 📄 news_api.py            # Global news data fetcher
│   │   └── 📄 polymarket_api.py      # Prediction market analytics
│   ├── 📁 scheduler/                 # Task Scheduling
│   │   └── 📄 jobs.py                # Data collection job definitions
│   └── 📁 scrapers/                  # Web Scraping
│       └── 📄 nairatoday_scraper.py   # Unofficial market rate extractor
├── 📁 ml/                            # Machine Learning Core
│   ├── 📁 db/                        # ML Persistence Layer
│   │   ├── 📄 database.py            # Connection management
│   │   ├── 📄 models.py              # Feature database models
│   │   ├── 📄 repository.py          # Data access patterns
│   │   └── 📄 store.py               # Feature store implementation
│   ├── 📁 filters/                   # Data Cleaning & Signal Extraction
│   │   ├── 📄 bayse_filter.py        # Bayse signal processing
│   │   ├── 📄 eia_filter.py          # Oil/Energy macro filtering
│   │   ├── 📄 fx_filter.py           # Currency pair relevance filtering
│   │   ├── 📄 news_filter.py         # Macro-relevant news extraction
│   │   └── 📄 polymarket_filter.py   # Prediction volume/prob filtering
│   ├── 📁 models/                    # Model Architectures
│   │   ├── 📄 calibrator.py          # Probability calibration
│   │   ├── 📄 feature_db.py          # SQLite/Relational feature tracking
│   │   ├── 📄 interpreter.py         # Model explainability suite
│   │   ├── 📄 meta_learner.py        # Ensemble synthesis model
│   │   ├── 📄 pipeline.py            # End-to-end ML pipeline
│   │   ├── 📄 scaler.py              # Data scaling utilities
│   │   ├── 📄 train_lstm.py          # Sequence model implementation
│   │   ├── 📄 train_xgboost.py       # Gradient boosting implementation
│   │   └── 📁 weights/               # Serialized model artifacts (.keras, .json, .pkl)
│   ├── 📁 pipelines/                 # Workflow Orchestration
│   │   ├── 📄 data_ingestion.py      # Raw data ingestion flow
│   │   ├── 📄 evaluation.py          # Metrics and performance tracking
│   │   ├── 📄 feature_engineering.py # Signal transformation logic
│   │   ├── 📄 normalizer.py          # Scaling and normalization
│   │   ├── 📄 runtime.py             # Live execution environment
│   │   └── 📄 walk_forward.py        # Backtesting engine
│   └── 📁 registry/                  # Model Governance
│       └── 📄 model_registry.py      # Versioning and storage logic
├── 📁 nlp/                           # Natural Language Processing
│   ├── 📄 preprocessing.py           # Text cleaning and tokenization
│   └── 📄 sentiment.py               # News sentiment aggregation
├── 📁 scripts/                       # Operational Scripts
│   ├── 📄 backfill.py                # Historical data population
│   ├── 📄 run_inference.py           # Live system execution
│   └── 📄 run_training.py            # Model training entry point
└── 📁 tests/                         # Quality Assurance
    ├── 📄 test_pipeline.py           # End-to-end integration tests
    └── 📄 test_filters.py            # Unit tests for data filters
```

---

## 🚀 Getting Started

### Prerequisites
To run the Fotuna FX Engine, ensure your environment meets the following requirements:
*   **Python:** 3.10 or higher
*   **Package Manager:** `pip`
*   **Database:** PostgreSQL 14+ (for feature storage)
*   **Cache:** Redis 6+ (for session and real-time data)
*   **Containerization:** Docker (optional but recommended)

### Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/axrylic-ice/Helios-ML-Engine.git
    cd axrylic-ice-Helios-ML-Engine
    ```

2.  **Create a Virtual Environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Database Setup**
    Ensure your PostgreSQL and Redis services are running. The system will use the configurations defined in `configs/settings.yaml`.

5.  **Initialize the Environment**
    ```bash
    # Run the backfill script to populate initial historical data
    python scripts/backfill.py
    ```

---

## 🔧 Usage

### Running the API
The core interaction point for external services is the FastAPI server.
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
Once running, you can access the API documentation at `http://localhost:8000/docs`.

### Training the Models
To retrain the LSTM, XGBoost, and Meta-Learner models on the latest ingested data:
```bash
python scripts/run_training.py
```
This script will:
1.  Load data from the feature store.
2.  Perform walk-forward validation splits.
3.  Optimize hyperparameters using Optuna.
4.  Save the latest weights to `ml/models/weights/`.

### Executing Live Inference
For continuous monitoring and decision generation, use the live system script:
```bash
python scripts/run_inference.py
```
This will trigger the full pipeline: Ingestion -> Filtering -> Engineering -> Prediction -> Decision.

### API Endpoints
*   **GET `/`**: Health check and system status.
*   **POST `/api/v1/decision`**: (Supported via `routes.py`) Returns a synthesized FX decision based on current market features.

---

## 🤝 Contributing

We welcome contributions to improve the Fotuna FX Decision Intelligence Engine! Your input helps make this project a more robust tool for the global finance community.

### How to Contribute

1. **Fork the repository** - Click the 'Fork' button at the top right of this page.
2. **Create a feature branch** 
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes** - Improve code, documentation, or model architectures.
4. **Test thoroughly** - Ensure all functionality works by running existing tests.
   ```bash
   pytest tests/
   ```
5. **Commit your changes** - Write clear, descriptive commit messages.
   ```bash
   git commit -m 'Add: Implementation of new macro signal filter for central bank data'
   ```
6. **Push to your branch**
   ```bash
   git push origin feature/amazing-feature
   ```
7. **Open a Pull Request** - Submit your changes for review by the maintainers.

### Development Guidelines
- ✅ Follow PEP 8 style guides for Python code.
- 📝 Document all new functions and classes (even if the current codebase is light on docstrings).
- 🧪 Add unit tests in the `tests/` directory for any new filters or pipelines.
- 🔄 Maintain backward compatibility with the existing `FeatureRow` and `FeatureStore` schemas.

---

## 📝 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for complete details.

### What this means:
- ⚠️ **Liability:** The software is provided "as is", without warranty. Predictive models involve financial risk; use responsibly.

---

<p align="center">Made with ❤️ by the Helios Engineering Team</p>
<p align="center">
  <a href="#">⬆️ Back to Top</a>
</p>
