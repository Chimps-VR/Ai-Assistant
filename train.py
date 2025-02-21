from chat_gen import *

import os

if __name__ == "__main__":

    # Define some paths
    assistantName = input("Assistant Name: ")
    assistantFolder = os.path.join(os.getcwd(), "/assistants/", "/"+assistantName+"/")

    # Create assistant folder if it does not exist
    if not os.path.exists(assistantFolder):
        os.mkdir(assistantFolder)
    
    # Define some more paths
    modelDirectory = os.path.join(assistantFolder, 'checkpoint/', input("Checkpoint Name: "))
    csvPath = os.path.join(modelDirectory, 'train.csv')

    # Exit if training data doesn't exist
    if not os.path.exists(csvPath):
        raise Exception(f"File {csvPath} does not exist, this is required as you need training data to train a model!")
        exit()

    # Prepare the model arguments
    args = create_args(
        num_epochs=3,
        batch_size=4,
        learning_rate=3e-5,
        save_every=1000,
        max_length=512,
        temperature=0.8,
        top_k=60,
        top_p=0.92,
        repetition_penalty=1.2
    )

    # Train the model with the training data
    train_model(modelDirectory, csvPath, args)
