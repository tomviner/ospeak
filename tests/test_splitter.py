from ospeak.splitter import text_splitter, SEPARATORS
import hypothesis.strategies as st
from hypothesis import given, example


def test_default_separators():
    text = "Hello\n\nWorld\nHow are you?"
    result = text_splitter(text, chunk_size=12)
    expected = ["Hello\n\n", "World\n", "How are you?"]
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
    text = "Short. A medium sentence going next. And a final sentence."
    result = text_splitter(text, chunk_size=21)
    assert result == [
        "Short. ",
        "A medium sentence ",
        "going next. ",
        "And a final sentence.",
    ]


def test_split_sentences_short_second():
    text = "A medium sentence going first. And a next sentence. Short. "
    result = text_splitter(text, chunk_size=21)
    assert result == [
        "A medium sentence ",
        "going first. ",
        "And a next sentence. ",
        "Short. ",
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
        "Chapter 1\n\n",
        "Paragraph 1.\n",
        "Paragraph 2.\n\n",
        "Chapter 2\n\n",
        "Paragraph 3.",
    ]
    assert result == expected
    assert "".join(result) == text


@given(
    text=st.text(min_size=0, max_size=1000),
    chunk_size=st.integers(min_value=1, max_value=100),
)
@example("Hello\n\nWorld\nHow are you?", 12)
def test_split_roundtrip(text, chunk_size):
    result = text_splitter(text, chunk_size=chunk_size)
    assert "".join(result) == text
    max_sep_len = 2
    for chunk in result:
        within_chunk_size = len(chunk) <= chunk_size
        contains_separator = any(sep in chunk[:-1] for sep in SEPARATORS)
        assert (
            within_chunk_size or not contains_separator
        ), f"chunk: {chunk!r}, chunk_size: {chunk_size}, result: {result!r}"
