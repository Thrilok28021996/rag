from sentence_transformers import CrossEncoder, SentenceTransformer
from sentence_transformers.util import cos_sim
from transformers import pipeline


def context_relevancy(query, answer):
    cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
    relevancy_score = cross_encoder.predict([query, answer])
    print(f" The context relevancy score is: {relevancy_score}")
    return relevancy_score


def faithfulness(context, answer):
    nli_model = pipeline("text-classification", model="roberta-large-mnli")
    faithfulness_check = nli_model(f"{context}</s></s> {answer}")
    print(f" the faithfulness check is: {faithfulness_check}")
    return faithfulness_check


def answer_relevancy(goldenanswer, generatedanswer):
    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings1 = embedder.encode(goldenanswer)
    embeddings2 = embedder.encode(generatedanswer)
    similarity = cos_sim(embeddings1, embeddings2)
    print(f" The answer relevancy is {similarity}")
    return similarity
