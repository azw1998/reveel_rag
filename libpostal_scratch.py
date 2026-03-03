from openai import OpenAI
import pymupdf
from pathlib import Path


# def extract_text_from_pdf(path):
#     doc = pymupdf.open(path)
#     return [page.get_text() for page in doc]


# def header_to_rule(text):
#     return text.split("\n")[1], text.split("\n", maxsplit=2)[-1]


def main():
    # PDF_PATH = "/Users/anthonywang/Downloads/Small_Business_Rate_Guide.pdf"
    # CARRIER = "UPS"
    # YEAR = 2024
    # with open("/Users/anthonywang/.langchain", "r") as f:
    #     api_key = f.read().strip()

    # client = OpenAI(api_key=api_key)

    # text = extract_text_from_pdf(
    #     "/Users/anthonywang/Downloads/Small_Business_Rate_Guide.pdf"
    # )

    # 0th page is cover, 1st page is table of contents,
    # 2nd page marks in tables the commitment days for the different services whether they're domestic or international
    # the next pages have rates
    # then a page about dim divisor
    # then a page about value-added surcharges (some surcharges are only available for certain services)
    # then a page about general surcharges
    # last page is more surcharges

    # base_rates = text[3:-4]
    # clean_base_rates = [header_to_rule(rate) for rate in base_rates]
    # print(clean_base_rates[0])
    file_path = Path("rag_docs/tables/premodel.txt")
    schema_doc = file_path.read_text(encoding="utf-8")

    with open("/Users/anthonywang/.langchain", "r") as f:
        api_key = f.read().strip()

    client = OpenAI(api_key=api_key)

    question = "What was the total demand surcharge spend plus surge surcharge spend for tracking number 1Z97Y6036659856231"

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": f"""
    You generate Databricks SQL.
    Use the schema below.

    Schema:
    {schema_doc}

    Return SELECT-only SQL.
    """,
            },
            {"role": "user", "content": question},
        ],
    )

    print(response.output_text)


if __name__ == "__main__":
    main()
