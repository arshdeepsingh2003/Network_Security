import os
from dataclasses import dataclass
from networksecurity.constant import training_pipeline

from networksecurity.constant.training_pipeline import *

# -----------------------------
# Training Pipeline Config
# -----------------------------

@dataclass
class TrainingPipelineConfig:
    pipeline_name: str = training_pipeline.PIPELINE_NAME
    artifact_dir: str = training_pipeline.ARTIFACT_DIR

    def __post_init__(self):
        # Create artifact directory if it doesn't exist
        os.makedirs(self.artifact_dir, exist_ok=True)


# -----------------------------
# Data Ingestion Config
# -----------------------------

@dataclass
class DataIngestionConfig:
    training_pipeline_config: TrainingPipelineConfig

    def __post_init__(self):
        # Main data ingestion directory inside artifacts
        self.data_ingestion_dir: str = os.path.join(
            self.training_pipeline_config.artifact_dir,
            training_pipeline.DATA_INGESTION_DIR_NAME
        )

        # Feature store directory
        self.feature_store_dir: str = os.path.join(
            self.data_ingestion_dir,
            training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR
        )

        # ✅ ADD THIS (REQUIRED)
        self.feature_store_file_path: str = os.path.join(
            self.feature_store_dir,
            training_pipeline.FILE_NAME
        )

        # Ingested (train/test) data directory
        self.ingested_dir: str = os.path.join(
            self.data_ingestion_dir,
            training_pipeline.DATA_INGESTION_INGESTED_DIR
        )

        # File paths
        self.train_file_path: str = os.path.join(
            self.ingested_dir,
            training_pipeline.TRAIN_FILE_NAME
        )

        self.test_file_path: str = os.path.join(
            self.ingested_dir,
            training_pipeline.TEST_FILE_NAME
        )

        # MongoDB config
        self.database_name: str = training_pipeline.DATA_INGESTION_DATABASE_NAME
        self.collection_name: str = training_pipeline.DATA_INGESTION_COLLECTION_NAME

        # Train-test split ratio
        self.train_test_split_ratio: float = (
            training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        )

        # Create directories
        os.makedirs(self.feature_store_dir, exist_ok=True)
        os.makedirs(self.ingested_dir, exist_ok=True)





class DataValidationConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        
        self.data_validation_dir: str = os.path.join(
            training_pipeline_config.artifact_dir,
            training_pipeline.DATA_VALIDATION_DIR_NAME
        )

        self.valid_data_dir: str = os.path.join(
            self.data_validation_dir,
            training_pipeline.DATA_VALIDATION_VALID_DIR
        )

        self.invalid_data_dir: str = os.path.join(
            self.data_validation_dir,
            training_pipeline.DATA_VALIDATION_INVALID_DIR
        )

        self.valid_train_file_path: str = os.path.join(
            self.valid_data_dir,
            training_pipeline.TRAIN_FILE_NAME
        )

        self.valid_test_file_path: str = os.path.join(
            self.valid_data_dir,
            training_pipeline.TEST_FILE_NAME
        )

        self.invalid_train_file_path: str = os.path.join(
            self.invalid_data_dir,
            training_pipeline.TRAIN_FILE_NAME
        )

        self.invalid_test_file_path: str = os.path.join(
            self.invalid_data_dir,
            training_pipeline.TEST_FILE_NAME
        )

        self.drift_report_file_path: str = os.path.join(
            self.data_validation_dir,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME
        )
