#!/usr/bin/env python3
"""
Quant Option C — Advanced (Regression | Clustering | PCA)
Produces JSONs for dashboards and prints interpretations.

Examples:
  python scripts/quant/analysis_C_quant.py --method regression \
    --target LifeSatisfaction2018 \
    --features LifeExpectancy2018 GDPPerCapita2018 \
    --data_url https://.../thriving.csv --country_col Country

  python scripts/quant/analysis_C_quant.py --method clustering \
    --features LifeSatisfaction2018 LifeExpectancy2018 --k 4 \
    --data_url https://.../thriving.csv --country_col Country

  python scripts/quant/analysis_C_quant.py --method pca \
    --features LifeSatisfaction2018 LifeExpectancy2018 GDPPerCapita2018 \
    --n_components 2 --data_url https://.../thriving.csv --country_col Country
"""
import argparse, sys, os, json
import pandas as pd
import numpy as np

def try_import_sklearn():
    try:
        from sklearn.linear_model import LinearRegression
        from sklearn.cluster import KMeans
        from sklearn.decomposition import PCA
        return LinearRegression, KMeans, PCA
    except Exception:
        print('[ERROR] scikit-learn required. In Colab: !pip install scikit-learn')
        raise

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--data_url', type=str, default=None)
    ap.add_argument('--data_path', type=str, default=None)
    ap.add_argument('--country_col', type=str, default='Country')
    ap.add_argument('--method', choices=['regression','clustering','pca'], required=True)
    ap.add_argument('--features', nargs='+', required=True)
    ap.add_argument('--target', type=str, default=None)
    ap.add_argument('--k', type=int, default=4)
    ap.add_argument('--n_components', type=int, default=2)
    ap.add_argument('--outdir', type=str, default='outputs')
    args = ap.parse_args()

    if not args.data_url and not args.data_path:
        print('[ERROR] Provide --data_url or --data_path'); sys.exit(1)

    df = pd.read_csv(args.data_url or args.data_path)
    os.makedirs(args.outdir, exist_ok=True)

    LinearRegression, KMeans, PCA = try_import_sklearn()

    if args.method == 'regression':
        if not args.target:
            print('[ERROR] --target required for regression'); sys.exit(1)
        use = df.dropna(subset=[*args.features, args.target])
        X = use[args.features].values
        y = use[args.target].values
        m = LinearRegression().fit(X, y)
        coefs = dict(zip(args.features, m.coef_.tolist()))
        intercept = float(m.intercept_)
        r2 = float(m.score(X, y))
        print('\n[REGRESSION]\nIntercept:', intercept, '\nCoefficients:', coefs, '\nR^2:', r2)

        # Simple scatter (first two dims)
        cols = [args.features[0], args.features[1] if len(args.features)>1 else args.target]
        usable = df.dropna(subset=[args.country_col, *cols])
        scatter = [{"country": r[args.country_col], "x": float(r[cols[0]]), "y": float(r[cols[1]])}
                   for _, r in usable.iterrows()]
        with open(os.path.join(args.outdir, 'quant_C_scatter.json'), 'w', encoding='utf-8') as f:
            json.dump(scatter, f, ensure_ascii=False, indent=2)

        best = max(coefs, key=lambda k: abs(coefs[k])) if coefs else None
        print(f"\n[INTERPRETATION] R^2 ≈ {r2:.2f}. Strongest predictor appears to be '{best}'.")

    elif args.method == 'clustering':
        usable = df.dropna(subset=[*args.features, args.country_col]).copy()
        X = usable[args.features].values
        km = KMeans(n_clusters=args.k, n_init=10, random_state=42).fit(X)
        usable['cluster'] = km.labels_

        f0, f1 = args.features[0], args.features[1] if len(args.features)>1 else args.features[0]
        scatter = [{
            'country': r[args.country_col],
            'x': float(r[f0]),
            'y': float(r[f1]),
            'group': int(r['cluster'])
        } for _, r in usable.iterrows()]
        with open(os.path.join(args.outdir, 'quant_C_scatter.json'), 'w', encoding='utf-8') as f:
            json.dump(scatter, f, ensure_ascii=False, indent=2)

        hist_vals = usable[f0].dropna().values.tolist()
        with open(os.path.join(args.outdir, 'quant_C_hist.json'), 'w', encoding='utf-8') as f:
            json.dump(hist_vals, f, ensure_ascii=False, indent=2)

        print(f"\n[INTERPRETATION] Formed {args.k} clusters. Explore differences by cluster in the dashboard.")

    elif args.method == 'pca':
        usable = df.dropna(subset=[*args.features, args.country_col]).copy()
        X = usable[args.features].values
        pca = PCA(n_components=args.n_components, random_state=42).fit(X)
        comps = pca.components_.tolist()
        expl = pca.explained_variance_ratio_.tolist()

        loadings = [{'component': i+1,
                     'loadings': dict(zip(args.features, [float(v) for v in comp]))}
                    for i, comp in enumerate(comps)]

        X_pca = pca.transform(X)
        scatter = [{
            'country': usable.iloc[i][args.country_col],
            'x': float(X_pca[i,0]),
            'y': float(X_pca[i,1] if X_pca.shape[1] > 1 else 0.0),
            'group': 0
        } for i in range(len(usable))]
        with open(os.path.join(args.outdir, 'quant_C_scatter.json'), 'w', encoding='utf-8') as f:
            json.dump(scatter, f, ensure_ascii=False, indent=2)
        with open(os.path.join(args.outdir, 'quant_C_pca_loadings.json'), 'w', encoding='utf-8') as f:
            json.dump(loadings, f, ensure_ascii=False, indent=2)

        print(f"\n[INTERPRETATION] PCA explained variance ≈ {[round(v,2) for v in expl]}. Use loadings to interpret components.")

if __name__ == '__main__':
    main()
