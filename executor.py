from snowflake.snowpark import DataFrame

from reveel_lib.shipment import get_shipment

# from reveel_lib.pricing import get_modeled_price

SAFE_GLOBALS = {
    "__builtins__": {},
    "get_shipment": get_shipment,
    # "get_modeled_price": get_modeled_price,
    # "add_active_agreement_id": add_active_agreement_id,
    # "add_normalized_surcharge": add_normalized_surcharge,
    # "add_modeled_price": add_modeled_price,
}


def run_generated_code(code: str):
    output_df = eval(code, SAFE_GLOBALS)

    if not isinstance(output_df, DataFrame):
        raise ValueError("The output of the code is not a DataFrame.")

    output_df.show()
