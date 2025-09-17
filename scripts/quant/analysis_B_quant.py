#!/usr/bin/env python3
"""
Quant Option B — Friendly Baseline
- Load CSV from --data_url (or --data_path)
- Summary stats, top/bottom 10, correlation
- Save scatter-ready JSON (country, x, y)
- Print 1–2 key findings

Example:
  python scripts/quant/analysis_B_quant.py \
    --data_url https://.../thriving.csv \
    --x LifeSatisfaction2018 --y LifeExpectancy2018 --country_col Country
"""
import argparse, sys, json, os
import pandas as pd
import numpy as np

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--data_url', type=str, default=None)
    ap.add_argument('--data_path', type=str, default=None)
    ap.add_argument('--country_col', type=str, default='Country')
    ap.add_argument('--measures', nargs='*', default=None)
    ap.add_argument('--x', type=str, default=None)
    ap.add_argument('--y', type=str, default=None)
    ap.add_argument('--outdir', type=str, default='outputs')
    args = ap.parse_args()

    if not args.data_url and not args.data_path:
        print('[ERROR] Provide --data_url or --data_path'); sys.exit(1)

    df = pd.read_csv(args.data_url or args.data_path)

    if args.measures is None:
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        args.measures = numeric_cols[:3]
        print(f'[INFO] Auto-picked measures: {args.measures}')

    if args.x is None: args.x = args.measures[0]
    if args.y is None: args.y = args.measures[1] if len(args.measures) > 1 else args.measures[0]

    os.makedirs(args.outdir, exist_ok=True)

    # Summary stats
    print('\n[SUMMARY]\n', df[args.measures].describe().T)

    # Top/bottom 10 for X
    if args.country_col in df.columns and args.x in df.columns:
        top10 = df[[args.country_col, args.x]].dropna().nlargest(10, args.x)
        bottom10 = df[[args.country_col, args.x]].dropna().nsmallest(10, args.x)
        print(f"\n[TOP 10 by {args.x}]\n", top10.to_string(index=False))
        print(f"\n[BOTTOM 10 by {args.x}]\n", bottom10.to_string(index=False))

    # Correlation
    print('\n[CORRELATION]\n', df[args.measures].corr())

    # Scatter JSON
    if {args.country_col, args.x, args.y}.issubset(df.columns):
        records = df[[args.country_col, args.x, args.y]].dropna()
        out = [{"country": r[args.country_col], "x": float(r[args.x]), "y": float(r[args.y])}
               for _, r in records.iterrows()]
        outpath = os.path.join(args.outdir, 'quant_B_scatter.json')
        with open(outpath, 'w', encoding='utf-8') as f:
            json.dump(out, f, ensure_ascii=False, indent=2)
        print(f"\n[SAVED] {outpath}")

    if {args.x, args.y}.issubset(df.columns):
        corr_xy = df[[args.x, args.y]].corr().iloc[0,1]
        print(f"\n[KEY FINDING] {args.x} and {args.y} correlation ≈ {corr_xy:.2f}.")

if __name__ == '__main__':
    main()
