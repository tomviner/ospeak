from typing import List, Optional

SEPARATORS = ["\n\n", "\n", ". ", " "]


def text_splitter(
    text: str,
    separators: Optional[List[str]] = None,
    chunk_size: int = 1000,
) -> List[str]:
    separators = separators or SEPARATORS

    return list(recursive_split(text, separators, chunk_size))


def recursive_split(text: str, separators: List[str], chunk_size: int):
    if not separators:
        yield text
        return

    separator = separators[0]
    chunks = split_text(text, separator)
    current_chunk = ""

    for chunk in chunks:
        # If adding chunk would exceed size limit, yield what we have
        if current_chunk and len(current_chunk) + len(chunk) > chunk_size:
            yield current_chunk
            current_chunk = ""

        # Recursively split the chunk
        for sub_chunk in recursive_split(chunk, separators[1:], chunk_size):
            if len(current_chunk) + len(sub_chunk) > chunk_size:
                yield current_chunk
                current_chunk = ""
            current_chunk += sub_chunk

    if current_chunk:
        yield current_chunk


def split_text(text: str, separator: str) -> List[str]:
    chunks = text.split(separator)
    return [
        chunk + (separator if i < len(chunks) else "")
        for i, chunk in enumerate(chunks, 1)
    ]
