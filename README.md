# Fraudulent Donation Link Detection Using AI

## Overview

With the rise of global humanitarian crises, natural disasters, and emergency fundraising campaigns, many individuals turn to online platforms to donate and support affected communities. Unfortunately, cybercriminals often exploit public trust by creating fraudulent donation websites and malicious donation links that impersonate legitimate charities or use emotional manipulation to deceive donors.

This project aims to develop a hybrid AI-based fraud detection system capable of identifying potentially fraudulent donation links through a combination of reputation analysis, URL structure analysis, domain intelligence, webpage content analysis, and machine learning techniques.

The system provides an interpretable risk assessment that helps users determine whether a donation link is likely to be legitimate, suspicious, or fraudulent.

---

# Objectives

* Detect fraudulent donation links using a multi-layered detection framework.
* Extract meaningful structural, temporal, and textual features from donation URLs and webpages.
* Analyze domain-related metadata such as domain age.
* Identify suspicious patterns commonly found in scam donation campaigns.
* Train a machine learning model to classify donation links.
* Generate interpretable risk scores and classifications.
* Evaluate detection performance using cross-validation and standard machine learning metrics.

---

# Detection Pipeline

The system evaluates a given URL using four primary analysis modules.

## 1. Blacklist Checking (Reputation-Based Analysis)

Checks whether the URL or domain appears in known phishing, scam, or malicious website databases.

### Potential Sources

* PhishTank
* OpenPhish
* URLhaus
* Google Safe Browsing (if integrated)

### Purpose

Provides rapid detection for previously reported malicious websites.

### Example Feature

```python
blacklist_hit = True
```

---

## 2. URL Structure Analysis (Structural Analysis)

Analyzes characteristics of the URL itself.

### Features Extracted

* URL length
* Number of subdomains
* Presence of suspicious keywords
* Use of special characters
* Excessive hyphens
* Presence of IP addresses instead of domain names
* HTTPS usage
* Unusual URL patterns

### Example

```text
http://urgent-donation-help-now.xyz
```

Possible indicators:

* Long URL
* Suspicious keywords
* Newly registered domain
* Uncommon top-level domain

---

## 3. Domain Age Analysis (Temporal Analysis)

Retrieves domain registration information and calculates domain age.

### Features Extracted

* Domain creation date
* Domain age (days)
* Domain expiration date (optional)

### Assumption

Fraudulent donation campaigns are often hosted on recently created domains.

### Example

```text
Domain Age = 12 days
```

Higher risk than:

```text
Domain Age = 8 years
```

---

## 4. Webpage Text Analysis (Textual / NLP Analysis)

Extracts visible webpage content and analyzes linguistic patterns.

### Features Extracted

#### Urgency Indicators

Examples:

```text
Act Now
Donate Immediately
Emergency Appeal
Limited Time
Urgent Help Needed
```

#### Emotional Manipulation Indicators

Examples:

```text
Save Lives
Children Are Suffering
People Are Dying
Help Before It's Too Late
```

#### Call-To-Action Indicators

Examples:

```text
Donate Now
Click Here
Support Today
Send Funds Immediately
```

### Text-Based Metrics

* Urgency word count
* Emotional word count
* Call-to-action count
* Text risk score

---

# Machine Learning Component

## Decision Tree Classifier

The project uses a Decision Tree classifier to learn fraud patterns from extracted URL and webpage features.

Decision Trees are chosen because they:

* Are easy to interpret
* Produce explainable decision rules
* Handle mixed feature types well
* Allow visualization of decision-making paths

### Input Features

Examples:

* blacklist_hit
* url_length
* num_subdomains
* suspicious_keyword_count
* has_https
* domain_age_days
* urgency_word_count
* emotional_word_count
* call_to_action_count
* text_risk_score

### Target Labels

```text
0 = Legitimate
1 = Fraudulent
```

or

```text
Legitimate
Suspicious
Fraudulent
```

depending on dataset design.

---

# Dataset Strategy

The project combines publicly available phishing datasets with donation-specific data collection.

## Dataset 1: General Phishing Dataset

Used for primary model training.

Potential sources:

* UCI PhiUSIIL Phishing URL Dataset
* Kaggle Phishing URL Datasets
* OpenPhish
* PhishTank
* URLhaus

Labels:

```text
Legitimate
Phishing
```

Phishing URLs are treated as fraudulent examples.

---

## Dataset 2: Donation-Specific Dataset

A custom dataset created specifically for this project.

### Legitimate Donation Sources

Examples:

* UNICEF
* International Committee of the Red Cross
* Save the Children
* Doctors Without Borders
* Islamic Relief

### Fraudulent Donation Sources

Collected from:

* PhishTank reports
* OpenPhish feeds
* URLhaus feeds
* Public scam reports
* Charity fraud warnings

Labels:

```text
Legitimate
Fraudulent
```

---

# Feature Engineering

The following features are planned for extraction:

| Category  | Features                 |
| --------- | ------------------------ |
| Blacklist | blacklist_hit            |
| URL       | url_length               |
| URL       | num_subdomains           |
| URL       | suspicious_keyword_count |
| URL       | special_character_count  |
| URL       | has_https                |
| Domain    | domain_age_days          |
| Domain    | domain_expiry_days       |
| Text      | urgency_word_count       |
| Text      | emotional_word_count     |
| Text      | call_to_action_count     |
| Text      | text_risk_score          |

---

# Model Evaluation

## K-Fold Cross Validation

To obtain reliable and unbiased performance estimates, the model will be evaluated using K-Fold Cross Validation.

### Procedure

1. Split dataset into K folds.
2. Use K-1 folds for training.
3. Use remaining fold for testing.
4. Repeat until every fold has served as the test set.
5. Average results across all folds.

Example:

```text
K = 5

Fold 1 → Train + Test
Fold 2 → Train + Test
Fold 3 → Train + Test
Fold 4 → Train + Test
Fold 5 → Train + Test
```

### Benefits

* Better generalization estimates
* Reduced risk of overfitting
* More reliable evaluation than a single train-test split

---

# Evaluation Metrics

The model will be evaluated using:

### Classification Metrics

* Accuracy
* Precision
* Recall
* F1 Score

### Additional Analysis

* Confusion Matrix
* Feature Importance Analysis
* Decision Tree Visualization

---

# Risk Scoring Framework

In addition to machine learning classification, a rule-based risk scoring mechanism may be implemented.

Each module contributes a weighted risk score.

Example:

```text
Blacklist Hit         +40
Very New Domain       +20
Many Suspicious Words +15
High Urgency Language +10
```

Total score determines overall risk level.

Example:

```text
0–20     → Low Risk
21–50    → Suspicious
51+       → High Risk
```

---

# Example Output

```json
{
  "url": "http://example-donation-link.com",
  "blacklist_hit": false,
  "url_length": 58,
  "domain_age_days": 17,
  "urgency_word_count": 8,
  "emotional_word_count": 6,
  "text_risk_score": 14,
  "final_score": 33,
  "classification": "Suspicious"
}
```

---

# Future Improvements

* Random Forest comparison
* XGBoost comparison
* Real-time browser extension
* Web application interface
* Deep learning based text analysis
* Charity verification database integration
* Explainable AI (XAI) visualizations

---

# Technologies

* Python
* Pandas
* NumPy
* Scikit-learn
* BeautifulSoup
* Requests
* Whois
* Matplotlib
* Seaborn
* Jupyter Notebook

---

# Project Status

Current Stage:

* Project Planning
* Dataset Collection
* Feature Engineering Design
* Detection Pipeline Design
* Machine Learning Model Selection (Decision Tree)
* K-Fold Cross Validation Planning

Next Stage:

* Dataset Collection
* Feature Extraction Implementation
* Model Training
* Evaluation and Analysis
* Final Report Preparation
