# Dataset Collection & Building Stage

> **Project:** Fraudulent Donation Link Detection Using AI
> **Stage:** Data Collection → Feature Engineering → Dataset Construction
> **Goal of this stage:** Transform a raw list of URLs into a clean, balanced, numerical table (a feature matrix) that a machine learning model can train and test on.

---

## Overview

A machine learning model cannot read a raw URL like `http://urgent-donate-now.xyz`. It can only learn from **numbers**. This stage is about converting every URL in our dataset into a row of measurable features (URL length, domain age, urgency-word count, and so on), each paired with a label (`Legitimate` or `Fraudulent`).

The output of this stage is a single file — `dataset.csv` — which becomes the direct input to the model-training stage.

This stage is split into two parts:

| Part | Name | What happens |
| --- | --- | --- |
| **Part A** | Dataset Collection | Gather and label raw URLs (legitimate + fraudulent) |
| **Part B** | Dataset Building (Feature Engineering) | Use Python to extract numerical features from each URL and assemble the final table |

---

## Part A — Dataset Collection

The model learns to distinguish fraudulent links from legitimate ones, so it needs labelled examples of **both**. Donation-themed URLs are deliberately included on **both sides** so the model learns *fraud patterns*, not just *"does this look charity-related."*

### Class definitions

| Class | Label | Composition |
| --- | --- | --- |
| Fraudulent | `1` | General phishing URLs **+** known fraudulent donation URLs |
| Legitimate | `0` | General legitimate URLs **+** verified charity / donation URLs |

### Data sources

**Fraudulent URLs**

| Source | Description |
| --- | --- |
| PhiUSIIL Phishing URL Dataset | Pre-labelled dataset of ~235,000 URLs (phishing + legitimate). Primary source. |
| PhishTank | Community-reported phishing URLs, downloadable as CSV. |
| OpenPhish | Live phishing feed, updated regularly. |
| URLhaus (abuse.ch) | Malicious URL database, downloadable as CSV. |

**Legitimate donation URLs**

| Source | Description |
| --- | --- |
| Charity Navigator | Rated, verified nonprofits — collect donation page URLs. |
| GiveRadar | Charity intelligence platform covering millions of nonprofits worldwide. |
| BBB Wise Giving Alliance (give.org) | Charities vetted against accountability standards. |
| Major organizations | UNICEF, Red Cross, WHO, Save the Children, Doctors Without Borders, etc. |

### Balancing the dataset

To prevent **class imbalance** (where one class vastly outnumbers the other and biases the model), both classes are matched to an equal count:

1. Collect the realistically available number of legitimate donation URLs (target: **200–500**).
2. Randomly **downsample** the large phishing pool to the same count.
3. Final dataset is balanced — e.g. 500 legitimate / 500 fraudulent.

> **Note:** A Decision Tree classifier performs well on a few hundred to a couple thousand rows per class. Tens of thousands of rows are not required.

### Output of Part A

A two-column file:

| URL | label |
| --- | --- |
| `https://www.unicef.org/donate` | 0 |
| `http://urgent-donate-now.xyz` | 1 |

---

## Part B — Dataset Building (Feature Engineering)

Each URL is processed by Python code that automatically extracts **12 numerical features**. These features are grouped into four analysis categories.

### Feature reference

| Category | Feature | Description |
| --- | --- | --- |
| Blacklist | `blacklist_hit` | Whether the URL appears in a known phishing database (0 / 1) |
| URL | `url_length` | Total character length of the URL |
| URL | `num_subdomains` | Number of subdomains |
| URL | `suspicious_keyword_count` | Count of scam-related keywords in the URL |
| URL | `special_character_count` | Count of unusual characters (`@`, `-`, `_`, etc.) |
| URL | `has_https` | Whether the URL uses HTTPS (0 / 1) |
| Domain | `domain_age_days` | Age of the domain in days (from WHOIS) |
| Domain | `domain_expiry_days` | Days until domain expiry |
| Text | `urgency_word_count` | Urgency phrases on the page ("act now", "urgent") |
| Text | `emotional_word_count` | Emotional manipulation phrases ("children are suffering") |
| Text | `call_to_action_count` | Pushy CTAs ("donate now", "send funds") |
| Text | `text_risk_score` | Combined weighted score of the text signals |

### Build workflow

```
URL list (Part A)
       │
       ▼
For each URL, run feature functions:
       ├─ URL parsing      → url_length, num_subdomains, special_char_count, has_https, suspicious_keyword_count
       ├─ WHOIS lookup     → domain_age_days, domain_expiry_days
       ├─ Web scraping     → urgency_word_count, emotional_word_count, call_to_action_count, text_risk_score
       └─ Blacklist check  → blacklist_hit
       │
       ▼
Assemble all features into a Pandas DataFrame
       │
       ▼
Export → dataset.csv   ✅  (ready for model training)
```

### Output of Part B

The final feature matrix:

| URL | blacklist_hit | url_length | num_subdomains | domain_age_days | urgency_word_count | has_https | ... | label |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| unicef.org | 0 | 10 | 1 | 8760 | 0 | 1 | ... | 0 |
| urgent-help.xyz | 1 | 22 | 0 | 12 | 8 | 0 | ... | 1 |

---

## Tools & Libraries

| Library | Purpose in this stage |
| --- | --- |
| `pandas` | Holds the dataset table; adds feature columns; exports to CSV |
| `requests` | Fetches the HTML of each webpage |
| `BeautifulSoup` (`bs4`) | Extracts visible text from the fetched page |
| `python-whois` | Retrieves domain registration / expiry dates |
| `urllib.parse` / `re` | Parses URL structure and matches keyword patterns |

Install with:

```bash
pip install pandas requests beautifulsoup4 python-whois
```

---

## Learning Resources (Watch Order)

These videos cover every skill required to complete this stage. Recommended order is top to bottom.

### 1. Learn Pandas in Under 3 Hours — *Alex The Analyst*
🔗 https://www.youtube.com/watch?v=Mdq1WWSdUtw

The foundation of this stage. Pandas holds the entire dataset in memory as a DataFrame. Used to load the URL+label CSV, add each extracted feature as a new column, filter rows, handle missing values, and export the final `dataset.csv`. **Focus on:** loading a CSV, creating new columns, `.apply()`, filtering, and saving to CSV.

### 2. Web Scraping with BeautifulSoup and Requests — *Corey Schafer*
🔗 https://www.youtube.com/watch?v=ng2o98k983k

Covers installing BeautifulSoup, understanding HTML structure, inspecting pages, searching for elements, error handling, and saving results. **Why it matters:** the text-analysis features (urgency, emotional, and call-to-action word counts) require visiting each URL, pulling the page's visible text, and counting words. `requests` fetches the page; `BeautifulSoup` extracts the text.

### 3. WHOIS Domain Lookup Tool in Python — *NeuralNine*
🔗 https://www.youtube.com/watch?v=bQ0iQblgnbI

A short, focused tutorial on the `python-whois` library. **Why it matters:** the `domain_age_days` feature is one of the strongest fraud signals, since fraudulent donation sites are typically registered on very new domains. This library queries a domain's registration date, which is then subtracted from today's date to compute its age.

### 4. Python regex / urllib.parse — *Corey Schafer*
🔗 https://www.youtube.com/watch?v=K8L6KVGG-7o

**Why it matters:** the URL-structure features (length, subdomain count, special-character count, HTTPS check, suspicious-keyword count) are all derived by breaking apart the URL string. `urllib.parse` and basic regular expressions make this clean and reliable.

### 5. Pandas `.apply()` to a Column *(supplementary)*
🔗 Search: *"pandas apply function to column"*

**Why it matters:** the professional approach is to write one function per feature and run it across all rows at once, e.g. `df['url_length'] = df['URL'].apply(get_url_length)`. This is the "glue" that connects the feature functions to the table.

### Skill-to-feature map

| Resource | Builds these features |
| --- | --- |
| Pandas | The table itself + holds all columns |
| BeautifulSoup + Requests | `urgency_word_count`, `emotional_word_count`, `call_to_action_count`, `text_risk_score` |
| WHOIS | `domain_age_days`, `domain_expiry_days` |
| regex / urllib | `url_length`, `num_subdomains`, `special_character_count`, `has_https`, `suspicious_keyword_count` |
| Simple file / API check | `blacklist_hit` |

---

## Stage Checklist

- [ ] Collect fraudulent URLs (general phishing + donation scams)
- [ ] Collect legitimate URLs (general + verified charities)
- [ ] Assign labels (`0` = Legitimate, `1` = Fraudulent)
- [ ] Balance the two classes via downsampling
- [ ] Write feature-extraction functions (URL, domain, text, blacklist)
- [ ] Run all functions across every URL using Pandas
- [ ] Handle missing/failed lookups (try-except)
- [ ] Export the final feature matrix to `dataset.csv`

---

## Next Stage

➡️ **Model Training & Evaluation** — split the dataset into features (`X`) and labels (`y`), apply K-Fold Cross Validation, train the Decision Tree classifier, and evaluate using Accuracy, Precision, Recall, and F1 Score.
