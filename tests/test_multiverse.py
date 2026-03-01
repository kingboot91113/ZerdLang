from pathlib import Path

from zerdlang_parser import extract_code_block, assert_nested_blocks_closed


def test_multiverse_example_has_closed_nested_blocks():
    source = Path("KitapGiris.md").read_text(encoding="utf-8")
    multiverse_block = extract_code_block(source, "DEFINE multiverse AS {")

    # Includes nested `collision => { ... }` and inline `IF ... THEN share(...)`.
    assert_nested_blocks_closed(multiverse_block)
