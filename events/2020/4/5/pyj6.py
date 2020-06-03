for token, vector in pipe(
    stream_file("harry_potter.txt"),
    tokenize(),
    duplicate(4),
    (None, one_hot(), tfidf(), glove()),
    (None, zero_center(), None, None),
    concat_vectors(),
):
    pass
