<h1 align="center"> Fotuna FX Decision Intelligence Engine </h1>

<p align="center"> High-performance ensemble machine learning architecture for multi-signal foreign exchange forecasting and macroeconomic decision intelligence. </p>

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

## 📌 Table of Contents

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
Fotuna FX Decision Intelligence Engine is a sophisticated, high-precision forecasting ecosystem that leverages multi-modal machine learning—integrating deep learning, gradient boosting, and sentiment analysis—to navigate the complexities of volatile currency markets with institutional-grade accuracy.

### The Problem
> Traditional foreign exchange analysis often relies on lagging indicators or siloed data streams, failing to account for the rapid interplay between official rates, parallel market fluctuations, global energy prices, and real-time news sentiment. For analysts and systems operating in high-volatility environments (such as the USD/NGN corridor), the lack of a unified, predictive engine that synthesizes macro-economic signals with micro-market sentiment leads to suboptimal decision-making and increased financial risk.

### The Solution
Fotuna FX eliminates fragmented analysis by providing a centralized Decision Intelligence Engine. By orchestrating a complex pipeline of data ingestion (from oil prices to prediction markets), sentiment extraction through NLP, and ensemble modeling (LSTM and XGBoost), Fotuna transforms raw macro-data into actionable insights. It automates the heavy lifting of feature engineering, standardization, and model calibration, allowing users to focus on strategic execution rather than data plumbing.

### Architecture Overview
The system is built on a modular **Microservices-ready architecture** utilizing:
- **RESTful API Layer**: Powered by **FastAPI** for high-concurrency inference and system health monitoring.
- **Ensemble ML Core**: Utilizing **PyTorch** for sequential modeling (LSTM) and **XGBoost** for structural data analysis.
- **Data Orchestration**: A robust pipeline featuring specialized filters (EIA, News, FX) and a centralized Feature Store.
- **Persistence**: Hybrid storage using **PostgreSQL** for feature persistence and **Redis** for high-speed state management.

---

## ✨ Key Features

### 🧠 Advanced Ensemble Modeling
Fotuna doesn't rely on a single algorithm. It utilizes a dual-engine approach:
- **LSTM (Long Short-Term Memory)**: Captures complex temporal dependencies and sequential patterns in FX historical data.
- **XGBoost**: Processes tabular macro-economic features and structural market signals with high efficiency.
- **FXMetaLearner**: An intelligent aggregator that builds high-level features to provide a final, calibrated decision.

### 📊 Real-Time Macro-Signal Integration
Stay ahead of market shifts by automatically processing diverse external signals:
- **Energy Intelligence**: Extracts oil and energy signals via the EIA filter to account for commodity-driven currency movements.
- **Prediction Markets**: Integrates probability and volume signals from platforms like Polymarket to gauge market expectations.
- **News Sentiment**: Leverages NLP transformers to convert global news streams into quantitative sentiment scores.

### 🛡️ Robust Data Engineering & Validation
Ensures the highest data integrity through a rigorous pipeline:
- **FXScaler**: Implements leak-proof scaling, fitting exclusively on training data to ensure valid backtesting.
- **Walk-Forward Engine**: Simulates real-world conditions by testing models in sequential time windows.
- **Standardization & Normalization**: Dedicated modules for cleaning and aligning heterogeneous data sources (Official vs. Unofficial FX rates, Bayse events, etc.).

### ⚡ Production-Ready Infrastructure
- **FastAPI Core**: A high-performance gateway providing real-time access to model decisions and system status.
- **Automated Schedulers**: Background jobs for continuous data collection and model retraining.
- **Dockerized Deployment**: Consistent environment parity from development to production.

---

## 🛠️ Tech Stack & Architecture

| Technology | Purpose | Why it was Chosen |
| :--- | :--- | :--- |
| **FastAPI** | Backend API Framework | Offers exceptional performance, asynchronous support, and automatic OpenAPI documentation. |
| **PyTorch / TensorFlow** | ML Core & NLP | Provides the deep learning infrastructure required for LSTM models and NLP sentiment analysis. |
| **XGBoost** | Tabular Modeling | Industry-leading performance for structured data classification and regression. |
| **PostgreSQL** | Primary Database | Relational integrity for storing historical features, model metadata, and training rows. |
| **Redis** | Caching & State | Ensures low-latency access to real-time features and inference results. |
| **Optuna** | Hyperparameter Tuning | Automated optimization to find the most efficient model configurations. |
| **Docker** | Containerization | Guarantees reproducibility and simplifies cross-platform deployment. |

---

## 📁 Project Structure

```
Fotuna-FX-Engine/
├── 📄 Dockerfile                  # Container definition for production deployment
├── 📄 requirements.txt            # Project dependencies (FastAPI, PyTorch, XGBoost, etc.)
├── 📂 app/                        # Main API Application layer
│   ├── 📄 main.py                 # FastAPI entry point & health check
│   ├── 📂 api/                    # API Route definitions
│   │   └── 📄 routes.py           # Endpoints for system status and decisions
│   └── 📂 services/               # Business logic providers
│       ├── 📄 feature_builder.py  # Constructs inference-ready feature sets
│       ├── 📄 decision_engine.py  # Logic for final market decisions
│       └── 📄 inference_service.py # Orchestrates live model predictions
├── 📂 ml/                         # Machine Learning Core
│   ├── 📂 models/                 # Model architectures & weights
│   │   ├── 📄 meta_learner.py     # Aggregator for multi-model outputs
│   │   ├── 📄 train_lstm.py       # Sequence-based neural network logic
│   │   ├── 📄 train_xgboost.py    # Gradient boosting model logic
│   │   └── 📂 weights/            # Pre-trained model artifacts (.keras, .json, .pkl)
│   ├── 📂 pipelines/              # Data processing & training workflows
│   │   ├── 📄 pipeline.py         # Main training and inference pipeline
│   │   ├── 📄 feature_engineering.py # Logic for market expectations & macro signals
│   │   ├── 📄 walk_forward.py     # Backtesting validation engine
│   │   └── 📄 normalizer.py       # Data scaling and cleaning utilities
│   ├── 📂 filters/                # Data-source specific cleaners
│   │   ├── 📄 fx_filter.py        # Focuses on USD/NGN and relevant pairs
│   │   └── 📄 eia_filter.py       # Processes energy and oil market signals
│   ├── 📂 data/                   # Data storage (Raw & Processed)
│   │   ├── 📂 raw/                # Original datasets (Oil, FX, GDELT)
│   │   └── 📂 features/           # Engineered feature sets
│   └── 📂 db/                     # ML-specific storage logic
│       ├── 📄 repository.py       # CRUD operations for feature rows
│       └── 📄 store.py            # High-level feature storage interface
├── 📂 data_ingestion/             # External Data Acquisition
│   ├── 📂 apis/                   # Connectors for external providers
│   │   ├── 📄 fixer_api.py        # FX rate procurement
│   │   └── 📄 news_api.py         # News metadata fetching
│   ├── 📂 scrapers/               # Web scraping utilities
│   │   └── 📄 nairatoday_scraper.py # Parallel market data extraction
│   └── 📂 scheduler/              # Automated job management
│       └── 📄 jobs.py             # Periodic data collection tasks
├── 📂 nlp/                        # Natural Language Processing
│   ├── 📄 sentiment.py            # News sentiment aggregation
│   └── 📄 preprocessing.py        # Text cleaning and tokenization
├── 📂 scripts/                    # Operational Utilities
│   ├── 📄 run_training.py         # Model training entry point
│   └── 📄 run_inference.py        # Live system execution script
└── 📂 tests/                      # Comprehensive Test Suite
    ├── 📄 test_pipeline.py        # Integration tests for ML workflows
    └── 📄 test_filters.py         # Unit tests for data filtering logic
```

---

## 🚀 Getting Started

### Prerequisites
- **Python 3.10+**
- **Pip** (Python Package Manager)
- **PostgreSQL** (Active instance for data persistence)
- **Redis** (Active instance for caching)
- **Docker** (Optional, for containerized execution)

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/axrylic-ice/Helios-ML-Engine.git
   cd Helios-ML-Engine
   ```

2. **Set Up Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize Database**
   Ensure your PostgreSQL and Redis services are running. The system will create necessary tables upon the first run of the training script.

---

## 🔧 Usage

### 1. Data Backfilling
Before training, populate the system with historical data:
```bash
python scripts/backfill.py
```

### 2. Model Training
Train the ensemble (LSTM, XGBoost, and Meta-Learner) using the provided training script. This script handles feature engineering, scaling, and model persistence:
```bash
python scripts/run_training.py
```

### 3. Running the API Service
Start the FastAPI server to expose endpoints for inference and system monitoring:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
*Access the interactive API docs at `http://localhost:8000/docs`*

### 4. Live Inference
To run the system in a continuous loop, fetching new features and generating decisions:
```bash
python scripts/run_inference.py
```

### Available Endpoints
- `GET /`: Health check and system status.
- `GET /api/decision`: (Implementation in `routes.py`) Retrieve the latest market decision and position sizing.

---

## 🤝 Contributing

We welcome contributions to improve the Fotuna FX Engine! Whether it's optimizing model performance or adding new data sources, your help is appreciated.

### How to Contribute

1. **Fork the repository** - Click the 'Fork' button at the top right.
2. **Create a feature branch** 
   ```bash
   git checkout -b feature/improved-sentiment-analysis
   ```
3. **Make your changes** - Ensure code follows existing styles.
4. **Test thoroughly** - Run the test suite:
   ```bash
   pytest tests/
   ```
5. **Commit your changes**
   ```bash
   git commit -m 'Add: Integration for new Macro-API source'
   ```
6. **Push to your branch**
   ```bash
   git push origin feature/improved-sentiment-analysis
   ```
7. **Open a Pull Request** - Describe your changes in detail.

### Ideas for Contributions
- 🧪 **Testing:** Expand coverage in `test_pipeline.py`.
- ✨ **New Filters:** Add filters for additional commodity markets (e.g., Gold).
- ⚡ **Performance:** Optimize the `FeatureEngine` for faster processing of large CSVs.
- 📖 **Documentation:** Add more detailed tutorials for individual model training.

---

## 📝 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for complete details.

### What this means:
- ✅ **Commercial use:** You can use this project commercially.
- ✅ **Modification:** You can modify the code to suit your needs.
- ✅ **Distribution:** You can distribute this software.
- ✅ **Private use:** You can use this project privately.
- ⚠️ **Liability:** The software is provided "as is", without warranty.

---

<p align="center">Made with ❤️ by the Fotuna FX Team</p>
<p align="center">
  <a href="#">⬆️ Back to Top</a>
</p>
