if __name__ == "__main__":
    raise Exception("Oops, this is not supposed to be ran without an import!")
    exit()

from chat_gen import *

def loadAssistantModel(modelDirectory, max_length=512, temperature=0.8, top_k=60, top_p=0.92, repetition_penalty=1.2):
    model, tokenizer = load_model_and_tokenizer(modelDirectory)
    args = create_args(
            max_length=max_length,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
            repetition_penalty=repetition_penalty
        )
    return model, tokenizer, args
    
def promptText(question, model, tokenizer, args):
    response = generate_responses(model, tokenizer, question, args=args, clean_result=True)
    print(f"Prompt: {question}")
    print(f"Generated Response: {response}")