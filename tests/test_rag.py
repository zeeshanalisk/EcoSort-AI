from rag import retrieve_guidance


queries = [
    "used lithium battery",
    "plastic bottle",
    "old laptop",
    "banana peel",
    "cardboard box",
]


for query in queries:
    print("\n==============================")
    print("QUERY:", query)
    print("==============================")

    for result in retrieve_guidance(query):
        print("\nSCORE:", round(result["score"], 3))
        print(result["text"])
