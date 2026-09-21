import sys
from typing import Optional

import pandas as pd

from src.configuration.mongo_db_connection import MongoDBClient
from src.constants.database import DATABASE_NAME
from src.exception.base import HeartStrokeException


class StrokeData:
    """
    This class help to export entire mongo db record as pandas dataframe
    """

    def __init__(self):
        """ """
        try:
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)

        except Exception as e:
            raise HeartStrokeException(e, sys) from e

    def export_collection_as_dataframe(
        self, collection_name: str, database_name: Optional[str] = None
    ) -> pd.DataFrame:
        try:
            """
            export entire collection as dataframe:
            return pd.DataFrame of collection
            """
            if database_name is None:
                collection = self.mongo_client.database[collection_name]
            else:
                collection = self.mongo_client[database_name][collection_name]
            df = pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df.drop(columns=["_id"], inplace=True)
            return df

        except Exception as e:
            raise HeartStrokeException(e, sys) from e
