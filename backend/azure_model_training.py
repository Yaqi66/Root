import os
import time
import uuid

# Azure Cognitive Services for Custom Vision
from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training.models import (
    ImageFileCreateBatch,
    ImageFileCreateEntry,
)

# msrest
from msrest.authentication import ApiKeyCredentials

# 1) Retrieve environment variables (already set via setx or export)
ENDPOINT = os.environ["VISION_TRAINING_ENDPOINT"]
training_key = os.environ["VISION_TRAINING_KEY"]
prediction_key = os.environ["VISION_PREDICTION_KEY"]
prediction_resource_id = os.environ["VISION_PREDICTION_RESOURCE_ID"]

# 2) Authenticate
credentials = ApiKeyCredentials(in_headers={"Training-key": training_key})
trainer = CustomVisionTrainingClient(ENDPOINT, credentials)

prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)

# 3) Create a new Custom Vision project
project_name = str(uuid.uuid4())  # a random name for the project
print("Creating project with name:", project_name)
project = trainer.create_project(project_name)

# 4) Upload images from subfolders as tags
base_image_location = r"D:\Azure\archive\split_ttv_dataset_type_of_plants\Train_Set_Folder"

for folder_name in os.listdir(base_image_location):
    folder_path = os.path.join(base_image_location, folder_name)
    if os.path.isdir(folder_path):
        print(f"Processing folder: {folder_name}")

        # Create a tag in the project named after the folder
        tag = trainer.create_tag(project.id, folder_name)

        # Gather images in this folder
        image_entries = []
        for file_name in os.listdir(folder_path):
            if file_name.lower().endswith((".jpg", ".jpeg", ".png")):
                file_path = os.path.join(folder_path, file_name)
                with open(file_path, "rb") as image_data:
                    image_entries.append(
                        ImageFileCreateEntry(
                            name=file_name,
                            contents=image_data.read(),
                            tag_ids=[tag.id]
                        )
                    )

        # Upload in batches of up to 64
        BATCH_SIZE = 64
        for i in range(0, len(image_entries), BATCH_SIZE):
            batch = image_entries[i : i + BATCH_SIZE]
            upload_result = trainer.create_images_from_files(
                project.id,
                ImageFileCreateBatch(images=batch)
            )
            if not upload_result.is_batch_successful:
                print(f"Image batch upload failed for folder {folder_name}.")
                for image in upload_result.images:
                    print("Image status:", image.status)
            else:
                print(f"Uploaded batch of {len(batch)} images from '{folder_name}'.")

# 5) Train the project
print("Training...")
iteration = trainer.train_project(project.id)
while iteration.status != "Completed":
    iteration = trainer.get_iteration(project.id, iteration.id)
    print("Training status:", iteration.status)
    time.sleep(10)
print("Training completed.")

# 6) Publish the iteration
publish_iteration_name = "classifyModel"
trainer.publish_iteration(
    project.id, iteration.id, publish_iteration_name, prediction_resource_id
)
print("Published the trained model.")

# 7) Test the trained model
# Path to your test set folder (with subfolders like "aloevera", "banana", etc.)
test_base_image_location = r"D:\Azure\archive\split_ttv_dataset_type_of_plants\Test_Set_Folder"

# Loop over each subfolder in Test_Set_Folder
for folder_name in os.listdir(test_base_image_location):
    folder_path = os.path.join(test_base_image_location, folder_name)

    # Ensure it's a directory (not a file)
    if os.path.isdir(folder_path):
        print(f"Testing folder: {folder_name}")

        # Loop over each file in that folder
        for file_name in os.listdir(folder_path):
            if file_name.lower().endswith((".jpg", ".jpeg", ".png")):
                file_path = os.path.join(folder_path, file_name)

                # Open the image and send it to your published model for classification
                with open(file_path, "rb") as image_data:
                    results = predictor.classify_image(
                        project.id,
                        publish_iteration_name,
                        image_data.read()
                    )

                # Print out the results
                print(f"\nImage: {file_path}")
                for prediction in results.predictions:
                    print(f"  {prediction.tag_name}: {prediction.probability * 100:.2f}%")