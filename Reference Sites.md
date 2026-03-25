##  Reference Websites

The following tools are widely used in cybersecurity to detect fraudulent or suspicious URLs:

---

### 1. Google Safe Browsing Transparency Report
- 🔗 https://transparencyreport.google.com/safe-browsing/search  
- Checks if a URL is flagged by Google for phishing, malware, or scams  
- Useful as a **first-level filter** for suspicious donation links  

---

### 2. VirusTotal
- 🔗 https://www.virustotal.com  
- Scans URLs using **70+ antivirus engines**  
- Provides reputation scores, domain details, and community feedback  
- Ideal for **multi-engine validation**  

---

### 3. ScamAdviser
- 🔗 https://www.scamadviser.com  
- Generates a **trust score** based on:
  - Domain age  
  - Server location  
  - Owner information  
- Useful for **risk scoring and credibility analysis**  

---

### 4. PhishTank
- 🔗 https://www.phishtank.com  
- Community-driven database of verified phishing URLs  
- Suitable for implementing a **blacklist-based detection system**  

---

### 5. URLVoid
- 🔗 https://www.urlvoid.com  
- Aggregates multiple blacklist engines  
- Provides quick insight into a website’s reputation  

---

### 6. WHOIS Lookup (ICANN)
- 🔗 https://lookup.icann.org  
- Provides domain registration details:
  - Creation date  
  - Registrar  
- Useful for **domain age analysis** (new domains are more likely to be suspicious)  

---

### 7. CheckPhish
- 🔗 https://checkphish.ai  
- AI-powered phishing detection tool  
- Useful for analyzing suspicious donation pages and identifying phishing patterns  

---

## Relevance to This Project

This project adopts a multi-layered detection approach inspired by real-world cybersecurity tools:

| Detection Method        | Related Tools           |
|------------------------|------------------------|
| Blacklist Checking     | PhishTank, URLVoid     |
| Link Structure Analysis| VirusTotal, ScamAdviser|
| Domain Age Analysis    | ICANN WHOIS            |
| Content/Text Analysis  | CheckPhish             |

---

##  Note

This project integrates multiple detection strategies inspired by industry tools such as VirusTotal, Google Safe Browsing, and ScamAdviser to identify fraudulent donation links more effectively.
