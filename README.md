# Fraudulent Donation Link Detection Using AI

##Overview
With the rise of global humanitarian crises, many individuals turn to online platforms to donate and support affected communities. Unfortunately, this has also led to an increase in fraudulent donation links that exploit public trust.

This project aims to develop a **hybrid fraud detection system** that analyzes donation links using multiple indicators, including blacklist databases, URL structure, domain age, and webpage content.

The goal is to identify potentially fraudulent donation links and provide an interpretable risk assessment.

---

## Objectives
- Detect fraudulent donation links using a multi-layered approach
- Extract meaningful features from URLs and webpage content
- Analyze domain-related metadata such as domain age
- Develop a risk scoring and classification system
- Evaluate the effectiveness of different detection strategies

---

## Detection Pipeline

The system evaluates a given URL using four key methods:

### 1. Blacklist Checking (Reputation-Based)
- Compares URLs/domains against known scam databases
- Provides fast detection for previously identified threats

### 2. URL Structure Analysis (Structural)
- Analyzes URL characteristics such as:
  - Length of URL
  - Number of subdomains
  - Presence of suspicious keywords (e.g., "donate", "urgent")
  - Use of special characters or unusual patterns

### 3. Domain Age Analysis (Temporal)
- Retrieves domain creation date
- Computes domain age
- Flags newly created domains as higher risk

### 4. Webpage Text Analysis (Textual / NLP)
- Extracts webpage content
- Detects:
  - Urgency language (e.g., "act now", "urgent")
  - Emotional manipulation (e.g., "save lives", "suffering")
  - Excessive calls to action

---

## System Design

The system combines all extracted features into a **risk scoring framework**:

- Each module contributes to an overall risk score
- The final classification is based on combined signals

### Example Output
```json
{
  "url": "http://example-donation-link.com",
  "blacklist_hit": false,
  "url_risk_score": 12,
  "domain_age_days": 17,
  "text_risk_score": 14,
  "final_score": 33,
  "classification": "Suspicious"
}
