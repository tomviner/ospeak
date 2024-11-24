from typing import List, Optional


def text_splitter(
    text: str,
    separators: Optional[List[str]] = None,
    chunk_size: int = 1000,
) -> List[str]:
    separators = separators or ["\n\n", "\n", ". ", " "]

    result = recursive_split(text, separators, chunk_size)

    return [chunk.strip() for chunk in result]


def recursive_split(text: str, separators: List[str], chunk_size):
    if not separators:
        yield text
        return

    separator = separators[0]
    chunks = split_text(text, separator)

    current_chunk = ""

    for chunk in chunks:
        if len(current_chunk) + len(chunk) > chunk_size and current_chunk:
            yield current_chunk
            current_chunk = ""

        sub_chunks = recursive_split(chunk, separators[1:], chunk_size)
        for sub_chunk in sub_chunks:
            if len(current_chunk) + len(sub_chunk) > chunk_size and current_chunk:
                yield current_chunk
                current_chunk = ""
            current_chunk += sub_chunk

    if current_chunk:
        yield current_chunk


def split_text(text: str, separator: str) -> List[str]:
    chunks = text.split(separator)
    return [
        chunk.strip() + (separator if i < len(chunks) else '')
        for i, chunk in enumerate(chunks, 1)
        if chunk.strip()
    ]
