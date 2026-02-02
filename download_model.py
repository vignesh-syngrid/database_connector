from transformers import pipeline
print("Downloading model...")
llm = pipeline(
    "text2text-generation",
    model="google/flan-t5-base"
)
print("Model downloaded successfully!")