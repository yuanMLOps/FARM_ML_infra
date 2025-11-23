import pandas as pd
from pandas import DataFrame
import numpy as np
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestRegressor
from xgboost.sklearn import XGBRegressor
import xgboost as xgb

from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

import optuna


def plot_PC_explained(X: pd.DataFrame) -> None:
    standard_scaler = StandardScaler()
    scaled_X = standard_scaler.fit_transform(X)

    pca = PCA()
    pca_scores = pca.fit_transform(scaled_X)
    cum_variance_explained = np.cumsum(pca.explained_variance_ratio_)

    plt.figure(figsize = (8, 6))
    plt.plot(range(1, len(cum_variance_explained)+1), cum_variance_explained,
                   marker='o', linestyle="--")
    plt.xlabel("Number of Compoent")
    plt.ylabel("Cumulative Variance Explained")
    plt.grid()
    plt.show()


def plot_2D_biplot(df: DataFrame, target_col: str) -> None:
    """
    plot 2D biplot from the original dataframe containing original features and target column
    """
    
    X, y = df.drop(columns=[target_col]), df[target_col]
    standard_scaler = StandardScaler()
    scaled_X = standard_scaler.fit_transform(X)
    scaled_X_df = pd.DataFrame(scaled_X, columns = X.columns)

    pca = PCA(n_components=2)
    pca_scores = pca.fit_transform(scaled_X)
    PC2_df = pd.DataFrame(pca_scores, columns=["PC1", "PC2"])
    loadings = pca.components_.T * np.sqrt(pca.explained_variance_)

    plt.figure(figsize=(8,6))
    scatter = plt.scatter(data=PC2_df, x="PC1", y="PC2", c=y, cmap='viridis', s=50)
    for i, varname in enumerate(scaled_X_df.columns):  # Exclude the 'Color' column
        plt.arrow(0, 0, loadings[i, 0] *2, loadings[i, 1] *2, color='r', alpha=0.5)
        plt.text(loadings[i, 0] * 2.15, loadings[i, 1] * 2.15, varname, color='r', ha='center', va='center')
    plt.colorbar(scatter, label='Color')
    plt.xlabel("PC1")
    plt.ylabel("PC2")     

    plt.show()  

def plot_3D_PCA_dist(PCA_df: DataFrame, PCA_cols: list[str], y_col: str):
    
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    X_pca = PCA_df
    PC1, PC2, PC3 = PCA_cols
    
    sc = ax.scatter(
        X_pca[PC1],  # PC1
        X_pca[PC2],  # PC2
        X_pca[PC3],  # PC3
        c=X_pca[y_col],
        cmap='viridis',  # or 'tab10' for discrete classes
        s=28,
        alpha=0.9
    )
    
    ax.set_xlabel(PC1)
    ax.set_ylabel(PC2)
    ax.set_zlabel(PC3)
    ax.set_title('3D PCA scatter')

    # Colorbar for numeric labels; for categorical, map colors manually (see next snippet)
    cbar = plt.colorbar(sc, ax=ax, shrink=0.7)
    cbar.set_label(y_col)
    
    plt.tight_layout()
    plt.show()


def plot_feature_importance(rf,features):
    importances=rf.feature_importances_
    imp_std=np.std([tree.feature_importances_ for tree in rf.estimators_],axis=0)
    imp_idx=np.argsort(importances)   
    
    print("feature ranking")
    for name, importance in zip(features[imp_idx[::-1]],importances[imp_idx[::-1]]):
        print("feature name: %s %f" %(name,importance))
    
    plt.figure(figsize=(10,7))
    plt.barh(range(len(importances)),importances[imp_idx],xerr=imp_std[imp_idx],color='b')
    plt.yticks(range(len(importances)),features[imp_idx])


def plot_pred_vs_test(test_y, pred_y):
    plt.figure(figsize=(8,6))
    scatter = plt.scatter(x=test_y, y=pred_y, marker="o", c="b", s=50, alpha=0.7)
    plt.xlabel("measured")
    plt.ylabel("predicted")
    plt.title("Predicted vs. Measured")

    # add y = x reference line
    min_val = min(test_y.min(), pred_y.min())
    max_val = max(test_y.max(), pred_y.max())
    plt.plot([min_val, max_val], [min_val, max_val], 'k--', lw=2, label='Ideal: y = x')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

