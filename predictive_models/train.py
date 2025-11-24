from .pipeline import get_data, create_evaluate_pipeline, create_pipeline, model_eval_RMSE

def train_model(model_type: str) -> None:
    train_rmse = float("inf")
    final_model_type = "rf"
    
    train_X, test_X, train_y, test_y = get_data()

    for model_type in ("xgb", "rf"):
        eval_model = create_evaluate_pipeline(train_X, train_y, 3, model_type)
        train_rmse_model, test_rmse_model = model_eval_RMSE(eval_model, train_X, test_X, train_y, test_y)
    
        if train_rmse_model < train_rmse:
            train_rmse = train_rmse_model
            test_rmse = test_rmse_model
            final_model_type = model_type


    if train_rmse < 0.2 and test_rmse < 0.25:
        model = create_pipeline(train_X, test_X, train_y, test_y, 3, final_model_type)

        # update model 




