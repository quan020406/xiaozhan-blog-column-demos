from __future__ import annotations


def build_langchain_agent():
    """Optional migration placeholder for LangChain tools and model binding."""
    try:
        from langchain_core.tools import tool
    except ImportError as exc:
        raise RuntimeError("Install LangChain before running this adapter.") from exc

    @tool
    def calculator(expression: str) -> str:
        """Evaluate a small arithmetic expression."""
        return str(eval(expression, {"__builtins__": {}}, {}))

    return [calculator]


if __name__ == "__main__":
    tools = build_langchain_agent()
    print([tool.name for tool in tools])

