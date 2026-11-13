# Ontology-Based Customer Review Sentiment Analysis System

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1.3-green.svg)](https://palletsprojects.com/p/flask/)
[![RDFLib](https://img.shields.io/badge/RDFLib-7.6.0-yellow.svg)](https://rdflib.readthedocs.io/)
[![License](https://img.shields.io/badge/License-Academic-lightgrey.svg)]()

> A full-stack, ontology-driven natural language processing web application that combines semantic web technologies (OWL/RDF) with context-sensitive sentiment reasoning to conduct aspect-level customer review analysis.

---

## 1. Project Abstract

Customer review sentiment analysis is an essential capability for modern e-commerce and consumer intelligence. Traditional lexicon-based approaches (such as simple bag-of-words or positive/negative word frequency counters) typically evaluate text uniformly, obscuring vital multi-aspect nuances where a customer praises one feature (e.g., *"The camera is excellent"*) while criticizing another (e.g., *"but the battery is poor"*). 

This project presents an **Ontology-Based Customer Review Sentiment Analysis System**. Built on a formal, Protégé-compatible OWL 2 ontology (`customer_review_ontology.owl`), the system employs semantic relationships between products, product categories, feature hierarchies, opinion expressions, and polarity categories. Using Python's **RDFLib**, text preprocessing with contraction expansion and negation retention, clause boundary segmentation, and deductive reasoning rules, the engine resolves aspect-level sentiments, handles negation inversion (e.g., *"not good"* vs. *"not bad"*), weighs linguistic intensifiers, classifies contradictory reviews as **Mixed**, and produces explainable reasoning traces. The project includes an interactive web interface built with Flask, SQLite/SQLAlchemy, Chart.js, Vis-network graph visualization, CSV dataset batch processing, and on-demand CSV/PDF report generation.

---

## 2. Problem Statement

Standard sentiment analysis techniques suffer from significant limitations when applied to real-world customer feedback:
1. **Lack of Aspect Awareness:** Evaluating an entire review with a single positive or negative label fails when a customer expresses contrasting opinions about different product attributes.
2. **Context Insensitivity:** Simple keyword matchers fail to distinguish between negated statements (*"not good"* $\rightarrow$ negative) and attenuations (*"not bad"* $\rightarrow$ positive).
3. **Absence of Domain Knowledge:** Bag-of-words models do not understand that *"lens"*, *"cam"*, and *"photo"* represent the concept **Camera**, or that *"shipping"*, *"courier"*, and *"transit"* represent **Delivery**.
4. **Opaque Black-Box Classifications:** Pure statistical or black-box classifiers cannot provide transparent explanations to business stakeholders indicating *why* a particular rating was determined.

---

## 3. Proposed System

The proposed system addresses these shortcomings by integrating an **OWL 2 Knowledge Base** with a rule-based semantic reasoning engine:
* **Domain Ontology:** A formal semantic model defining products (Smartphones, Laptops, Headphones, Online Shopping), their feature hierarchies, and an evaluative opinion lexicon with synonym mappings.
* **Aspect-Level Sentiment Extraction:** Segments compound reviews into clauses using contrast markers (*"but"*, *"however"*, *"although"*), associating opinion words with the specific features mentioned in each clause.
* **Negation & Modifier Engine:** Explicitly models polarity inversion (*"not clear"* $\rightarrow$ negative) and negated negative moderation (*"not bad"* $\rightarrow$ mildly positive), while scaling scores via intensifiers (*"very"*, *"extremely"*).
* **Transparent Inference Trace:** Explains every decision step by citing the matched ontology concepts, clauses, and semantic rules.
* **Dynamic Interactive Analytics:** Visualizes real-time sentiment distributions, aspect-level satisfaction rankings, and interactive knowledge graphs.

---

## 4. System Architecture & Data Flow

```
+-------------------------------------------------------------------------------+
|                                FRONTEND UI                                    |
|   HTML5 + CSS3 + Bootstrap 5 + Bootstrap Icons + Chart.js + Vis-Network.js    |
+-------------------------------------------------------------------------------+
                                        | (HTTP / REST)
                                        v
+-------------------------------------------------------------------------------+
|                              FLASK BACKEND                                    |
|  [routes/auth]  [routes/review]  [routes/dashboard]  [routes/ontology]  [report]  |
+-------------------------------------------------------------------------------+
         |                              |                               |
         v                              v                               v
+------------------+         +---------------------+         +------------------+
|  SQLITE DATABASE |         |  ANALYSIS PIPELINE  |         |   REPORT ENGINE  |
|  (SQLAlchemy)    |         | 1. Preprocessing    |         | 1. Sanitized CSV |
|  - Users         |         | 2. Clause Splitting |         | 2. Standards PDF |
|  - Products      |         | 3. Feature Binding  |         +------------------+
|  - Reviews       |         | 4. Context Rules    |
|  - AspectSentiments        +---------------------+
+------------------+                    |
                                        v
                       +---------------------------------+
                       |     ONTOLOGY KNOWLEDGE BASE     |
                       | customer_review_ontology.owl    |
                       |       (RDFLib Graph Engine)     |
                       +---------------------------------+
```

### Data Flow Steps:
1. **Input Submission:** A user submits a customer review via manual entry or CSV dataset upload.
2. **Text Preprocessing:** Expands contractions (*"won't"* $\rightarrow$ *"will not"*), cleans whitespace, and preserves negation tokens (*"not"*, *"never"*).
3. **Clause Segmentation:** Splits text across punctuation and contrast conjunctions (*"but"*, *"however"*).
4. **Ontology Concept Matching:** Matches n-grams to ontology features (`ProductFeature`) and opinion terms (`Opinion`).
5. **Contextual Evaluation:** Applies negation windows, modifier scaling, and aspect polarity score calculations.
6. **Deductive Synthesis:** Aggregates feature polarities; assigns **Positive**, **Negative**, **Neutral**, or **Mixed** classification.
7. **Storage & Visualization:** Persists findings in SQLite; updates Chart.js dashboard charts and review histories.

---

## 5. Ontology Design

The ontology is serialized in Protégé-compatible OWL 2 RDF/XML format (`ontology/customer_review_ontology.owl`).

### A. Core Classes
* `Product`: Concrete products subjected to review.
* `ProductCategory`: Domain classification (`Smartphone`, `Laptop`, `Headphones`, `OnlineShopping`).
* `ProductFeature`: Component or attribute (`Camera`, `Battery`, `Display`, `Delivery`, `SoundQuality`, etc.).
* `Opinion`: Evaluative linguistic expression (`excellent`, `poor`, `terrible`, `clear`, etc.).
* `Sentiment`: Top-level polarity class.
  * `PositiveSentiment` (SubClass)
  * `NegativeSentiment` (SubClass)
  * `NeutralSentiment` (SubClass)
  * `MixedSentiment` (SubClass)
* `CustomerReview`: Textual review instance.
* `Customer`: Author entity.

### B. Object Properties
* `hasCategory` (`Product` $\rightarrow$ `ProductCategory`)
* `hasFeature` (`Product` $\rightarrow$ `ProductFeature`)
* `mentionsFeature` (`CustomerReview` $\rightarrow$ `ProductFeature`)
* `expressesOpinion` (`CustomerReview` $\rightarrow$ `Opinion`)
* `hasSentiment` (`Opinion` $\rightarrow$ `Sentiment`)
* `reviewsProduct` (`CustomerReview` $\rightarrow$ `Product`)

### C. Data Properties
* `reviewText` (`xsd:string`)
* `productName` (`xsd:string`)
* `opinionWord` (`xsd:string`)
* `sentimentScore` (`xsd:float`)
* `reviewDate` (`xsd:dateTime`)

### D. Modeled Instances & Feature Mappings
| Domain | Products Modeled | Features Modeled & Synonyms |
| :--- | :--- | :--- |
| **Smartphone** | iPhone 15 Pro, Samsung Galaxy S24, Pixel 8 | Camera (*lens, cam, photo*), Battery (*charge, backup*), Display (*screen, OLED*), Performance (*speed*), Price (*cost*), Design (*finish*) |
| **Laptop** | MacBook Pro M3, Dell XPS 15, ThinkPad X1 | Processor (*CPU, chip*), Battery, Keyboard (*keys, typing*), Display, Performance, Price |
| **Headphones** | Sony WH-1000XM5, Bose QC45, AirPods Pro 2 | SoundQuality (*audio, bass, clarity*), Battery, Comfort (*fit, cushioning*), NoiseCancellation (*ANC*), Price |
| **Online Shopping** | Amazon Shopping, Flipkart Order | Delivery (*shipping, courier*), Packaging (*box*), ProductQuality (*authenticity*), CustomerService (*support, refund*), Price |

---

## 6. Technology Stack

* **Programming Language:** Python 3.10+ (tested on Python 3.14)
* **Web Framework:** Flask 3.1.3
* **Database & ORM:** SQLite 3, SQLAlchemy 2.1.4, Flask-SQLAlchemy 3.1.1
* **Knowledge Base Engine:** RDFLib 7.6.0 (OWL 2 RDF/XML parser and SPARQL engine)
* **Frontend Design:** HTML5, CSS3, JavaScript (ES6+), Bootstrap 5.3.3, Bootstrap Icons 1.11.3
* **Analytics Visualization:** Chart.js 4.4.2
* **Network Graph Visualization:** Vis-Network.js
* **Reporting:** Native pure-Python standard PDF generator (PDF-1.4) & Sanitized CSV exporter
* **Security:** Werkzeug password hashing (PBKDF2:SHA256), session protection, input sanitation

---

## 7. Installation & Setup Guide (Windows)

### Prerequisites
* Windows 10 or 11
* Python 3.10 or higher installed (with `Add Python to PATH` checked)

### Step 1: Clone or Navigate to the Project Directory
Open PowerShell or Command Prompt:
```powershell
cd c:\Users\prana\OneDrive\Desktop\fpro
```

### Step 2: (Optional) Create and Activate Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Step 3: Install Required Dependencies
```powershell
pip install -r requirements.txt
```

### Step 4: Verify Environment Configuration
A `.env.example` file is provided. The application runs with safe defaults automatically. If you wish to customize keys:
```powershell
copy .env.example .env
```

---

## 8. Running the Application

Start the Flask development server:
```powershell
python app.py
```

### Accessing the Web Application
Open your web browser and navigate to:
```
http://127.0.0.1:5000
```

### Default Demonstration Credentials
A secure administrator account is initialized automatically on first startup:
* **Email:** `admin@sentiment.local`
* **Password:** `Admin@12345`

You may also register your own account through the registration page at `/register`.

---

## 9. Modules Walkthrough & How to Use

1. **Home / Landing Page (`/`):**
   * Overview of project objectives, semantic pipeline, and comparison with bag-of-words limitations.
2. **Dashboard (`/dashboard`):**
   * Dynamic metrics: Total Reviews, Positive %, Negative %, Neutral %, Mixed %.
   * Chart.js Doughnut chart (Sentiment distribution) & Stacked Bar chart (Feature breakdown).
   * Aspect leaders table highlighting features with the most positive and negative feedback.
   * Filter reviews by category, product, or sentiment.
3. **Analyze Single Review (`/analyze`):**
   * Type any customer review or click one of the pre-set demonstration buttons.
   * View the preprocessed text, aspect-level classifications, scores, and full deductive inference trace.
4. **Upload Dataset (`/upload`):**
   * Upload custom CSV review datasets.
   * Or click the **"Load Sample Dataset"** button to instantly populate 35 realistic customer reviews across Smartphones, Laptops, Headphones, and Online Shopping.
5. **Review History (`/history`):**
   * Search reviews by keyword or product name.
   * Filter, sort by date, paginate, re-analyze with updated rules, or delete records.
6. **Feature-wise Analysis (`/features`):**
   * Drill down into individual product features (Camera, Battery, Display, etc.) with sentiment percentages and representative customer quotes.
7. **Ontology Explorer (`/ontology`):**
   * Pan, zoom, and drag nodes in the interactive Vis-network graph.
   * Click on any node to view its URI and ontology properties.
   * Inspect formal tables for classes, object properties, data properties, and reasoning rules.
8. **Export Reports (`/reports`):**
   * Download filtered datasets in sanitized CSV format or as a structured, professional PDF report.

---

## 10. Sample Test Demonstrations

| Review Text | Identified Feature | Opinion Word | Feature Polarity | Overall Sentiment | Applied Semantic Rule |
| :--- | :--- | :--- | :--- | :--- | :--- |
| *"The camera is excellent."* | Camera | excellent | Positive (+1.0) | **Positive** | Direct feature-opinion binding |
| *"The battery is terrible."* | Battery | terrible | Negative (-0.95) | **Negative** | Direct negative appraisal |
| *"The phone arrived yesterday."* | None | arrived | Neutral (0.0) | **Neutral** | Factual statement without sentiment |
| *"The camera is good, but the battery is poor."* | Camera, Battery | good, poor | Cam: +0.7, Bat: -0.75 | **Mixed** | Contrast clause splitting across *"but"* |
| *"The camera is not good."* | Camera | good | Negative (-0.63) | **Negative** | Negation window inverted polarity |
| *"The battery is not bad."* | Battery | bad | Positive (+0.45) | **Positive** | Negated negative attenuation rule |
| *"The laptop display is very clear."* | Display | clear | Positive (+1.0) | **Positive** | Intensifier (*"very"*) 1.5x multiplier |
| *"The headphones are comfortable, but the sound quality is terrible."* | Comfort, SoundQuality | comfortable, terrible | Comf: +0.8, Snd: -0.95 | **Mixed** | Aspect conflict produces Mixed sentiment |
| *"The delivery was slow."* | Delivery | slow | Negative (-0.7) | **Negative** | Online shopping feature binding |
| *"" (Empty text)* | — | — | — | **Validation Error** | Rejection with `ValueError` |

---

## 11. Automated Test Suite

The project includes an automated test suite verifying all 10 core demonstration test cases, text preprocessing, ontology parsing, database relationships, and authentication.

To execute all tests:
```powershell
python -m unittest discover tests -v
```

### Test Results Summary:
```
test_protected_route_redirect (test_auth.TestAuthentication) .......................... ok
test_user_registration_and_hash (test_auth.TestAuthentication) ........................ ok
test_web_login_flow_invalid_password (test_auth.TestAuthentication) ................... ok
test_web_login_flow_success (test_auth.TestAuthentication) ............................ ok
test_web_registration_flow (test_auth.TestAuthentication) ............................. ok
test_classes_exist (test_ontology.TestOntologyService) ................................. ok
test_feature_synonym_matching (test_ontology.TestOntologyService) ...................... ok
test_ontology_loaded (test_ontology.TestOntologyService) ............................... ok
test_opinion_polarity_lookup (test_ontology.TestOntologyService) ....................... ok
test_clause_splitting (test_preprocessing.TestTextPreprocessing) ....................... ok
test_contraction_expansion (test_preprocessing.TestTextPreprocessing) .................. ok
test_negation_preservation (test_preprocessing.TestTextPreprocessing) .................. ok
test_whitespace_normalization (test_preprocessing.TestTextPreprocessing) ............... ok
test_cascade_delete (test_reviews.TestReviewPersistence) ............................... ok
test_create_review_with_features (test_reviews.TestReviewPersistence) .................. ok
test_case_1_positive_camera (test_sentiment.TestSentimentAnalysisEngine) ............... ok
test_case_2_negative_battery (test_sentiment.TestSentimentAnalysisEngine) .............. ok
test_case_3_neutral_phone (test_sentiment.TestSentimentAnalysisEngine) ................. ok
test_case_4_mixed_camera_and_battery (test_sentiment.TestSentimentAnalysisEngine) ...... ok
test_case_5_negation_not_good (test_sentiment.TestSentimentAnalysisEngine) .............. ok
test_case_6_negation_not_bad (test_sentiment.TestSentimentAnalysisEngine) ............... ok
test_case_7_display_very_clear (test_sentiment.TestSentimentAnalysisEngine) ............. ok
test_case_8_mixed_headphones (test_sentiment.TestSentimentAnalysisEngine) .............. ok
test_case_9_delivery_slow (test_sentiment.TestSentimentAnalysisEngine) .................. ok
test_case_10_empty_review_validation (test_sentiment.TestSentimentAnalysisEngine) ...... ok

----------------------------------------------------------------------
Ran 25 tests in 2.315s
OK
```

---

## 12. Known Limitations & Educational Notes

* **Rule-Based Semantic Interpretation:** The ontology engine relies on syntactic clause splitting and semantic lexicon matching. While explainable and fast, it may not detect subtle irony, sarcasm (e.g., *"Oh great, another broken screen"*), or complex slang not present in the ontology vocabulary.
* **Complex Multi-Clause Anaphora:** In sentences with pronouns referring to aspects mentioned multiple sentences prior (e.g., *"I bought the phone. It was fast. But then it stopped."*), aspect coreference is resolved locally within clauses.
* **Vocabulary Expansion:** If a product feature or opinion word is completely missing from the ontology, it evaluates to general sentiment rather than a specific aspect. New terms can be added directly to `customer_review_ontology.owl`.

---

## 13. Future Enhancements

1. **Hybrid Transformer Integration:** Pairing the ontology knowledge graph with a fine-tuned lightweight BERT or RoBERTa model to achieve high linguistic generalizability with strict ontological explainability.
2. **Automated Ontology Learning:** Automatically proposing new candidate feature and opinion individuals from large incoming review streams using clustering and frequency analysis.
3. **Multi-Language Support:** Expanding the OWL ontology lexicon to include multilingual synonym properties (`cro:synonym` with language tags `@es`, `@fr`, `@hi`).

---

## 14. Project Directory Structure

```
fpro/
├── app.py                          # Application factory, database seed, route registration
├── config.py                       # Configuration (SQLite URI, upload limits, secret keys)
├── models.py                       # SQLAlchemy ORM models (User, Product, Review, FeatureSentiment)
├── requirements.txt                # Python package dependencies
├── .env.example                    # Environment template
├── README.md                       # Academic project documentation and demonstration guide
│
├── ontology/
│   └── customer_review_ontology.owl # Protégé-compatible OWL 2 RDF/XML Knowledge Base
│
├── services/
│   ├── preprocessing.py            # Contraction expansion, normalization, negation retention
│   ├── ontology_service.py         # RDFLib OWL loader, graph queries, Vis-Network exporter
│   ├── reasoning_engine.py         # Clause segmentation, aspect-opinion binding, deduction trace
│   ├── sentiment_analyzer.py       # Polarity scoring, negation inversion, aspect synthesis
│   └── report_service.py           # Sanitized CSV and standard PDF report generation
│
├── routes/
│   ├── auth_routes.py              # User authentication, registration, session management
│   ├── review_routes.py            # Review analysis, dataset upload, history, details, reanalysis
│   ├── dashboard_routes.py         # Analytics dashboard, Chart.js API, feature-level analysis
│   ├── ontology_routes.py          # Ontology explorer and graph visualization API
│   └── report_routes.py            # CSV and PDF download endpoints
│
├── templates/
│   ├── base.html                   # Master layout with responsive navbar, sidebar, and footer
│   ├── index.html                  # Academic landing page with theory, features, and pipeline
│   ├── login.html                  # User login form
│   ├── register.html               # User registration form
│   ├── dashboard.html              # Analytics dashboard with Chart.js charts and filters
│   ├── analyze_review.html         # Interactive review tester with live aspect breakdown
│   ├── upload_dataset.html         # Batch CSV upload and sample dataset loader
│   ├── review_history.html         # Searchable, filterable, paginated review table
│   ├── review_details.html         # Detailed review inspector with text comparison and evidence
│   ├── feature_analysis.html       # Aspect-level sentiment drilldown across products
│   ├── ontology_explorer.html      # Interactive Vis-network graph and schema specification
│   ├── reports.html                # Reports hub for CSV and PDF downloads
│   └── settings.html               # Account profile and system diagnostics
│
├── static/
│   ├── css/
│   │   └── style.css               # Professional Navy/Blue theme, badges, and layout styles
│   └── js/
│       ├── main.js                 # General front-end utilities and sample review insert buttons
│       ├── dashboard.js            # Chart.js initialization and dynamic API update handlers
│       └── ontology_graph.js       # Vis-network interactive graph rendering and click inspector
│
├── sample_data/
│   └── sample_reviews.csv          # 35 realistic customer reviews across 4 domains
│
└── tests/
    ├── test_sentiment.py           # 10 core required project sentiment test cases
    ├── test_preprocessing.py       # Contraction expansion, negation preservation, clause splitting
    ├── test_ontology.py            # RDFLib ontology parsing, classes, properties, synonyms
    ├── test_auth.py                # Authentication, password hashing, protected routes
    └── test_reviews.py             # Database persistence, foreign keys, cascade deletion
```
