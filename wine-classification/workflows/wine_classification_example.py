import pandas as pd
import numpy as np

from sklearn.datasets import load_wine
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
from flytekit import task, workflow
# import seaborn as sns
# from flytekitplugins.mlflow import mlflow_autolog
import mlflow
from typing import List, Tuple, Dict
from flytekit import ImageSpec

sklearn_image_spec = ImageSpec(
    packages=["mlflow"]
)

@task(container_image=sklearn_image_spec)
def get_data() -> pd.DataFrame:
    """Get the wine dataset."""
    return load_wine(as_frame=True).frame

@task(container_image=sklearn_image_spec)
def process_data(data: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Simplify the task from a 3-class to a binary classification problem."""
    data_out = data.assign(target=lambda x: x["target"].where(x["target"] == 0, 1))
    data_out_train, data_out_test = train_test_split(data_out, test_size=0.2, random_state=42)

    train_x = data_out_train.drop("target", axis=1)
    test_x = data_out_test.drop("target", axis=1)
    train_y = data_out_train[["target"]]
    test_y = data_out_test[["target"]]

    return train_x, test_x, train_y, test_y
    
@task(container_image=sklearn_image_spec)
# @mlflow_autolog(framework=mlflow.sklearn)
def train_model(
    train_x: pd.DataFrame, 
    test_x: pd.DataFrame, 
    train_y: pd.DataFrame, 
    test_y: pd.DataFrame, 
    params: Dict[str, float]) -> Tuple[float, float, LogisticRegression]:
    """Train a model on the wine dataset."""

    lr = LogisticRegression(max_iter=3000, **params)
    lr.fit(train_x, train_y.iloc[:, 0])

    pred_y = lr.predict(test_x)
    mse = float(mean_squared_error(test_y, pred_y))
    mae = float(mean_absolute_error(test_y, pred_y))

    return mse, mae, lr


@task(container_image=sklearn_image_spec)
def training_model_loop(
    train_x: pd.DataFrame, 
    test_x: pd.DataFrame, 
    train_y: pd.DataFrame, 
    test_y: pd.DataFrame, 
    params_list: List[Dict[str, float]] = [{"C": 0.1}, {"C": 0.2}, {"C": 0.3}, {"C": 0.4}]
) -> None:

    print(params_list)

    for params_i in params_list:
        print('ahhhh')
        print(params_i)
        rmse_i, mae_i, lr_i = train_model(
            train_x = train_x,
            test_x = test_x,
            train_y = train_y,
            test_y = test_y,
            params=params_i,
        )

@workflow
def training_workflow(params_list: List[Dict[str, float]] = [{"C": 0.1}, {"C": 0.2}, {"C": 0.3}, {"C": 0.4}]) -> None:
    """Put all of the steps together into a single workflow."""
    # raise Exception("This is a test")
    data = get_data()
    train_x, test_x, train_y, test_y = process_data(data=data)

    print(params_list)

    training_model_loop(
        train_x = train_x,
        test_x = test_x,
        train_y = train_y,
        test_y = test_y,
        params_list=params_list,
    )

if __name__ == "__main__":
    training_workflow(params_list=[{"C": 0.1}, {"C": 0.2}, {"C": 0.3}, {"C": 0.4}])
