import re
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

# 1. Load and validate the literature matrix
INPUT_FILE = Path("literature_matrix.csv")
OUTPUT_FILE = Path("coding_summary.png")

if not INPUT_FILE.is_file():
    raise FileNotFoundError(
        f"Cannot find {INPUT_FILE.resolve()}\n"
        "Place literature_matrix.csv in the working directory "
        "or update INPUT_FILE."
    )

df = pd.read_csv(INPUT_FILE)

print("CSV file path:", INPUT_FILE.resolve())
print("CSV file size:", INPUT_FILE.stat().st_size, "bytes")
print("DataFrame shape:", df.shape)
print("Column names:", df.columns.tolist())
print("First five rows:")
print(df.head())

if df.empty:
    raise ValueError("The literature matrix contains no records.")


REQUIRED_COLUMNS = {"title", "year", "abstract", "source_type"}
missing_columns = REQUIRED_COLUMNS - set(df.columns)

if missing_columns:
    raise ValueError(
        f"CSV is missing required columns: {sorted(missing_columns)}\n"
        f"Available columns: {list(df.columns)}"
    )

if df.empty:
    raise ValueError("The literature matrix contains no records.")

# Normalize text fields and clean publication years.
df["abstract"] = df["abstract"].fillna("").astype(str).str.strip()

original_years = df["year"].copy()
df["year"] = pd.to_numeric(df["year"], errors="coerce")

invalid_years = int(df["year"].isna().sum())
if invalid_years:
    print(f"Warning: {invalid_years} records have missing or invalid years.")

# 2. Keyword dictionaries
CODEBOOK = {
    "activity": {
        "UNIT_GEN": r"unit test|test generation",
        "API_GEN": r"\bapi\b|openapi|swagger",
        "UI_E2E": r"end-to-end|\be2e\b|gui|web test",
        "BUG_REPRO": r"bug report|reproduc",
        "MAINTENANCE": r"self-heal|test repair|flaky|locator",
    },
    "technique": {
        "RULE_BASED": r"rule-based|pattern matching",
        "TRANSFORMER": r"transformer|bert",
        "LLM_PROMPT": r"large language model|\bllm\b|\bgpt\b|prompt",
        "LLM_AGENT": r"agent|tool use|model context protocol",
    },
    "barrier": {
        "HALLUCINATION": r"hallucinat|incorrect assertion",
        "PRIVACY": r"privacy|confidential|data leak",
        "EVALUATION": r"benchmark|data contamination|threat to validity",
    },
}

# Compile patterns once instead of compiling them for every abstract.
COMPILED_CODEBOOK = {
    dimension: {
        code: re.compile(pattern, flags=re.IGNORECASE)
        for code, pattern in patterns.items()
    }
    for dimension, patterns in CODEBOOK.items()
}


# 3. Assign multiple codes to each abstract
def assign_codes(text, patterns):
    text = str(text)
    return [code for code, regex in patterns.items() if regex.search(text)]


for dimension, patterns in COMPILED_CODEBOOK.items():
    df[dimension] = df["abstract"].apply(lambda text: assign_codes(text, patterns))


# 4. Calculate code frequencies safely
def code_frequency(column):
    return df[column].explode().dropna().value_counts().sort_values(ascending=False)


activity_freq = code_frequency("activity")
technique_freq = code_frequency("technique")
barrier_freq = code_frequency("barrier")

print(f"Total records processed: {len(df)}")
print(f"Records with empty abstracts: {(df['abstract'] == '').sum()}")

print("\nActivity frequencies:")
print(activity_freq if not activity_freq.empty else "No matches found.")

print("\nTechnique frequencies:")
print(technique_freq if not technique_freq.empty else "No matches found.")

print("\nBarrier frequencies:")
print(barrier_freq if not barrier_freq.empty else "No matches found.")


# 5. Publication trend by valid year
valid_years = df.dropna(subset=["year"]).copy()

if not valid_years.empty:
    # Group by integer year, avoiding separate groups for 2024 and 2024.0.
    valid_years["year"] = valid_years["year"].astype(int)
    trend = valid_years.groupby("year").size().sort_index()
else:
    trend = pd.Series(dtype="int64")


# 6. Visualize the results
fig, axes = plt.subplots(1, 3, figsize=(16, 5))

if activity_freq.empty:
    axes[0].text(0.5, 0.5, "No activity matches", ha="center", va="center")
else:
    activity_freq.plot.bar(ax=axes[0])

axes[0].set_title("Test Activities Studied")
axes[0].set_ylabel("Number of abstracts")

if barrier_freq.empty:
    axes[1].text(0.5, 0.5, "No barrier matches", ha="center", va="center")
else:
    barrier_freq.plot.bar(ax=axes[1])

axes[1].set_title("Reported Barriers")
axes[1].set_ylabel("Number of abstracts")

if trend.empty:
    axes[2].text(0.5, 0.5, "No valid publication years", ha="center", va="center")
else:
    trend.plot(ax=axes[2], marker="o")
    axes[2].set_xticks(trend.index)
    axes[2].tick_params(axis="x", rotation=45)

axes[2].set_title("Sources per Year")
axes[2].set_ylabel("Number of sources")

plt.tight_layout()
plt.savefig(OUTPUT_FILE, dpi=200, bbox_inches="tight")
plt.close(fig)

# 7. Save the coded matrix for auditing and further analysis
df.to_csv("coded_literature_matrix.csv", index=False)

print(f"\nChart saved to: {OUTPUT_FILE.resolve()}")
print(f"Coded matrix saved to: {Path('coded_literature_matrix.csv').resolve()}")
