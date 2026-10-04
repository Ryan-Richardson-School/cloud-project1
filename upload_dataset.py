from azure.storage.blob import BlobServiceClient

CONNECTION_STRING = "UseDevelopmentStorage=true"
CONTAINER_NAME = "datasets"
BLOB_NAME = "All_Diets.csv"

blob_service_client = BlobServiceClient.from_connection_string(
    CONNECTION_STRING
)

container_client = blob_service_client.get_container_client(CONTAINER_NAME)

try:
    container_client.create_container()
    print(f"Created container: {CONTAINER_NAME}")
except Exception:
    print(f"Container '{CONTAINER_NAME}' already exists.")

blob_client = container_client.get_blob_client(BLOB_NAME)

with open(BLOB_NAME, "rb") as data:
    blob_client.upload_blob(data, overwrite=True)

print(f"Uploaded {BLOB_NAME} successfully.")