from networksecurity.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact
)
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.utils.main_utils.utils import read_yaml_file, write_yaml_file

from scipy.stats import ks_2samp
import pandas as pd
import numpy as np
import os, sys


class DataValidation:
    def __init__(
        self,
        data_ingestion_artifact: DataIngestionArtifact,
        data_validation_config: DataValidationConfig
    ):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    # -----------------------------
    # Read CSV
    # -----------------------------
    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    # -----------------------------
    # Column count validation
    # -----------------------------
    def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool:
        try:
            required_columns = self._schema_config["columns"]
            number_of_columns = len(required_columns)

            logging.info(f"Required number of columns: {number_of_columns}")
            logging.info(f"Data frame has columns: {len(dataframe.columns)}")

            return len(dataframe.columns) == number_of_columns

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    # -----------------------------
    # Non-numerical column check
    # -----------------------------
    def check_non_numerical_columns(self, dataframe: pd.DataFrame) -> bool:
        try:
            non_numeric_columns = dataframe.select_dtypes(
                exclude=[np.number]
            ).columns

            if len(non_numeric_columns) > 0:
                logging.error(
                    f"Non-numerical columns found: {list(non_numeric_columns)}"
                )
                return False

            logging.info("No non-numerical columns found")
            return True

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    # -----------------------------
    # Data drift detection (KS-Test)
    # -----------------------------
    def detect_dataset_drift(
        self,
        base_df: pd.DataFrame,
        current_df: pd.DataFrame,
        threshold: float = 0.05
    ) -> bool:
        """
        Returns True -> No drift
        Returns False -> Drift found
        """
        try:
            status = True
            report = {}

            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]

                ks_result = ks_2samp(d1, d2)

                drift_status = ks_result.pvalue < threshold

                if drift_status:
                    status = False

                report[column] = {
                    "p_value": float(ks_result.pvalue),
                    "drift_status": drift_status
                }

            # Create drift report directory
            drift_report_path = self.data_validation_config.drift_report_file_path
            os.makedirs(os.path.dirname(drift_report_path), exist_ok=True)

            # Write report.yaml
            write_yaml_file(
                file_path=drift_report_path,
                content=report
            )

            logging.info("Data drift report generated successfully")

            return status

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    # -----------------------------
    # Main validation method
    # -----------------------------
    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            train_dataframe = self.read_data(train_file_path)
            test_dataframe = self.read_data(test_file_path)

            # Force numeric conversion (safety)
            train_dataframe = train_dataframe.apply(
                pd.to_numeric, errors="coerce"
            )
            test_dataframe = test_dataframe.apply(
                pd.to_numeric, errors="coerce"
            )

            # 1️⃣ Column count validation
            train_col_status = self.validate_number_of_columns(train_dataframe)
            test_col_status = self.validate_number_of_columns(test_dataframe)

            # 2️⃣ Non-numerical check
            train_dtype_status = self.check_non_numerical_columns(train_dataframe)
            test_dtype_status = self.check_non_numerical_columns(test_dataframe)

            # 3️⃣ Data drift check
            drift_status = self.detect_dataset_drift(
                base_df=train_dataframe,
                current_df=test_dataframe
            )

            validation_status = (
                train_col_status
                and test_col_status
                and train_dtype_status
                and test_dtype_status
            
            )

            if validation_status:
                os.makedirs(
                    os.path.dirname(
                        self.data_validation_config.valid_train_file_path
                    ),
                    exist_ok=True
                )

                train_dataframe.to_csv(
                    self.data_validation_config.valid_train_file_path,
                    index=False,
                    header=True
                )

                test_dataframe.to_csv(
                    self.data_validation_config.valid_test_file_path,
                    index=False,
                    header=True
                )

            return DataValidationArtifact(
                validation_status=validation_status,
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )
        
            

        except Exception as e:
            raise NetworkSecurityException(e, sys)
