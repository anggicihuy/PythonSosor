# ============================================================
# 1. IMPORT LIBRARIES
# ============================================================

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, classification_report

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler

import xgboost as xgb

# ============================================================
# 2. LOAD DATA
# ============================================================

df = pd.read_csv("transactions.csv")

# Drop kolom ID yang tidak dipakai
df = df.drop(["nameOrig", "nameDest"], axis=1)

X = df.drop("isFraud", axis=1)
y = df["isFraud"]

# ============================================================
# 3. ONE-HOT ENCODING untuk kolom 'type'
# ============================================================

encoder = ColumnTransformer(
    transformers=[("type", OneHotEncoder(handle_unknown="ignore"), ["type"])],
    remainder="passthrough"
)

X = encoder.fit_transform(X)

# ============================================================
# 4. TRAIN-TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# ============================================================
# 5. DEFINISI MODEL
# ============================================================

models = {
    "Logistic Regression": LogisticRegression(max_iter=2000, class_weight="balanced"),
    "Random Forest": RandomForestClassifier(n_estimators=200, class_weight="balanced", random_state=42),
    "XGBoost": xgb.XGBClassifier(
        eval_metric='logloss',
        scale_pos_weight=(y_train.value_counts()[0] / y_train.value_counts()[1]),
        use_label_encoder=False
    )
}

# ============================================================
# 6. FUNGSI EVALUASI MODEL
# ============================================================

def evaluate_model(model, X_test, y_test):
    pred = model.predict(X_test)
    prob = model.predict_proba(X_test)[:, 1]

    return {
        "Accuracy": accuracy_score(y_test, pred),
        "Precision": precision_score(y_test, pred),
        "Recall": recall_score(y_test, pred),
        "F1-score": f1_score(y_test, pred),
        "ROC-AUC": roc_auc_score(y_test, prob)
    }

# ============================================================
# 7. HASIL EVALUASI UNTUK SEMUA METODE BALANCING
# ============================================================

results = []

# ================================
# A. CLASS WEIGHTING
# ================================
print("\n================ CLASS WEIGHTING ================")

for name, model in models.items():
    model.fit(X_train, y_train)
    scores = evaluate_model(model, X_test, y_test)
    scores["Model"] = name
    scores["Balancing"] = "Class Weighting"
    results.append(scores)

    print(f"\nModel: {name}")
    print(classification_report(y_test, model.predict(X_test)))


# ================================
# B. SMOTE OVERSAMPLING
# ================================
print("\n====================== SMOTE ======================")

sm = SMOTE(random_state=42)
X_smote, y_smote = sm.fit_resample(X_train, y_train)

for name, model in models.items():
    model.fit(X_smote, y_smote)
    scores = evaluate_model(model, X_test, y_test)
    scores["Model"] = name
    scores["Balancing"] = "SMOTE"
    results.append(scores)

    print(f"\nModel: {name} (SMOTE)")
    print(classification_report(y_test, model.predict(X_test)))


# ================================
# C. UNDERSAMPLING
# ================================
print("\n================== UNDERSAMPLING ==================")

under = RandomUnderSampler(random_state=42)
X_under, y_under = under.fit_resample(X_train, y_train)

for name, model in models.items():
    model.fit(X_under, y_under)
    scores = evaluate_model(model, X_test, y_test)
    scores["Model"] = name
    scores["Balancing"] = "Undersampling"
    results.append(scores)

    print(f"\nModel: {name} (Undersampling)")
    print(classification_report(y_test, model.predict(X_test)))


# ============================================================
# 8. HASIL AKHIR DALAM TABEL
# ============================================================

df_results = pd.DataFrame(results)
print("\n\n=========== HASIL PERBANDINGAN FULL ===========\n")
print(df_results)
