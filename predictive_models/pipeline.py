from sklearn.ensemble import RandomForestRegressor
from xgboost.sklearn import XGBRegressor
import pandas as pd
import numpy as np

from sklearn.metrics import mean_squared_error

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.pipeline import Pipeline

import optuna
import pickle

from .plots import plot_pred_vs_test


def model_eval_RMSE(model, train_X, train_y, test_X, test_y) -> tuple[float, float]:
    train_y_pred = model.predict(train_X)
    test_y_pred = model.predict(test_X)
    
    train_rmse = np.sqrt(mean_squared_error(train_y, train_y_pred))
    test_rmse = np.sqrt(mean_squared_error(test_y, test_y_pred))
    plot_pred_vs_test(train_y, train_y_pred)
    plot_pred_vs_test(test_y, test_y_pred)

    print(f"Training RMSE: {train_rmse:.4f}, Test RMSE: {test_rmse:.4f}")

    return train_rmse, test_rmse


def train_RF_model_optuna(X, y): 
    seed=342
    

    def objective(trial):
        n_estimators = trial.suggest_int("n_estimators", 50, 400)
        min_samples_split = trial.suggest_int("min_samples_split", 2, 5)  
        # min_samples_leaf = trial.suggest_int("min_samples_leaf", 1, 10)  	
    
        rf = RandomForestRegressor(n_jobs=-1, 
                                   n_estimators=n_estimators,
                                   min_samples_split = min_samples_split,
                                   random_state=seed)

        cv = KFold(n_splits=10, shuffle=True, random_state=seed)
        scores = cross_val_score(rf, X, y, cv=cv, scoring="neg_mean_squared_error")
        return np.mean(scores)

    study = optuna.create_study(direction="maximize")
    study.optimize(objective, show_progress_bar=False,n_trials=50)
    # vis.plot_optimization_history(study)

    best_params = study.best_params
    best_model = RandomForestRegressor(**best_params, random_state=seed)
    best_model.fit(X, y)

    return best_model, best_params

def train_XGBoost_model_optuna(X, y): 
    seed=342
    

    def objective(trial):
        n_estimators = trial.suggest_int("n_estimators", 50, 400)
        max_depth = trial.suggest_int("max_depth", 1, 20) 
        learning_rate = trial.suggest_float("learning_rate", 1e-4, 2, log=True)

        params_fixed = {
        'objective': 'reg:squarederror',
        'verbosity': 0           
        }
                   
        xgb_model = XGBRegressor(n_jobs=-1, **params_fixed,
                                   n_estimators=n_estimators,
                                   max_depth = max_depth,
                                   learning_rate=learning_rate,
                                   random_state=seed)

        cv = KFold(n_splits=10, shuffle=True, random_state=seed)
        try:
            scores = cross_val_score(xgb_model, X, y, cv=cv, scoring="neg_mean_squared_error")
            return np.mean(scores)
        except ValueError:
            return float("-inf")  # Penalize failed trials    

    study = optuna.create_study(direction="maximize")
    study.optimize(objective, show_progress_bar=False, n_trials=50)
    # vis.plot_optimization_history(study)

    best_params = study.best_params
    best_model = XGBRegressor(**best_params, random_state=seed)
    best_model.fit(X, y)

    return best_model, best_params


def create_preprocessor_pipeline(num_components):
    return Pipeline([('Scaler', StandardScaler()), ('PCA', PCA(n_components=num_components))])

def create_evaluate_pipeline(train_X: pd.DataFrame, train_y: pd.DataFrame, n_PCs: int, model_type: str):
    """
    create pipeline objects using the original training dataset containing all element ratios
    """
    if model_type != "rf" and model_type != "xgb":
        print("model type must be either rf or xgb")
        return
        
    preprocessor = create_preprocessor_pipeline(n_PCs)
    processed_X = preprocessor.fit_transform(train_X)

    if model_type == "rf":
        best_model, _ = train_RF_model_optuna(processed_X, train_y)

    else:
        best_model, _ = train_XGBoost_model_optuna(processed_X, train_y)
    
    return Pipeline([
        ('preprocess', preprocessor), # already fitted preprocessor
        ('model', best_model)             # already fitted model
        ])


def create_pipeline(train_X: pd.DataFrame, train_y: pd.DataFrame, test_X: pd.DataFrame,
                    test_y:pd.DataFrame, n_PCs: int, model_type: str):
    """
    create pipeline objects using the original training dataset containing all element ratios
    """
    if model_type != "rf" and model_type != "xgb":
        print("model type must be either rf or xgb")
        return
        
    preprocessor = create_preprocessor_pipeline(n_PCs)
    processed_X = preprocessor.fit_transform(train_X)

    if model_type == "rf":
        _, best_params = train_RF_model_optuna(processed_X, train_y)
        best_model = RandomForestRegressor(**best_params)

    else:
        _, best_params = train_XGBoost_model_optuna(processed_X, train_y)
        best_model = XGBRegressor(**best_params)
    
    X, y = pd.concat([train_X, test_X]), pd.concat([train_y, test_y])

    preprocessor_all = create_preprocessor_pipeline(n_PCs)
    processed_X = preprocessor_all.fit_transform(X)
    
    best_model.fit(processed_X, y)

    return Pipeline([
        ('preprocess', preprocessor_all), # already fitted preprocessor
        ('model', best_model)             # already fitted model
        ])
    
    