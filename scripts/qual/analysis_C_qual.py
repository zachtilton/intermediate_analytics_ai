#!/usr/bin/env python3
"""
Qual Option C — LDA Topic Modeling (scikit-learn)
- Load CSV from --data_url/--data_path (doc_id, text)
- CountVectorizer (1–2 grams)
- LDA with --n_topics
- Output topics JSON for viz

Example:
  python scripts/qual/analysis_C_qual.py --data_url https://.../corpus.csv --n_topics 6
"""
import argparse, sys, os, json
import pandas as pd

def try_import_sklearn():
    try:
        from sklearn.feature_extraction.text import CountVectorizer
        from sklearn.decomposition import LatentDirichletAllocation
        return CountVectorizer, LatentDirichletAllocation
    except Exception:
        print('[ERROR] scikit-learn required. In Colab: !pip install scikit-learn')
        raise

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--data_url', type=str, default=None)
    ap.add_argument('--data_path', type=str, default=None)
    ap.add_argument('--n_topics', type=int, default=6)
    ap.add_argument('--max_features', type=int, default=5000)
    ap.add_argument('--outdir', type=str, default='outputs')
    args = ap.parse_args()

    if not args.data_url and not args.data_path:
        print('[ERROR] Provide --data_url or --data_path'); sys.exit(1)

    df = pd.read_csv(args.data_url or args.data_path)
    if not {'doc_id','text'}.issubset(df.columns):
        print('[ERROR] CSV must have columns: doc_id, text'); sys.exit(1)

    os.makedirs(args.outdir, exist_ok=True)

    CountVectorizer, LatentDirichletAllocation = try_import_sklearn()

    vect = CountVectorizer(stop_words='english', ngram_range=(1,2), max_features=args.max_features)
    X = vect.fit_transform(df['text'].astype(str))
    lda = LatentDirichletAllocation(n_components=args.n_topics, random_state=42, learning_method='batch')
    W = lda.fit_transform(X)  # doc-topic
    H = lda.components_       # topic-term

    vocab = pd.Series(vect.get_feature_names_out())
    topn = 10
    topics = []
    for k in range(args.n_topics):
        top_idx = H[k].argsort()[-topn:][::-1]
        terms = vocab.iloc[top_idx].tolist()
        topics.append({'topic': int(k), 'top_terms': terms})

    doc_topics = W.argmax(axis=1)
    samples = []
    for k in range(args.n_topics):
        doc_ids = df.index[doc_topics == k].tolist()[:5]
        def _coerce(v):
            try: return int(v)
            except Exception: return str(v)
        samples.append({'topic': int(k), 'doc_ids': [_coerce(df.loc[i, 'doc_id']) for i in doc_ids]})

    out = {'topics': topics, 'samples': samples}
    outpath = os.path.join(args.outdir, 'qual_C_topics.json')
    with open(outpath, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print(f"[SAVED] {outpath}")
    print("[INTERPRETATION] Use top terms + sample doc_ids to label topics and tie back to your evaluation questions.")

if __name__ == '__main__':
    main()
