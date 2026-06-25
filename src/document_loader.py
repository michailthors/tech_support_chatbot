import pandas as pd

def load_twitter_data(filepath: str, max_pairs: int = 5000) -> list[dict]:
    """
    Reads twcs.csv and returns question-answer pairs.
    """
    df = pd.read_csv(filepath)

    # We only keep the columns we need
    df = df[['tweet_id', 'author_id', 'inbound', 'text', 'in_response_to_tweet_id']].copy()

    # We divide into inbound (customer inquiries) and outbound (outbound) companies.
    inbound = df[df['inbound'] == True].set_index('tweet_id')
    outbound = df[df['inbound'] == False].set_index('tweet_id')

    pairs = []

    for tweet_id, row in outbound.iterrows():
        response_to = row['in_response_to_tweet_id']

        if pd.isna(response_to):
            continue

        response_to = int(response_to)

        if response_to in inbound.index:
            question = inbound.loc[response_to, 'text']
            answer = row['text']

            # Clean-up from @mentions
            question = ' '.join(w for w in str(question).split() if not w.startswith('@'))
            answer = ' '.join(w for w in str(answer).split() if not w.startswith('@'))

            if len(question.strip()) > 10 and len(answer.strip()) > 10:
                pairs.append({
                    'question': question.strip(),
                    'answer': answer.strip(),
                    'company': row['author_id']
                })

        if len(pairs) >= max_pairs:
            break

    print(f"✅ Loaded {len(pairs)} pairs question-answer.")
    return pairs


if __name__ == "__main__":
    pairs = load_twitter_data('data/twcs.csv')
    print("\nExample:")
    for p in pairs[:2]:
        print(f"\nQuestion: {p['question']}")
        print(f"Answer: {p['answer']}")
        print(f"Company: {p['company']}")