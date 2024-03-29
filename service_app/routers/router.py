import json
from fastapi import APIRouter

from service_app.helpers.spark import Spark

router = APIRouter()
SPARK = Spark()


@router.get("/api/v1/top-titles/",
            tags=["Titles"],
            description="Get endpoint to retrieve the top 15 Movies from the following dataset https://datasets.imdbws.com/",
            )
def read_root():
    cleaned_data = []

    for item in SPARK.get_top_titles():
        # Remove backslashes and convert to a dictionary
        cleaned_item = json.loads(item.replace('\\', ''))
        cleaned_data.append(cleaned_item)

    return cleaned_data
