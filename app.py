from flask import Flask, render_template, request, send_file, jsonify, redirect, url_for
import os, uuid
import io

from werkzeug.security import generate_password_hash
import mimetypes #we need mimetypes for retrieving image files from blob
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure.cosmos import CosmosClient, PartitionKey
import datetime

app = Flask(__name__)







# Initialize Azure Storage Blob and Cosmos DB clients

# Define your Logic App endpoint for CRUD operations

# Define your Azure SQL Database connection

# Define your Cosmos DB connection


# Azure Storage Account information
account_name = "imageresourceskaveen"
account_key = "C5oPnNOaxcRPnvsKV6MpJ+LaMh3wwzRhrDMn2hlnNDQCWoCjGQQgs7juE5iF4cVk6ORqSyi9EaxH+AStzHrsiA=="
container_name = "userimage"



image_urls = [
    "https://imageresourceskaveen.blob.core.windows.net/userimage"
]






# Initialize Cosmos DB client
cosmos_client = CosmosClient("https://useruploads.documents.azure.com:443/", credential="9JxxLWYur0NSzFqKE201uuAk2gBegpm6ah1i1o9IS6uaLicgA9wfGpIz3mHnO3GpCkKRLS5rtW6MACDb6bwMWA==")

# Reference to my database
database = cosmos_client.create_database_if_not_exists("UserinfoDB")

# Reference to my container
container_definition = {
    "id": "usermediadata",   
}
# Define the partition key
partition_key = PartitionKey(path="/username")
# Create a PartitionKey instance
#partition_key = PartitionKey(path="/username")
container = database.create_container_if_not_exists(container_definition, offer_throughput=400, partition_key=partition_key) #, partition_key=partition_key)

# Create a JSON document based on the schema
"""image_data = {
    "id": "unique-document-id",
    "username": "user123",
    "imageTitle": "Nature Pic",
    "imageUrl": "https://imageresourceskaveen.blob.core.windows.net/userimage/images/Screenshot (10).png",
    "tags": ["girl", "beautiful"],
    "uploadDate": datetime.datetime.utcnow().isoformat()
}
"""

@app.route('/')
def index():
    return render_template('index.html')
   



@app.route('/home.html')
def home():
    # Fetch the list of blobs from the container
    blob_service_client = BlobServiceClient(account_url=f"https://{account_name}.blob.core.windows.net", credential=account_key)
    container_client = blob_service_client.get_container_client(container_name)
    blobs = container_client.list_blobs()

    # Create a list of image URLs to pass to the template
    #image_urls = [f"/get_image/{blob.name}" for blob in blobs]
    image_urls = [url_for('get_image_urls_from_cosmos_db', blob_name=blob.name) for blob in blobs]
    return render_template('home.html', image_urls=image_urls)


@app.route('/upload', methods=['POST'])
def upload():
    username = request.form['username']
    image_title = request.form['imageTitle']

    # Handle file upload
    image_file = request.files['imageFile']
    if image_file and allowed_file(image_file.filename):    
        image_url = save_image_to_blob_storage(image_file)


        # Save metadata to Cosmos DB
        image_data = {
            "id": str(datetime.datetime.utcnow().timestamp()),  # Generate a unique ID
            "username": username,
            "imageTitle": image_title,
            "imageUrl": image_url,
            "uploadDate": datetime.datetime.utcnow().isoformat()
        }
        container.create_item(body=image_data)
        return redirect(url_for('home'))    
    return "invalid file", 400



def save_image_to_blob_storage(image_file):
    try:
        if image_file:
            blob_service_client = BlobServiceClient(account_url=f"https://{account_name}.blob.core.windows.net", credential=account_key)
            container_client = blob_service_client.get_container_client(container_name)
            
            blob_name = os.path.join("images", image_file.filename)
            blob_client = container_client.get_blob_client(blob_name)

            blob_client.upload_blob(image_file)
            return "Image uploaded successfully", 200
           
        else:
            return "No file provided", 400
    except Exception as e:
        return str(e), 500

    






    

def get_blob_content(account_name, account_key, container_name, blob_name):
    blob_service_client = BlobServiceClient(account_url=f"https://{account_name}.blob.core.windows.net", credential=account_key)
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(blob_name)
    
    try:
        blob_data = blob_client.download_blob()
        content = blob_data.readall()
        return content
    except Exception as e:
        return str(e)
    

 # Implement media file upload logic
    # Save metadata to Cosmos DB
    # Save media file to Blob Storage






@app.route('/get_image/<path:blob_name>')
def get_image_urls_from_cosmos_db(blob_name):
    content = get_blob_content(account_name, account_key, container_name, blob_name)
    if content:
        mime_type, _ = mimetypes.guess_type(blob_name)
        return send_file(io.BytesIO(content), mimetype=mime_type)
    else:
        return "Image not found", 404





# Implement this function to check if the file type is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png', 'gif'}

# Add CRUD endpoints for asset records using Logic Apps


if __name__ == '__main__':
    app.run(debug=True)
