# Vibe Coding Activity — Instructions & Prompt Templates

This guide is the one-stop reference for running the vibe-coding lab. It includes the session plan, ready-to-copy prompt templates (A–C) for **quant** and **qual**, exact **run commands**, expected **outputs**, and how to load results into the **HTML visualizations**.

---

## 0) Repo at a Glance

- `INSTRUCTIONS.md` ← **(this file)**
- `scripts/quant/analysis_B_quant.py`  (friendly)
- `scripts/quant/analysis_C_quant.py`  (advanced)
- `scripts/qual/analysis_B_qual.py`    (friendly)
- `scripts/qual/analysis_C_qual.py`    (advanced)
- `viz/quant_B.html`   (scatter; upload JSON/CSV)
- `viz/quant_C.html`   (linked scatter+hist; upload JSONs)
- `viz/qual_B.html`    (word frequency bar chart; upload JSON/CSV)
- `viz/qual_C.html`    (topic browser; upload JSON)

---

## 1) Session Flow (95 minutes total)

- **Intro (20 min)** — 3 slides + fast demo (synthetic data ➜ HTML viz) + instructions.
- **Vibe Coding Activity (30 min)** — Groups of 4–5:
  - ≥2 go **Quant**, ≥2 go **Qual**.
  - Pick **A** (meta + code), **B** (friendly), or **C** (advanced).
- **Break (15 min)** — Let heavier runs finish; compare notes.
- **Viz (20 min)** — Use the HTML templates to visualize results.
- **Debrief (10 min)** — What worked? What surprised you? What’s next?

**Time expectations (set these up front)**
- Option **A**: may not fully execute before break (that’s OK).
- Option **B**: target completion in ~25 minutes.
- Option **C**: target completion in ~30 minutes.

**Group pattern**
- 2 × Quant (ideally one B, one C)
- 2 × Qual (ideally one B, one C)
- If a 5th person: flex or pair on A.

---

## 2) Data Requirements (you provide the files/URLs)

- **Quant CSV**: `Country` + numeric measures (e.g., `LifeSatisfaction2018`, `LifeExpectancy2018`, `GDPPerCapita2018`, …).
- **Qual CSV**: `doc_id`, `text`.

> All scripts accept **either** `--data_url https://.../file.csv` **or** `--data_path local.csv`.

---

## 3) Quickstart: Run Commands (copy/paste)

> Create an `outputs/` folder automatically by running any script; outputs are written there.

### 3.1 Quant — Option B (Friendly)
```bash
python scripts/quant/analysis_B_quant.py   --data_url https://YOUR_URL/thriving.csv   --x LifeSatisfaction2018   --y LifeExpectancy2018   --country_col Country
```
**Produces:** `outputs/quant_B_scatter.json` (records: `{country, x, y}`)

### 3.2 Quant — Option C (Advanced)

**Regression**
```bash
python scripts/quant/analysis_C_quant.py   --method regression   --target LifeSatisfaction2018   --features LifeExpectancy2018 GDPPerCapita2018   --data_url https://YOUR_URL/thriving.csv   --country_col Country
```

**Clustering**
```bash
python scripts/quant/analysis_C_quant.py   --method clustering   --features LifeSatisfaction2018 LifeExpectancy2018   --k 4   --data_url https://YOUR_URL/thriving.csv   --country_col Country
```

**PCA**
```bash
python scripts/quant/analysis_C_quant.py   --method pca   --features LifeSatisfaction2018 LifeExpectancy2018 GDPPerCapita2018   --n_components 2   --data_url https://YOUR_URL/thriving.csv   --country_col Country
```

**Produces (varies by method):**
- `outputs/quant_C_scatter.json` (records: `{country, x, y, group?}`)
- `outputs/quant_C_hist.json` (array of numbers; clustering only)
- `outputs/quant_C_pca_loadings.json` (PCA only)

---

### 3.3 Qual — Option B (Friendly)
```bash
python scripts/qual/analysis_B_qual.py   --data_url https://YOUR_URL/corpus.csv   --top_n 40
```
**Produces:**
- `outputs/qual_B_words.json` (records: `{term, freq}`)
- `outputs/qual_B_doc_sentiment.csv`

### 3.4 Qual — Option C (Advanced: LDA Topics)
```bash
python scripts/qual/analysis_C_qual.py   --data_url https://YOUR_URL/corpus.csv   --n_topics 6
```
**Produces:**
- `outputs/qual_C_topics.json`
  ```json
  {
    "topics": [ {"topic":0,"top_terms":["term1","term2",...]}, ... ],
    "samples": [ {"topic":0,"doc_ids":[...]}, ... ]
  }
  ```

---

## 4) Load Results into the Visualizations

> Open these files **locally** in your browser. Use the built-in **Upload** buttons—no server needed.

- **Quant B** (scatter): `viz/quant_B.html`  
  Upload: `outputs/quant_B_scatter.json` **or** a CSV with `country,x,y`.

- **Quant C** (linked views): `viz/quant_C.html`  
  Upload: `outputs/quant_C_scatter.json` (required)  
  Optional: `outputs/quant_C_hist.json` (for the histogram panel).

- **Qual B** (word frequencies): `viz/qual_B.html`  
  Upload: `outputs/qual_B_words.json` **or** a CSV with `term,freq`.

- **Qual C** (topic browser): `viz/qual_C.html`  
  Upload: `outputs/qual_C_topics.json`.

---

## 5) Prompt Templates (copy/paste)

### 5.1 Quantitative (A–C)

**Option A — Meta + Vibe Code**
```text
# Part 1 — Meta-dialogue (≈5 min)
Given my construct [X], measures [Y1, Y2, ...], question [Z], and analysis type [W],
what analytical procedure best reveals patterns? Suggest 2–3 concrete steps and the exact code.

# Part 2 — Vibe code (≈25 min)
Generate Python code to implement the recommended procedure on CSV at [DATA_URL].
Assume columns for Country and the numeric measures listed. Use pandas/numpy/scikit-learn only.
Return runnable code blocks with clear placeholders for variable names.
```

**Option B — Friendly Baseline**
```text
I want to analyze thriving using:
- Measures: [pick 2–3 from list]
- Country focus: [ALL or REGION]

Generate Python code that:
1) Loads CSV from [DATA_URL]
2) Calculates summary stats for my measures
3) Lists top/bottom 10 countries for a chosen measure
4) Builds a correlation matrix
5) Saves JSON for a scatter plot with fields: country, x, y
6) Prints 1–2 key findings in plain English
```

**Option C — Advanced (Regression / Clustering / PCA)**
```text
Construct: [YOUR CONSTRUCT]
Measures: [YOUR 3–4 MEASURES]
Question: [YOUR SPECIFIC QUESTION]
Method: [regression | clustering | pca]

Generate Python code that:
- Loads data from [DATA_URL]
- Runs [Method] with interpretable output
- Saves dashboard-ready JSON(s)
- Prints a concise interpretation of results
```

---

### 5.2 Qualitative / NLP (A–C)

**Option A — Meta + Vibe Code**
```text
# Part 1 — Meta-dialogue
Given my construct [X], corpus type (e.g., project descriptions, interviews), and question [Z],
which 1–2 methods (word frequency, sentiment, topics) should I run? Provide steps + exact code.

# Part 2 — Vibe code
Generate Python (pandas + scikit-learn only) for CSV at [DATA_URL] with columns doc_id,text.
Return runnable code blocks with clear placeholders.
```

**Option B — Frequency + Simple Sentiment**
```text
I want code that:
1) Loads CSV from [DATA_URL] (doc_id, text)
2) Cleans/tokenizes; removes stopwords
3) Gets top-N unigrams and bigrams across the corpus
4) Computes a simple lexicon-based sentiment per document
5) Saves a word-frequency JSON for a bar-chart viz
6) Prints 1–2 concise findings
```

**Option C — Topic Modeling (LDA)**
```text
I want Python code that:
- Loads CSV from [DATA_URL] (doc_id, text)
- Vectorizes with CountVectorizer (1–2 grams)
- Runs LDA with n_topics = [X]
- Outputs top terms per topic and sample doc_ids
- Saves topics JSON for a topic browser
- Prints a brief interpretation
```

---

### 5.3 Visualization Prompt Starters (optional, if generating viz code on the fly)
```text
My analysis found: [1–2 KEY FINDINGS]
My data structure: [describe fields you have: e.g., country, x, y]

Generate HTML/JavaScript for an interactive visualization that clearly shows this finding.
Include:
- Title and labels
- Interactivity (hover/click)
- Basic layout/styling
Option B: bar or scatter
Option C: small dashboard (2+ linked views)
```

---

## 6) Troubleshooting Quick Guide

- **Error** → Copy and paste error message into AI prompt box with a plea like "HELP!"
- **Visual Output Error** → Screenshot the relevant section with a description for remediation.
- **Import error** → Use basic Python libs; for Option C run `!pip install scikit-learn` in Colab.  
- **File not found** → Double-check `--data_url` or use `--data_path`.  
- **Code too long** → Run in chunks; print shapes/heads often.  
- **Timeout** → Reduce features/topics; sample rows.  
- **No output** → Check the `outputs/` folder; add `print()` statements.  
- **JSON upload fails** → Open the JSON to confirm structure matches the viz expectations.

---

## 7) Success Metrics

- **Option A**: Got through meta-dialogue and started code.  
- **Option B**: Working code + initial results.  
- **Option C**: Completed analysis and can interpret outputs.

---

