import os
import sys

from pandas import DataFrame
from sklearn.model_selection import train_test_split

from src.constants.training_pipeline import SCHEMA_FILE_PATH
from src.data_access.heart_stroke_data import StrokeData
from src.entity.artifact_entity import DataIngestionArtifact
from src.entity.config_entity import DataIngestionConfig
from src.exception.base import HeartStrokeException
from src.logger import logging
from src.utils.main_utils import read_yaml_file


class DataIngestion:
    """
    Handle the data ingestion stage of the ML pipeline.

    This class initializes and manages the configuration
    required for data ingestion operations.

    Parameters
    ----------
    data_ingestion_config : DataIngestionConfig, optional
        Configuration object containing ingestion-related
        parameters and file paths. By default,
        DataIngestionConfig() is used.

    Attributes
    ----------
    data_ingestion_config : DataIngestionConfig
        Stores the configuration object for the
        data ingestion component.

    Raises
    ------
    HeartStrokeException
        If any exception occurs during initialization.
    """
    def __init__(self, data_ingestion_config: DataIngestionConfig = DataIngestionConfig()):
        try:
            logging.info("Initalizing DataIngestion component")

            self.data_ingestion_config = data_ingestion_config

            logging.info("DataIngestion component initalized successfully")

        except Exception as e:
            logging.error("Failed to initialized DataIngestion compoenent")
            raise HeartStrokeException(e, sys) from e

    def export_data_into_feature_store(self) -> DataFrame:
        """
        Export data from MongoDB into the feature store.

        This method fetches data from the MongoDB collection,
        converts it into a pandas DataFrame, and stores the
        exported dataset into the configured feature store path.

        Returns
        -------
        DataFrame
            DataFrame containing the exported feature store data.

        Raises
        ------
        HeartStrokeException
            If any exception occurs during data export or
            feature store creation.
        """
        try:
            logging.info("Exporting data from MongoDB collection")

            heart_stroke_data = StrokeData()

            dataframe = heart_stroke_data.export_collection_as_dataframe(
                collection_name=self.data_ingestion_config.collection_name
            )

            logging.info(f"Exported of dataframe shape: {dataframe.shape}")

            feature_store_file_path = (self.data_ingestion_config.feature_store_file_path)

            dir_path = os.path.dirname(feature_store_file_path)

            os.makedirs(dir_path, exist_ok=True)

            logging.info(
                f"Saving dataframe into feature store path: "
                f"{feature_store_file_path}"
            )

            dataframe.to_csv(
                feature_store_file_path,
                index=False,
                header=True,
            )

            logging.info("Data successfully saved into feature store")

            return dataframe

        except Exception as e:
            logging.exception("Exception occured while exporting data into feature store")
            raise HeartStrokeException(e, sys) from e

    def split_data_as_train_test(self, dataframe: DataFrame) -> None:
        """
        Split the dataset into training and testing stes.

        This method performs a train-test split on the input
        dataframe using the configured split ratio and stores
        the resulting datasets into their respective file paths.

        Parameters
        ----------
        dataframe : DataFrame
            Input dataframe to be split into train and test sets.

        Raises
        ------
        HeartStrokeException
            If any exception occurs during dataset splitting
            or file export operations.
        """

        try:
            logging.info(
                "Starting train-test split operation"
            )

            train_set, test_set = train_test_split(
                dataframe,
                test_size=(
                    self.data_ingestion_config.train_test_split_ratio
                ),
                random_state=42,
            )

            logging.info(
                f"Train dataset shape: {train_set.shape}"
            )

            logging.info(
                f"Test dataset shape: {test_set.shape}"
            )

            training_dir = os.path.dirname(
                self.data_ingestion_config.training_file_path
            )

            os.makedirs(
                training_dir,
                exist_ok=True,
            )

            logging.info(
                "Saving train dataset to: "
                f"{self.data_ingestion_config.training_file_path}"
            )

            train_set.to_csv(
                self.data_ingestion_config.training_file_path,
                index=False,
                header=True,
            )

            logging.info(
                "Saving testing dataset to: "
                f"{self.data_ingestion_config.testing_file_path}"
            )

            test_set.to_csv(
                self.data_ingestion_config.testing_file_path,
                index=False,
                header=True,
            )

            logging.info(
                "Train and test datasets saved successfully"
            )

        except Exception as e:
            logging.exception(
                "Exception occured during train-test split process"
            )
            raise HeartStrokeException(e, sys) from e

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        """
        Initiate the data ingestion pipeline.

        This method orchestrates the complete data ingestion
        workflow, including:

        1. Exporting data from MongoDB into the feature, store.
        2. Reading schema configuration.
        3. Dropping unwanted columns from the dataset.
        4. Performing train-test split.
        5. Creating and returning the data ingestion artifact.

        Returns
        -------
        DataIngestionArtifact
            Artifact containing paths to the generated
            training and testing datasets.

        Raises
        ------
        HeartStrokeException
            If any exception occurs during the data ingestion
            pipeline execution.
        """
        try:
            logging.info("Starting data ingestion pipeline")

            dataframe = self.export_data_into_feature_store()

            _schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)

            drop_columns = _schema_config.get("Drop_columns", [])

            if drop_columns:
                logging.info(f"Dropping columns: {drop_columns}")

                dataframe = dataframe.drop(
                    columns=drop_columns,
                )

            logging.info(
                f"Processed dataframe shape: "
                f"{dataframe.shape}"
            )

            logging.info("Performing train-test split")

            self.split_data_as_train_test(dataframe)

            logging.info("Train-test split completed successfully")

            data_ingestion_artifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path,
            )

            logging.info(
                f"Data ingestion artifact details: "
                f"{data_ingestion_artifact}"
            )

            logging.info(
                "Data ingestion pipeline completed successfully"
            )

            return data_ingestion_artifact

        except Exception as e:
            logging.exception(
                "Data ingestion pipeline execution failed"
            )
            raise HeartStrokeException(e, sys) from e
