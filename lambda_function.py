from azure.storage.blob import BlobServiceClient
import pandas as pd
import io
import json
import os

CONNECTION_STRING = "UseDevelopmentStorage=true"
CONTAINER_NAME = "datasets"
BLOB_NAME = "All_Diets.csv"

OUTPUT_DIR = "simulated_nosql"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "results.json")


def process_nutritional_data_from_azurite():
    print("Connecting to Azurite...")

    # Connect to the Azurite Blob service
    blob_service_client = BlobServiceClient.from_connection_string(
        CONNECTION_STRING
    )

    # init client
    blob_client = blob_service_client.get_blob_client(
        container=CONTAINER_NAME,
        blob=BLOB_NAME,
    )


    print(f"Downloading {BLOB_NAME} from Azurite...")

    # Download the blob data from Azurite
    blob_data = blob_client.download_blob().readall()

    print("Loading CSV into Pandas...")

    df = pd.read_csv(io.BytesIO(blob_data))

    # Keep only the columns required for this operation
    required_columns = [
        "Diet_type",
        "Protein(g)",
        "Carbs(g)",
        "Fat(g)",
    ]


    #  --- Process Data ---
    df = df[required_columns].copy()

    numeric_columns = [
        "Protein(g)",
        "Carbs(g)",
        "Fat(g)",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df = df.dropna(subset=required_columns)

    print("Calculating average macronutrients by diet type...")

    avg_macros = (
        df.groupby("Diet_type")[
            ["Protein(g)", "Carbs(g)", "Fat(g)"]
        ]
        .mean()
        .round(2)
        .reset_index()
    )

    # Results to be saved as JSON
    results = avg_macros.to_dict(orient="records")
    
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_FILE, "w") as file:
        json.dump(results, file, indent=4)

    print(f"Processed {len(df)} recipes.")
    print(f"Calculated averages for {len(results)} diet types.")
    print(f"Results saved to {OUTPUT_FILE}")

    return results


if __name__ == "__main__":
    process_nutritional_data_from_azurite()