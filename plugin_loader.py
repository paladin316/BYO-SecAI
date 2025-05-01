import os
import importlib.util

PLUGIN_DIR = "plugins"

def discover_plugins():
    plugins = []
    for filename in os.listdir(PLUGIN_DIR):
        if filename.endswith(".py") and filename != "__init__.py":
            plugin_name = filename[:-3]
            plugins.append(plugin_name)
    return plugins

def load_plugin(plugin_name):
    plugin_path = os.path.join(PLUGIN_DIR, plugin_name + ".py")
    spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def run_all_plugins(ioc):
    results = {}
    for plugin_name in discover_plugins():
        try:
            plugin = load_plugin(plugin_name)
            if hasattr(plugin, "run"):
                results[plugin_name] = plugin.run(ioc)
            else:
                results[plugin_name] = {"error": "No 'run' function found"}
        except Exception as e:
            results[plugin_name] = {"error": str(e)}
    return results

if __name__ == "__main__":
    test_ioc = "8.8.8.8"
    output = run_all_plugins(test_ioc)
    for plugin, result in output.items():
        print(f"[{plugin}] -> {result}")
