from dataclasses import dataclass


@dataclass(frozen=True)
class Token:
    type: str
    value: str


def lex(source: str) -> list[Token]:
    """Very small lexer for `let <name> = <number>;` ZerdCore örneği."""
    source = source.replace(";", " ; ").replace("=", " = ")
    parts = [p for p in source.split() if p]

    tokens: list[Token] = []
    for part in parts:
        if part == "let":
            tokens.append(Token("LET", part))
        elif part == "=":
            tokens.append(Token("EQUAL", part))
        elif part == ";":
            tokens.append(Token("SEMICOLON", part))
        elif part.isdigit():
            tokens.append(Token("NUMBER", part))
        else:
            tokens.append(Token("IDENT", part))
    return tokens


def parse(tokens: list[Token]) -> dict:
    """Parses: let <IDENT> = <NUMBER>;"""
    assert [t.type for t in tokens] == ["LET", "IDENT", "EQUAL", "NUMBER", "SEMICOLON"]
    return {
        "type": "Program",
        "body": [
            {
                "type": "VariableDeclaration",
                "identifier": tokens[1].value,
                "value": {
                    "type": "NumberLiteral",
                    "value": int(tokens[3].value),
                },
            }
        ],
    }


def test_zerdcore_lexer_parser_pipeline_returns_expected_ast() -> None:
    source = "let enerji = 42;"

    tokens = lex(source)
    ast = parse(tokens)

    expected_ast = {
        "type": "Program",
        "body": [
            {
                "type": "VariableDeclaration",
                "identifier": "enerji",
                "value": {
                    "type": "NumberLiteral",
                    "value": 42,
                },
            }
        ],
    }

    assert ast == expected_ast
