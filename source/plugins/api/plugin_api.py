from typing import Protocol, Any

class GrazynaPlugin(Protocol):
    name: str
    version: str

    def run(self, context: dict[str, Any]) -> None:
        ...

def call_plugin(plugin: GrazynaPlugin, context: dict[str, Any]) -> None:
    print(f"[PLUGIN-API] Running {plugin.name} v{plugin.version}")
    plugin.run(context)
