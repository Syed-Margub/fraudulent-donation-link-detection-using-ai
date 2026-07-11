# Detection Approach & Feature Plan

> Planning document for the Fraudulent Donation Link Detection project. It defines the detection strategy, the full feature set, the label convention, and the dataset rationale — the design decisions made before feature-engineering code begins.

---

## 1. The Four Analysis Modules

Every link is evaluated by four independent modules. Each contributes a group of numerical features to the final table, so a weakness in one module is compensated by the others.

### Module 1 — Blacklist Check
Checks whether the URL appears on an external database of known-malicious links (PhishTank, URLhaus, OpenPhish). This is a reputation signal, completely independent of the project's own labels.
- **Signal:** a direct hit is the strongest possible indicator of fraud.
- **Limitation:** only catches already-reported URLs; fresh scams are usually absent, which is precisely why machine learning is needed.

### Module 2 — URL Structure Analysis
Examines the URL string itself, without visiting the page. Scam URLs tend to be long, use many sub-domains, avoid HTTPS, contain unusual characters, and embed suspicious keywords.
- **Signal:** cheap, reliable, and works even for dead links.

### Module 3 — Domain Age (WHOIS)
Looks up each domain's registration and expiry dates. Fraudulent donation sites are typically registered days before a campaign; legitimate charities have long histories.
- **Signal:** domain age is one of the strongest single predictors of fraud.

### Module 4 — On-Page Text Analysis (NLP)
Fetches the page and analyses its visible text for manipulation cues — urgency, emotional pressure, and pushy calls to action — as well as the donation-specific signals that form this project's novel contribution.
- **Signal:** captures the *behaviour* of a fake charity, not just the shape of its link.

```
                 +-------------------------+
   Donation URL  |  1. Blacklist check     |
   ------------> |  2. URL structure       |  -->  feature vector  -->  model
                 |  3. Domain age (WHOIS)  |
                 |  4. On-page text (NLP)  |
                 +-------------------------+
```

---

## 2. Planned Feature Set (12 features + label)

Each URL is converted into the following numerical features. Features are grouped by the module that produces them.

| # | Feature | Module | Description | Type |
|---|---------|--------|-------------|------|
| 1 | `url_length` | URL Structure | Total number of characters in the URL | int |
| 2 | `num_subdomains` | URL Structure | Number of sub-domains in the host | int |
| 3 | `special_character_count` | URL Structure | Count of unusual characters (`@`, `-`, `_`, `//`) | int |
| 4 | `has_https` | URL Structure | Whether the URL uses HTTPS (1 = yes, 0 = no) | binary |
| 5 | `suspicious_keyword_count` | URL Structure | Count of scam-related keywords in the URL | int |
| 6 | `domain_age_days` | Domain | Age of the domain in days since registration | int |
| 7 | `domain_expiry_days` | Domain | Days remaining until domain expiry | int |
| 8 | `urgency_word_count` | Text (NLP) | Count of urgency phrases ("act now", "urgent") | int |
| 9 | `emotional_word_count` | Text (NLP) | Count of emotional-manipulation phrases | int |
| 10 | `call_to_action_count` | Text (NLP) | Count of pushy CTAs ("donate now", "send funds") | int |
| 11 | `text_risk_score` | Text (NLP) | Combined weighted score of the text signals | float |
| 12 | `blacklist_hit` | Blacklist | Whether the URL is on a known phishing database | binary |
| — | `label` | Target | Class label (see Section 3) | binary |

### Novel donation-specific features (the research contribution)
Beyond the standard baseline above, four donation-specific features distinguish this project from general phishing detectors. They are implemented as refinements/extensions within the Text module:

1. **Emotional-pressure language** — a donation-specific lexicon detecting guilt-driven, urgent appeals.
2. **Registration / tax-ID presence** — checks the page for charity registration numbers or tax identifiers that real charities display and fakes omit.
3. **Impersonation check** — compares the domain's registrant/name against known charities to catch look-alike names.
4. **Payment-pathway type** — classifies the requested payment method (gift card, crypto, wire, personal account vs. vetted processor).

---

## 3. Label Convention

The project uses the following convention throughout:

| Label | Meaning |
|-------|---------|
| `0` | Legitimate |
| `1` | Fraudulent |

> **Important:** the source PhiUSIIL dataset uses the *inverted* convention (`1 = legitimate`, `0 = phishing`). Labels were **remapped** during dataset construction so that the project consistently uses `1 = Fraudulent`. All features, evaluation, and reporting assume this remapped convention.

---

## 4. Dataset Strategy (phishing-vs-legitimate rationale)

**Decision:** train on a general phishing-versus-legitimate dataset rather than a donation-only one.

**Rationale:**

1. **No donation-specific dataset exists.** This gap is well documented; even recent academic work on donation-scam detection reports having to build such datasets from scratch. A donation-only collection would also be too small to train a reliable model.

2. **Fraudulent donation links are a sub-category of phishing.** They use the same techniques — newly registered domains, suspicious URL structures, urgency-driven language, and absence from trusted registries.

3. **A phishing detector generalises to donation fraud.** A model that learns the signals separating phishing from legitimate sites will, by extension, flag fraudulent donation links, since they exhibit the same signals.

4. **Donation relevance is preserved by design.** Donation- and charity-themed URLs are deliberately included on **both** the fraudulent and legitimate sides, so the model is exposed to the donation context and does not learn a superficial "charity-themed = safe" shortcut. The four novel features add explicit donation-domain intelligence on top of the general baseline.

**In short:** by teaching the model to recognise phishing in general — and adding donation-specific features on top — it inherits the ability to recognise fraudulent donation links specifically, while avoiding the data-scarcity problem a donation-only approach would face.

---

## Summary

This document fixes the four design decisions that guide the build: the **four detection modules**, the **12-feature set** (plus four novel donation features), the **`0`/`1` label convention**, and the **phishing-vs-legitimate dataset strategy**. Feature-engineering code follows directly from this plan.
