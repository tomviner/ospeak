from ospeak.splitter import text_splitter


def test_default_separators():
    text = "Hello\n\nWorld\nHow are you?"
    result = text_splitter(text, chunk_size=12)
    expected = ["Hello", "World", "How are you?"]
    assert result == expected


def test_custom_separators():
    text = "apple,banana;cherry"
    result = text_splitter(text, separators=[",", ";"], chunk_size=12)
    expected = ["apple,", "banana;", "cherry"]
    assert result == expected


def test_empty_text():
    text = ""
    result = text_splitter(text)
    expected = []
    assert result == expected


def test_no_splits():
    text = "HelloWorld"
    result = text_splitter(text, separators=[","])
    expected = ["HelloWorld"]
    assert result == expected


def test_split_sentences_short_first():
    text = (
        "Sure. This is a long text that should be split into smaller chunks based"
        " on the specified chunk size."
    )
    result = text_splitter(text, chunk_size=20)
    assert result == [
        'Sure.',
        'This is a long text',
        'that should be',
        'split into smaller',
        'chunks based on the',
        'specified chunk',
        'size.',
    ]


def test_split_sentences_short_second():
    text = (
        "This is a long text that should be split into smaller chunks based"
        " on the specified chunk size. Sure."
    )
    result = text_splitter(text, chunk_size=20)
    assert result == [
        'This is a long text',
        'that should be',
        'split into smaller',
        'chunks based on the',
        'specified chunk',
        'size. Sure.',
    ]


def test_multiple_separators():
    text = "Hello,World;How:are you?"
    result = text_splitter(text, separators=[",", ";", ":"], chunk_size=8)
    expected = ["Hello,", "World;", "How:", "are you?"]
    assert result == expected


def test_nested_splitting():
    text = "Chapter 1\n\nParagraph 1.\nParagraph 2.\n\nChapter 2\n\nParagraph 3."
    result = text_splitter(text, chunk_size=20)
    expected = [
        "Chapter 1",
        "Paragraph 1.",
        "Paragraph 2.",
        "Chapter 2",
        "Paragraph 3.",
    ]
    assert result == expected
