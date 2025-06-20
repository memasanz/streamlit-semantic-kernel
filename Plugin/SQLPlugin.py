import os
import pyodbc
import pandas as pd
from sqlalchemy import create_engine
from typing import Annotated
from semantic_kernel.functions.kernel_function_decorator import kernel_function


class SQLPlugin:
    """A plugin that retrieves data from a SQL database."""

    def _get_sqlalchemy_engine(self):
        """Helper method to create a SQLAlchemy engine using available drivers."""
        username = os.getenv("SQL_USERNAME")
        password = os.getenv("SQL_PASSWORD")
        server = os.getenv("SQL_SERVER")
        database = os.getenv("SQL_DATABASE")

        available_drivers = pyodbc.drivers()
        preferred_drivers = ["ODBC Driver 18 for SQL Server", "ODBC Driver 17 for SQL Server"]
        selected_driver = next((driver for driver in preferred_drivers if driver in available_drivers), None)

        if not selected_driver:
            raise Exception("Neither ODBC Driver 17 nor 18 for SQL Server is installed.")

        print("*******************")
        return create_engine(
            f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver={selected_driver.replace(' ', '+')}"
        )

    @kernel_function(name="check_installed_drivers", description="Check installed drivers if having issue connecting to SQL Server")
    def check_driver(self, driver: Annotated[str, "The input driver"]) -> Annotated[str, "The output is a string"]:
        try:
            drivers = pyodbc.drivers()
            return f"Driver '{driver}' is {'installed' if driver in drivers else 'not installed'}."
        except Exception as e:
            return f"Error checking driver: {e}"

    @kernel_function(name="get_tables", description="Get tables for database to assist in writing SQL queries")
    def get_tables(self) -> Annotated[str, "The output is an HTML table"]:
        try:
            engine = self._get_sqlalchemy_engine()
            query = "SELECT TABLE_SCHEMA, TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'"
            df = pd.read_sql(query, engine)
            return df.to_html(index=False, border=0, justify='center', classes='table table-striped table-bordered')
        except Exception as e:
            print("Error:", e)
            return f"Error retrieving tables: {e}"

    @kernel_function(name="get_table_schema", description="Get schema for a table to assist in writing SQL queries")
    def get_table_schema(self, table_name: str) -> Annotated[str, "The output is an HTML table"]:
        try:
            engine = self._get_sqlalchemy_engine()
            query = f"""
                SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH, IS_NULLABLE
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME = '{table_name}'
            """
            df = pd.read_sql(query, engine)
            return df.to_html(index=False, border=0, justify='center', classes='table table-striped table-bordered')
        except Exception as e:
            print("Error:", e)
            return f"Error retrieving schema for table '{table_name}': {e}"

    @kernel_function(name="execute_sql", description="With a SELECT statement, query the database and return the results as an HTML table")
    def execute_sql(self, query: str) -> Annotated[str, "The output is an HTML table"]:
        try:
            engine = self._get_sqlalchemy_engine()
            df = pd.read_sql(query, engine)
            return df.to_html(index=False, border=0, justify='center', classes='table table-striped table-bordered')
        except Exception as e:
            print("Error:", e)
            return f"Error executing query: {e}"
