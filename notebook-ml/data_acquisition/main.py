# AUTOGENERATED! DO NOT EDIT! File to edit: notebooks/01_data_acquisition.ipynb (unless otherwise specified).

__all__ = ['get_data', 'get_hold_out_data']

# Cell
import os
import sys
import pandas as pd
import argparse
from pathlib import Path


# sys.path.append(str(Path.cwd().parent / 'config'))
# Note the following import only works after adding current file to system path
import altaml_template_repo.config.default_config as config


def get_data() -> pd.DataFrame:
    # Read Data
    data_path = f"{config.INPUT_DATA_DIR}/{config.INPUT_DATA_NAME}"
    data = pd.read_csv(data_path)

    return data


def get_hold_out_data() -> pd.DataFrame:
    # Read Holdout Data
    hold_out_data_path = f"{config.INPUT_DATA_DIR}/{config.HOLD_OUT_DATA_NAME}"
    hold_out_data = pd.read_csv(hold_out_data_path)

    return hold_out_data


# Cell
if __name__ == "__main__":
    experiment_config = config
    if experiment_config.compute == 'azure':

        # Read Data
        data = get_data()

        # Get Run Context
        from azureml.core import Run
        run = Run.get_context()

        if experiment_config.output_dataset:
            path = Path(experiment_config.output_dataset)
            path.mkdir(exist_ok=True, parents=True)
            path = path / "processed.parquet"
            write_df = data.to_parquet(str(path), index=False)

        # Upload small sample holdout dataset to the parent Run
        # for testing deployed model purposes
        sample_hold_out_data = get_hold_out_data()
        temp_hold_out_data_path = "temp_hold_out_data.csv"
        sample_hold_out_data.to_csv(temp_hold_out_data_path, index=False)

        output_dir = experiment_config.model_dir
        path = Path(output_dir)
        path.mkdir(exist_ok=True, parents=True)
        run.parent.upload_file(f"{output_dir}/sample_holdout_data.csv", temp_hold_out_data_path)
