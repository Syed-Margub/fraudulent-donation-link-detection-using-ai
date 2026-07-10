# Fraudulent Donation Link Detection Using AI

> An interpretable machine-learning system that detects fraudulent donation and charity links by combining established phishing-detection techniques with novel, donation-specific features.

---

## Table of Contents

1. [Overview](#1-overview)
2. [The Problem](#2-the-problem)
3. [What Makes This Project Different](#3-what-makes-this-project-different)
4. [How the System Works](#4-how-the-system-works)
5. [The Dataset](#5-the-dataset)
6. [Feature Set](#6-feature-set)
7. [The Model](#7-the-model)
8. [Repository Structure](#8-repository-structure)
9. [Installation](#9-installation)
10. [Usage](#10-usage)
11. [Project Roadmap](#11-project-roadmap)
12. [Results](#12-results)
13. [Author & Supervision](#13-author--supervision)

---

## 1. Overview

Fraudulent donation links are deceptive URLs that imitate real charities or fundraising campaigns in order to steal money from well-meaning donors. They spike during disasters, humanitarian crises, and emergency appeals, when people are most likely to give quickly and least likely to verify.

This project builds an **AI model that automatically classifies a donation link as legitimate or fraudulent**. It extracts measurable signals from each link — its structure, the age of its domain, the language on its page, and whether it appears on known blacklists — and feeds them into a machine-learning classifier that learns to tell genuine charities from scams.

The system is designed to be **interpretable**: it does not just output a verdict, it can explain *why* a link was flagged, which is essential in a context where people are deciding whether to trust a request for money.

---

## 2. The Problem

Existing phishing detectors are accurate but **context-blind**. They judge a link purely by its surface characteristics and have no understanding of what the website claims to be — so a fake bank login and a fake charity page are treated identically.

At the same time, research that *does* focus on charitable fraud does not operate at the link level. It studies unusual transactions inside a charity's accounts, the wording of crowdfunding campaigns, or scam accounts on social media — never the classification of a donation URL using features specific to the donation context.

There is also **no publicly available dataset** dedicated to fraudulent donation links. This gap is well documented; researchers in this niche have had to build such datasets from scratch.

This project sits precisely in that unaddressed intersection.

---

## 3. What Makes This Project Different

The core contribution is combining two areas that have never been joined: **the link-analysis techniques of phishing detection** and **real-world knowledge of how fake charities operate**.

Alongside the standard, proven detection features, the model introduces **four donation-specific features** that no existing link detector measures. Each one turns an expert fraud-prevention heuristic into a machine-readable signal:

| # | Novel Feature | What it checks |
|---|---------------|----------------|
| 1 | **Emotional-pressure language** | Detects guilt-driven, urgent "donate now" wording designed to rush the donor. |
| 2 | **Proof of legitimacy** | Looks for a charity registration number or tax ID — things real charities show and fakes usually omit. |
| 3 | **Impersonation check** | Compares who registered the site against the charity it claims to be, catching look-alike names. |
| 4 | **Payment-pathway type** | Identifies risky payment methods — gift cards, crypto, wire transfers, personal accounts. |

> **In one sentence:** other models ask *"Does this link look suspicious?"* — this project asks *"Is this actually behaving like a fake charity?"*

---

## 4. How the System Works

Every link passes through **four analysis modules**, whose outputs become the numerical features the model learns from:

```
                 ┌─────────────────────────┐
   Donation URL  │                         │
   ────────────► │   1. Blacklist check    │──► is it a known scam?
                 │   2. URL structure      │──► length, subdomains, keywords...
                 │   3. Domain age (WHOIS) │──► how new is the domain?
                 │   4. On-page text (NLP) │──► urgency / emotion / payment cues
                 │                         │
                 └───────────┬─────────────┘
                             │
                             ▼
                   Feature vector (numbers)
                             │
                             ▼
                   Decision Tree classifier
                             │
                             ▼
              Prediction:  Legitimate  /  Fraudulent
                        (+ an explanation)
```

---

## 5. The Dataset

Because no donation-specific dataset exists, a custom one was built and verified.

| Property | Value |
|----------|-------|
| **Total URLs** | 804 |
| **Fraudulent** (label `1`) | 441 |
| **Legitimate** (label `0`) | 363 |
| **Balance** | ~1.21 : 1 (well balanced) |
| **Liveness** | 100% — every dead link removed |

**How it was built:**

- **Fraudulent links** were sourced from the PhiUSIIL phishing dataset and fresh phishing feeds.
- **Legitimate links** were drawn from the verified-legitimate portion of the same dataset, plus real charity and donation sources.
- Donation- and charity-themed URLs were deliberately included **on both sides**, so the model learns genuine fraud patterns rather than a superficial "charity-themed = safe" shortcut.
- The combined set was **de-duplicated, balanced, and passed through an automated liveness checker** that removed every URL no longer responding — ensuring feature extraction (which depends on reaching each page) runs reliably.

> **Label convention:** `0 = Legitimate`, `1 = Fraudulent`.
> Note: the source PhiUSIIL dataset uses the *inverted* convention (`1 = legitimate`), which was remapped during dataset construction.

---

## 6. Feature Set

Each URL is converted into **12 numerical features** across the four modules, plus the target label.

| # | Feature | Module | Description | Type |
|---|---------|--------|-------------|------|
| 1 | `url_length` | URL | Total characters in the URL | int |
| 2 | `num_subdomains` | URL | Number of sub-domains | int |
| 3 | `special_character_count` | URL | Count of unusual characters (`@`, `-`, `_`, …) | int |
| 4 | `has_https` | URL | Whether the URL uses HTTPS | 0/1 |
| 5 | `suspicious_keyword_count` | URL | Scam-related keywords in the URL | int |
| 6 | `domain_age_days` | Domain | Age of the domain in days (WHOIS) | int |
| 7 | `domain_expiry_days` | Domain | Days until domain expiry | int |
| 8 | `urgency_word_count` | Text | Urgency phrases ("act now", "urgent") | int |
| 9 | `emotional_word_count` | Text | Emotional-manipulation phrases | int |
| 10 | `call_to_action_count` | Text | Pushy CTAs ("donate now") | int |
| 11 | `text_risk_score` | Text | Combined weighted score of text signals | float |
| 12 | `blacklist_hit` | Blacklist | Appears in a known phishing database | 0/1 |
| — | `label` | Target | `0` = Legitimate, `1` = Fraudulent | 0/1 |

> Features 1, 8, and the donation-specific refinements form the basis of this project's novel contribution; the standard lexical and WHOIS features serve as an established, well-validated baseline.

---

## 7. The Model

The classifier is a **Decision Tree**, chosen deliberately to support the project's goals:

- **Interpretability** — it produces clear, human-readable rules, so the system can explain exactly why a link was flagged (e.g. *"3-day-old look-alike domain, no registration number, urgent language, gift-card payment"*). This matters in a trust-sensitive setting.
- **Suits the engineered features** — it handles the mix of numerical and binary features naturally, without needing feature scaling.
- **Efficient on a moderate dataset** — it trains quickly and reliably at this data size.
- **Handles class imbalance** — the slight imbalance is managed with `class_weight='balanced'`.

**Training & evaluation:** the data is split using **K-Fold cross-validation (K = 5)**, and performance is measured with **Accuracy, Precision, Recall, F1-score**, and a **confusion matrix**.

---

## 8. Repository Structure

```
fraudulent-donation-link-detection-using-ai/
├── data/                 # Datasets (raw, live, final)
│   └── dataset_live_links.csv
├── notebooks/            # Jupyter notebooks for each stage
├── scripts/              # Python scripts (feature extraction, liveness check)
├── outputs/              # Generated files (feature table, trained model, charts)
├── docs/                 # Reports and documentation
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

---

## 9. Installation

**Requirements:** Python 3.9+

```bash
# 1. Clone the repository
git clone https://github.com/Syed-Margub/fraudulent-donation-link-detection-using-ai.git
cd fraudulent-donation-link-detection-using-ai

# 2. (Optional) create a virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

**Dependencies:** `pandas`, `requests`, `beautifulsoup4`, `python-whois`, `scikit-learn`, `matplotlib`, `seaborn`

---

## 10. Usage

```python
import pandas as pd

# Load the dataset
df = pd.read_csv("data/dataset_live_links.csv")
print(df.shape)                    # (804, 2)
print(df['label'].value_counts())  # 1: 441 (fraud), 0: 363 (legit)
```

Full feature-extraction and model-training instructions will be added to the `notebooks/` and `scripts/` folders as those stages are completed.

---

## 11. Project Roadmap

The project is tracked via GitHub Issues across five milestones:

- [x] **Milestone 1 — Project Setup & Planning**
- [x] **Milestone 2 — Dataset Collection & Building**
- [ ] **Milestone 3 — Feature Engineering** *(in progress)*
- [ ] **Milestone 4 — Model Training & Evaluation**
- [ ] **Milestone 5 — Testing, Documentation & Delivery**

---

## 12. Results

*To be completed after model training and evaluation.*

| Metric | Score |
|--------|-------|
| Accuracy | — |
| Precision | — |
| Recall | — |
| F1-score | — |

---

## 13. Author & Supervision

**Author:** Syed Margub
**Supervisor:** Dr. Yasir
**Type:** Research internship project

---

<p align="center"><i>This project extends phishing-link detection into the donation domain — giving an accurate detector the context and explainability it has always lacked.</i></p>
