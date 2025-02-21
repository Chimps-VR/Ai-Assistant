from chat_gen import *
import os

if __name__ == "__main__":
    # Define Variables
    modelDirectory = 'checkpoint/run1'
    csvPath = os.path.join(modelDirectory, 'cleaned.csv')

    # Prepare the CSV data
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

    # Train the model
    train_model(modelDirectory, csvDath, args)

