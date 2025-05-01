"""
All plugins must implement the following interface:

def run(ioc: str) -> dict:
    return {
        "source": "plugin_name",
        "ioc": ioc,
        "result": "example result or data structure"
    }
"""
