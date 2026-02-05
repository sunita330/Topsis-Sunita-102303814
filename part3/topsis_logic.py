import pandas as pd
import numpy as np
import os

def topsis(input_file, weights, impacts, output_file):

    df = pd.read_excel(input_file)

    if df.shape[1] < 3:
        raise ValueError("File must have 3 or more columns")

    data = df.iloc[:, 1:].astype(float)

    weights = list(map(float, weights.split(",")))
    impacts = impacts.split(",")

    if len(weights) != data.shape[1]:
        raise ValueError("Weights count mismatch")

    if len(impacts) != data.shape[1]:
        raise ValueError("Impacts count mismatch")

    for i in impacts:
        if i not in ['+', '-']:
            raise ValueError("Impacts must be + or -")

    norm = data / np.sqrt((data ** 2).sum())
    weighted = norm * weights

    ideal_best = []
    ideal_worst = []

    for i in range(len(impacts)):
        if impacts[i] == '+':
            ideal_best.append(weighted.iloc[:, i].max())
            ideal_worst.append(weighted.iloc[:, i].min())
        else:
            ideal_best.append(weighted.iloc[:, i].min())
            ideal_worst.append(weighted.iloc[:, i].max())

    ideal_best = np.array(ideal_best)
    ideal_worst = np.array(ideal_worst)

    d_best = np.sqrt(((weighted - ideal_best) ** 2).sum(axis=1))
    d_worst = np.sqrt(((weighted - ideal_worst) ** 2).sum(axis=1))

    score = d_worst / (d_best + d_worst)

    df["Topsis Score"] = score
    df["Rank"] = score.rank(ascending=False).astype(int)

    df.to_excel(output_file, index=False)
