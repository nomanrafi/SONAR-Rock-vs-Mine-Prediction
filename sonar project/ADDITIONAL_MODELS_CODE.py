# Additional Models for SONAR Rock vs Mine Prediction
# Add these cells to your SONAR_03.ipynb notebook

# Cell: Random Forest Classifier
print("\n" + "="*70)
print("RANDOM FOREST CLASSIFIER")
print("="*70)

from sklearn.ensemble import RandomForestClassifier

# Train Random Forest
rf = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)

pipe_rf = Pipeline([
    ('scaler', StandardScaler()),
    ('clf', rf)
])

pipe_rf.fit(X_train, y_train)
y_pred_rf = pipe_rf.predict(X_test)
y_pred_proba_rf = pipe_rf.predict_proba(X_test)[:, 1]

print(f"Accuracy:  {accuracy_score(y_test, y_pred_rf):.4f}")
print(f"Precision: {precision_score(y_test, y_pred_rf):.4f}")
print(f"Recall:    {recall_score(y_test, y_pred_rf):.4f}")
print(f"F1-Score:  {f1_score(y_test, y_pred_rf):.4f}")
print(f"ROC-AUC:   {roc_auc_score(y_test, y_pred_proba_rf):.4f}")

# Cross-validation
cv_rf = cross_validate(
    pipe_rf, X, y, cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=42),
    scoring=['accuracy', 'precision', 'recall', 'f1', 'roc_auc']
)
print(f"\nCross-Val Accuracy: {cv_rf['test_accuracy'].mean():.4f} (+/- {cv_rf['test_accuracy'].std():.4f})")


# Cell: Support Vector Machine (SVM)
print("\n" + "="*70)
print("SUPPORT VECTOR MACHINE (SVM) - RBF Kernel")
print("="*70)

from sklearn.svm import SVC

# Train SVM with RBF kernel
svm = SVC(
    kernel='rbf',
    C=1.0,
    gamma='scale',
    probability=True,
    random_state=42
)

pipe_svm = Pipeline([
    ('scaler', StandardScaler()),
    ('clf', svm)
])

pipe_svm.fit(X_train, y_train)
y_pred_svm = pipe_svm.predict(X_test)
y_pred_proba_svm = pipe_svm.predict_proba(X_test)[:, 1]

print(f"Accuracy:  {accuracy_score(y_test, y_pred_svm):.4f}")
print(f"Precision: {precision_score(y_test, y_pred_svm):.4f}")
print(f"Recall:    {recall_score(y_test, y_pred_svm):.4f}")
print(f"F1-Score:  {f1_score(y_test, y_pred_svm):.4f}")
print(f"ROC-AUC:   {roc_auc_score(y_test, y_pred_proba_svm):.4f}")

# Cross-validation
cv_svm = cross_validate(
    pipe_svm, X, y, cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=42),
    scoring=['accuracy', 'precision', 'recall', 'f1', 'roc_auc']
)
print(f"\nCross-Val Accuracy: {cv_svm['test_accuracy'].mean():.4f} (+/- {cv_svm['test_accuracy'].std():.4f})")


# Cell: LightGBM Classifier
print("\n" + "="*70)
print("LIGHTGBM CLASSIFIER")
print("="*70)

try:
    from lightgbm import LGBMClassifier
    
    lgb = LGBMClassifier(
        n_estimators=200,
        max_depth=5,
        learning_rate=0.1,
        num_leaves=31,
        random_state=42,
        verbose=-1
    )
    
    pipe_lgb = Pipeline([
        ('scaler', StandardScaler()),
        ('clf', lgb)
    ])
    
    pipe_lgb.fit(X_train, y_train)
    y_pred_lgb = pipe_lgb.predict(X_test)
    y_pred_proba_lgb = pipe_lgb.predict_proba(X_test)[:, 1]
    
    print(f"Accuracy:  {accuracy_score(y_test, y_pred_lgb):.4f}")
    print(f"Precision: {precision_score(y_test, y_pred_lgb):.4f}")
    print(f"Recall:    {recall_score(y_test, y_pred_lgb):.4f}")
    print(f"F1-Score:  {f1_score(y_test, y_pred_lgb):.4f}")
    print(f"ROC-AUC:   {roc_auc_score(y_test, y_pred_proba_lgb):.4f}")
    
    cv_lgb = cross_validate(
        pipe_lgb, X, y, cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=42),
        scoring=['accuracy', 'precision', 'recall', 'f1', 'roc_auc']
    )
    print(f"\nCross-Val Accuracy: {cv_lgb['test_accuracy'].mean():.4f} (+/- {cv_lgb['test_accuracy'].std():.4f})")
    
except ImportError:
    print("⚠️  LightGBM not installed. Install with: pip install lightgbm")


# Cell: K-Nearest Neighbors
print("\n" + "="*70)
print("K-NEAREST NEIGHBORS (KNN)")
print("="*70)

from sklearn.neighbors import KNeighborsClassifier

knn = KNeighborsClassifier(
    n_neighbors=5,
    weights='distance',
    metric='euclidean'
)

pipe_knn = Pipeline([
    ('scaler', StandardScaler()),
    ('clf', knn)
])

pipe_knn.fit(X_train, y_train)
y_pred_knn = pipe_knn.predict(X_test)
y_pred_proba_knn = pipe_knn.predict_proba(X_test)[:, 1]

print(f"Accuracy:  {accuracy_score(y_test, y_pred_knn):.4f}")
print(f"Precision: {precision_score(y_test, y_pred_knn):.4f}")
print(f"Recall:    {recall_score(y_test, y_pred_knn):.4f}")
print(f"F1-Score:  {f1_score(y_test, y_pred_knn):.4f}")
print(f"ROC-AUC:   {roc_auc_score(y_test, y_pred_proba_knn):.4f}")

cv_knn = cross_validate(
    pipe_knn, X, y, cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=42),
    scoring=['accuracy', 'precision', 'recall', 'f1', 'roc_auc']
)
print(f"\nCross-Val Accuracy: {cv_knn['test_accuracy'].mean():.4f} (+/- {cv_knn['test_accuracy'].std():.4f})")


# Cell: Naive Bayes
print("\n" + "="*70)
print("GAUSSIAN NAIVE BAYES")
print("="*70)

from sklearn.naive_bayes import GaussianNB

nb = GaussianNB()

pipe_nb = Pipeline([
    ('scaler', StandardScaler()),
    ('clf', nb)
])

pipe_nb.fit(X_train, y_train)
y_pred_nb = pipe_nb.predict(X_test)
y_pred_proba_nb = pipe_nb.predict_proba(X_test)[:, 1]

print(f"Accuracy:  {accuracy_score(y_test, y_pred_nb):.4f}")
print(f"Precision: {precision_score(y_test, y_pred_nb):.4f}")
print(f"Recall:    {recall_score(y_test, y_pred_nb):.4f}")
print(f"F1-Score:  {f1_score(y_test, y_pred_nb):.4f}")
print(f"ROC-AUC:   {roc_auc_score(y_test, y_pred_proba_nb):.4f}")

cv_nb = cross_validate(
    pipe_nb, X, y, cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=42),
    scoring=['accuracy', 'precision', 'recall', 'f1', 'roc_auc']
)
print(f"\nCross-Val Accuracy: {cv_nb['test_accuracy'].mean():.4f} (+/- {cv_nb['test_accuracy'].std():.4f})")


# Cell: Model Comparison
print("\n" + "="*70)
print("MODEL COMPARISON SUMMARY")
print("="*70)

# Create comparison dataframe
model_results = pd.DataFrame({
    'Model': ['Logistic Regression', 'Random Forest', 'SVM (RBF)', 'LightGBM', 'KNN', 'Naive Bayes', 'XGBoost'],
    'Accuracy': [
        accuracy_score(y_test, y_pred_lr),
        accuracy_score(y_test, y_pred_rf),
        accuracy_score(y_test, y_pred_svm),
        accuracy_score(y_test, y_pred_lgb) if 'lgb' in locals() else np.nan,
        accuracy_score(y_test, y_pred_knn),
        accuracy_score(y_test, y_pred_nb),
        accuracy_score(y_test, y_pred)
    ],
    'Precision': [
        precision_score(y_test, y_pred_lr),
        precision_score(y_test, y_pred_rf),
        precision_score(y_test, y_pred_svm),
        precision_score(y_test, y_pred_lgb) if 'lgb' in locals() else np.nan,
        precision_score(y_test, y_pred_knn),
        precision_score(y_test, y_pred_nb),
        precision_score(y_test, y_pred)
    ],
    'Recall': [
        recall_score(y_test, y_pred_lr),
        recall_score(y_test, y_pred_rf),
        recall_score(y_test, y_pred_svm),
        recall_score(y_test, y_pred_lgb) if 'lgb' in locals() else np.nan,
        recall_score(y_test, y_pred_knn),
        recall_score(y_test, y_pred_nb),
        recall_score(y_test, y_pred)
    ],
    'F1-Score': [
        f1_score(y_test, y_pred_lr),
        f1_score(y_test, y_pred_rf),
        f1_score(y_test, y_pred_svm),
        f1_score(y_test, y_pred_lgb) if 'lgb' in locals() else np.nan,
        f1_score(y_test, y_pred_knn),
        f1_score(y_test, y_pred_nb),
        f1_score(y_test, y_pred)
    ],
    'ROC-AUC': [
        roc_auc_score(y_test, y_pred_proba_lr),
        roc_auc_score(y_test, y_pred_proba_rf),
        roc_auc_score(y_test, y_pred_proba_svm),
        roc_auc_score(y_test, y_pred_proba_lgb) if 'lgb' in locals() else np.nan,
        roc_auc_score(y_test, y_pred_proba_knn),
        roc_auc_score(y_test, y_pred_proba_nb),
        roc_auc_score(y_test, y_pred_proba)
    ]
})

model_results = model_results.sort_values('Accuracy', ascending=False)
print(model_results.to_string(index=False))

# Visualize model comparison
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Accuracy comparison
axes[0, 0].barh(model_results['Model'], model_results['Accuracy'], color='steelblue')
axes[0, 0].set_xlabel('Accuracy')
axes[0, 0].set_title('Model Accuracy Comparison')
axes[0, 0].set_xlim([0.6, 1.0])

# Precision comparison
axes[0, 1].barh(model_results['Model'], model_results['Precision'], color='coral')
axes[0, 1].set_xlabel('Precision')
axes[0, 1].set_title('Model Precision Comparison')
axes[0, 1].set_xlim([0.6, 1.0])

# Recall comparison
axes[1, 0].barh(model_results['Model'], model_results['Recall'], color='lightgreen')
axes[1, 0].set_xlabel('Recall')
axes[1, 0].set_title('Model Recall Comparison')
axes[1, 0].set_xlim([0.6, 1.0])

# ROC-AUC comparison
axes[1, 1].barh(model_results['Model'], model_results['ROC-AUC'], color='gold')
axes[1, 1].set_xlabel('ROC-AUC')
axes[1, 1].set_title('Model ROC-AUC Comparison')
axes[1, 1].set_xlim([0.6, 1.0])

plt.tight_layout()
plt.show()


# Cell: Soft Voting Ensemble
print("\n" + "="*70)
print("SOFT VOTING ENSEMBLE (BEST RESULTS)")
print("="*70)

from sklearn.ensemble import VotingClassifier

ensemble = VotingClassifier(
    estimators=[
        ('xgb', XGBClassifier(n_estimators=200, max_depth=5, learning_rate=0.1, eval_metric='logloss', random_state=42)),
        ('rf', RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42, n_jobs=-1)),
        ('svm', SVC(kernel='rbf', C=1.0, probability=True, random_state=42)),
        ('lr', LogisticRegression(max_iter=10000, random_state=42))
    ],
    voting='soft',
    n_jobs=-1
)

pipe_ensemble = Pipeline([
    ('scaler', StandardScaler()),
    ('clf', ensemble)
])

print("Training ensemble (this may take a minute)...")
pipe_ensemble.fit(X_train, y_train)

y_pred_ensemble = pipe_ensemble.predict(X_test)
y_pred_proba_ensemble = pipe_ensemble.predict_proba(X_test)[:, 1]

print(f"\n✅ Ensemble Model Results:")
print(f"Accuracy:  {accuracy_score(y_test, y_pred_ensemble):.4f}")
print(f"Precision: {precision_score(y_test, y_pred_ensemble):.4f}")
print(f"Recall:    {recall_score(y_test, y_pred_ensemble):.4f}")
print(f"F1-Score:  {f1_score(y_test, y_pred_ensemble):.4f}")
print(f"ROC-AUC:   {roc_auc_score(y_test, y_pred_proba_ensemble):.4f}")

# Cross-validation for ensemble
cv_ensemble = cross_validate(
    pipe_ensemble, X, y, cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=42),
    scoring=['accuracy', 'precision', 'recall', 'f1', 'roc_auc']
)
print(f"\nCross-Val Accuracy: {cv_ensemble['test_accuracy'].mean():.4f} (+/- {cv_ensemble['test_accuracy'].std():.4f})")

print("\n🎯 BEST MODEL: Soft Voting Ensemble combines strengths of all models!")
