import pandas as pd
import numpy as np
from sklearn.datasets import load_wine
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
from flytekit import task, workflow
from typing import List, Tuple, Dict
from flytekit import ImageSpec
import mlflow
from flytekitplugins.mlflow import mlflow_autolog
from sklearn.model_selection import GridSearchCV

sklearn_image_spec = ImageSpec(
    base_image="ghcr.io/flyteorg/flytekit:py3.11-1.11.0",
    packages=["flytekit==1.11.0", "mlflow", "flytekitplugins-mlflow", "scikit-learn==1.2.2"],
    registry="localhost:30000"    
)

@task(container_image=sklearn_image_spec)
def get_data() -> pd.DataFrame:
    """Get the wine dataset."""
    return load_wine(as_frame=True).frame

@task(container_image=sklearn_image_spec)
def process_data(data: pd.DataFrame) -> pd.DataFrame:
    """Simplify the task from a 3-class to a binary classification problem."""
    data_out = data.assign(target=lambda x: x["target"].where(x["target"] == 0, 1))

    return data_out
    

@task(enable_deck=True, container_image=sklearn_image_spec)
@mlflow_autolog(framework=mlflow.sklearn)
def hyperparameter_search(
    data: pd.DataFrame,
) -> Tuple[LogisticRegression, pd.DataFrame]:

    params = {'solver': ['liblinear'], 'penalty': ['l1', 'l2'], 'C': [0.1, 0.2, 0.3, 0.4]}

    lr = LogisticRegression()
    grid_search = GridSearchCV(lr, param_grid=params, scoring='accuracy')  
    grid_search.fit(data.drop("target", axis=1), data["target"])

    return grid_search.best_estimator_, pd.DataFrame(grid_search.cv_results_)

@workflow
def training_workflow() -> Tuple[LogisticRegression, pd.DataFrame]:
    """Put all of the steps together into a single workflow."""
    # raise Exception("This is a test")
    data = get_data()
    data = process_data(data=data)

    best_model, cv_results = hyperparameter_search(
        data = data
    )

    return best_model, cv_results

if __name__ == "__main__":
    training_workflow()
