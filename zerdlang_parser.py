from __future__ import annotations


def extract_code_block(source: str, block_start: str) -> str:
    start_index = source.find(block_start)
    if start_index == -1:
        raise ValueError(f"Could not find block start: {block_start!r}")

    open_brace_index = source.find("{", start_index)
    if open_brace_index == -1:
        raise ValueError(f"Block start does not contain an opening brace: {block_start!r}")

    depth = 0
    for i in range(open_brace_index, len(source)):
        char = source[i]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return source[start_index : i + 1]
            if depth < 0:
                raise AssertionError("Encountered unmatched closing brace while extracting block.")

    raise AssertionError("Block was not fully closed.")


def assert_nested_blocks_closed(code: str) -> None:
    brace_depth = 0

    for char in code:
        if char == "{":
            brace_depth += 1
        elif char == "}":
            brace_depth -= 1
            if brace_depth < 0:
                raise AssertionError("Found a closing brace without a matching opening brace.")

    if brace_depth != 0:
        raise AssertionError("One or more nested blocks are not closed.")

    # Validate inline IF closures in a minimal way for the Zerdlang examples.
    # `IF ... THEN { ... }` is covered by brace checks; this ensures
    # `IF ... THEN action(...);` also terminates cleanly.
    lines = code.splitlines()
    for idx, line in enumerate(lines):
        stripped = line.strip()
        if not stripped.startswith("IF "):
            continue

        if " THEN" not in stripped:
            raise AssertionError(f"IF statement is missing THEN: {stripped}")

        then_fragment = stripped.split("THEN", maxsplit=1)[1].strip()
        if not then_fragment:
            if idx + 1 >= len(lines):
                raise AssertionError(
                    f"IF statement has no body after THEN: {stripped}"
                )
            then_fragment = lines[idx + 1].strip()

        if then_fragment.startswith("{"):
            continue

        if not then_fragment.endswith(";"):
            raise AssertionError(
                f"Inline IF body must end with ';' to be considered closed: {stripped}"
            )
