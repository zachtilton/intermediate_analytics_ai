#!/usr/bin/env python3
"""
Qual Option B — Frequency + Simple Sentiment (lexicon-based)
- Load CSV from --data_url/--data_path (doc_id, text)
- Tokenize, remove stopwords
- Top-N unigrams + bigrams
- Simple lexicon sentiment per doc
- Save word-frequency JSON + doc sentiment CSV

Example:
  python scripts/qual/analysis_B_qual.py --data_url https://.../corpus.csv --top_n 40
"""
import argparse, re, os, json, sys
import pandas as pd
from collections import Counter

STOPWORDS = {
    'a','an','the','and','or','but','if','then','else','of','to','in','on','for','with',
    'is','are','was','were','be','been','being','at','by','from','as','it','this','that',
    'these','those','there','here','we','you','they','he','she','them','his','her','their',
    'i','me','my','our','ours','your','yours','us'
}

SENTIMENT = {
    'good': 2, 'great': 3, 'excellent': 4, 'positive': 2, 'benefit': 2, 'improve': 2,
    'bad': -2, 'poor': -2, 'negative': -2, 'harm': -3, 'worse': -2, 'risk': -1
}

TOKEN_RE = re.compile(r"[a-zA-Z]{2,}")

def tokenize(text):
    toks = [t.lower() for t in TOKEN_RE.findall(text or '') if t.lower() not in STOPWORDS]
    return toks

def bigrams(tokens):
    return [f"{tokens[i]} {tokens[i+1]}" for i in range(len(tokens)-1)]

def doc_sentiment(tokens):
    return sum(SENTIMENT.get(t, 0) for t in tokens)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--data_url', type=str, default=None)
    ap.add_argument('--data_path', type=str, default=None)
    ap.add_argument('--top_n', type=int, default=30)
    ap.add_argument('--outdir', type=str, default='outputs')
    args = ap.parse_args()

    if not args.data_url and not args.data_path:
        print('[ERROR] Provide --data_url or --data_path'); sys.exit(1)

    df = pd.read_csv(args.data_url or args.data_path)
    if not {'doc_id','text'}.issubset(df.columns):
        print('[ERROR] CSV must have columns: doc_id, text'); sys.exit(1)

    os.makedirs(args.outdir, exist_ok=True)

    all_uni = Counter(); all_bi = Counter(); sentiments = []
    for _, row in df.iterrows():
        toks = tokenize(str(row['text']))
        all_uni.update(toks)
        all_bi.update(bigrams(toks))
        sentiments.append({'doc_id': row['doc_id'], 'sentiment': doc_sentiment(toks)})

    top_uni = all_uni.most_common(args.top_n)
    top_bi = all_bi.most_common(args.top_n)

    freq_records = [{'term': t, 'freq': int(c)} for t, c in top_uni + top_bi]

    out_freq = os.path.join(args.outdir, 'qual_B_words.json')
    with open(out_freq, 'w', encoding='utf-8') as f:
        json.dump(freq_records, f, ensure_ascii=False, indent=2)

    out_sent = os.path.join(args.outdir, 'qual_B_doc_sentiment.csv')
    pd.DataFrame(sentiments).to_csv(out_sent, index=False)

    print(f"[SAVED] {out_freq}\n[SAVED] {out_sent}")
    print("\n[KEY FINDING] Top terms and bigrams highlight dominant themes; per-doc sentiment provides a quick polarity scan.")

if __name__ == '__main__':
    main()
