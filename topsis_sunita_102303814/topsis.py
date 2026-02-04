import sys
import os
import pandas as pd
import numpy as np


def topsis(input_file, weights, impacts, output_file):

    # -------- Check input file ----------
    if not os.path.exists(input_file):
        raise FileNotFoundError("Input file not found")

    # -------- Read file ----------
    if input_file.endswith(".csv"):
        df = pd.read_csv(input_file)
    else:
        df = pd.read_excel(input_file)

    # -------- Minimum columns ----------
    if df.shape[1] < 3:
        raise ValueError("Input file must contain at least 3 columns")

    data = df.iloc[:, 1:]

    # -------- Numeric check ----------
    try:
        data = data.astype(float)
    except:
        raise ValueError("Criteria columns must contain numeric values only")

    # -------- Weights & impacts ----------
    weights = weights.split(",")
    impacts = impacts.split(",")

    if len(weights) != data.shape[1]:
        raise ValueError("Number of weights must match number of criteria")

    if len(impacts) != data.shape[1]:
        raise ValueError("Number of impacts must match number of criteria")

    weights = np.array(list(map(float, weights)))

    for i in impacts:
        if i not in ["+", "-"]:
            raise ValueError("Impacts must be either + or -")

    # -------- Step 1: Normalization ----------
    norm = data / np.sqrt((data ** 2).sum())

    # -------- Step 2: Weighted matrix ----------
    weighted = norm * weights

    # -------- Step 3: Ideal best & worst ----------
    ideal_best = []
    ideal_worst = []

    for i in range(len(impacts)):
        if impacts[i] == "+":
            ideal_best.append(weighted.iloc[:, i].max())
            ideal_worst.append(weighted.iloc[:, i].min())
        else:
            ideal_best.append(weighted.iloc[:, i].min())
            ideal_worst.append(weighted.iloc[:, i].max())

    ideal_best = np.array(ideal_best)
    ideal_worst = np.array(ideal_worst)

    # -------- Step 4: Distances ----------
    d_best = np.sqrt(((weighted - ideal_best) ** 2).sum(axis=1))
    d_worst = np.sqrt(((weighted - ideal_worst) ** 2).sum(axis=1))

    # -------- Step 5: TOPSIS score ----------
    score = d_worst / (d_best + d_worst)

    df["Topsis Score"] = score
    df["Rank"] = score.rank(ascending=False).astype(int)

    # -------- Save output ----------
    if output_file.endswith(".csv"):
        df.to_csv(output_file, index=False)
    else:
        df.to_excel(output_file, index=False)

    print("TOPSIS calculation completed successfully")
    print("Output saved to:", output_file)


def main():
    if len(sys.argv) != 5:
        print("Usage:")
        print("python topsis.py <inputfile> <weights> <impacts> <outputfile>")
        sys.exit(1)

    topsis(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])


if __name__ == "__main__":
    main()
