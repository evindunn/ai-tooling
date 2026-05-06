
import base64
import dataclasses
import os
import pathlib


_MAX_FILE_CHARACTERS = 12_000


@dataclasses.dataclass(frozen=True)
class FileSummary:
    """
    Summarized file content and metadata.

    :param mime_type: MIME type describing the summarized content.
    :param content_encoding: Optional encoding name applied to ``content``.
    :param truncated: Whether the summarized content was truncated.
    :param size_bytes: Original file size in bytes.
    :param content: Text content or an encoded representation of binary data.
    """

    mime_type: str
    content_encoding: str | None
    truncated: bool
    size_bytes: int
    content: str


def iter_directory_entries(target: pathlib.Path) -> list[tuple[pathlib.Path, list[str], list[str]]]:
    """
    Return the walked directory entries.

    :param target: Path to the directory to walk.
    :returns: Walk results as ``(root, dir_names, file_names)`` tuples.
    """
    path_walk = getattr(target, 'walk', None)
    if path_walk is not None:
        return list(path_walk())

    walk_entries: list[tuple[pathlib.Path, list[str], list[str]]] = []
    for root, dir_names, file_names in os.walk(target):
        walk_entries.append((pathlib.Path(root), dir_names, file_names))
    return walk_entries


def read_file(file_path: pathlib.Path) -> FileSummary:
    """
    Read a file into a structured summary.

    :param file_path: File path to summarize.
    :returns: Structured file metadata and content.
    """
    f_size_bytes = file_path.stat().st_size

    with file_path.open('rb') as file:
        file_bytes = file.read(_MAX_FILE_CHARACTERS + 1)

    is_truncated = len(file_bytes) > _MAX_FILE_CHARACTERS
    file_bytes = file_bytes[:_MAX_FILE_CHARACTERS]

    try:
        file_text = file_bytes.decode('utf-8')
    except UnicodeDecodeError:
        return FileSummary(
            mime_type='application/octet-stream',
            content_encoding='base64',
            truncated=is_truncated,
            size_bytes=f_size_bytes,
            content=base64.b64encode(file_bytes).decode('ascii'),
        )

    return FileSummary(
        mime_type='text/plain',
        content_encoding=None,
        truncated=is_truncated,
        size_bytes=f_size_bytes,
        content=file_text,
    )
