import snowflake.snowpark.functions as F
from snowflake.snowpark import DataFrame


def get_shipment(tracking_number: str) -> DataFrame:
    return session.table("staging.charge.premodel").where(
        F.col("tracking_number") == tracking_number
    )
