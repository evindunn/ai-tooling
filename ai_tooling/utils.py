
import base64
import os
import pathlib


_MAX_FILE_CHARACTERS = 12_000


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


def read_file(file_path: pathlib.Path) -> str | dict[str, object]:
    """
    Read a file into a JSON-friendly value.

    :param file_path: File path to summarize.
    :returns: Full text content, truncated text content, or binary metadata.
    """
    with file_path.open('rb') as file:
        file_bytes = file.read(_MAX_FILE_CHARACTERS + 1)

    is_truncated = len(file_bytes) > _MAX_FILE_CHARACTERS

    try:
        file_text = file_bytes.decode('utf-8')
    except UnicodeDecodeError:
        return {
            'mime_type': 'application/octet-stream',
            'content_encoding': 'base64',
            'truncated': is_truncated,
            'size_bytes': len(file_bytes),
            'content': base64.b64encode(file_bytes).decode('ascii'),
        }

    return {
        'mime_type': 'text/plain',
        'content_encoding': None,
        'truncated': is_truncated,
        'size_characters': len(file_text),
        'content': file_text,
    }
