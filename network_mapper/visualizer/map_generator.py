from pyvis.network import Network
from config import HTML_OUTPUT


def generate_html(graph, devices):
    """
    Генерирует HTML-файл с визуализацией карты сети.
    """
    print("[HTML] Генерация HTML-карты сети...")

    net = Network(height="800px", width="100%", directed=False)
    net.barnes_hut()
    lis = []

    # Цвета по типу устройства
    type_colors = {
        "workstation": "#888888",
        "server": "#FFD700",
        "router": "#1E90FF",
        "printer": "#228B22",
        "camera": "#FF69B4",
        "phone": "#00CED1",
        "unknown": "#AAAAAA"
    }

    for node in graph.nodes(data=True):
        ip = node[0]
        attrs = node[1]

        # Попробуем вручную определить роутер
        label = attrs.get("label", ip)
        dev_type = attrs.get("type", "unknown")


        if ip == "192.168.0.1" or "tp-link" in label.lower():
            dev_type = "router"
            attrs["type"] = dev_type
            attrs["color"] = "#008000"

        net.add_node(
            ip,
            label=label,
            color=attrs.get("color", "#888888"),
            title=f"{label}\nТип: {dev_type}"
        )
    print("[DEBUG] Рёбра графа:")
    for edge in graph.edges():
        print(edge)
    for source, target in graph.edges():
        net.add_edge(source, target, width=2, hidden=False)
    if len(lis) >= 2:
        net.add_edge(lis[0], lis[1], width=2, hidden=False)

    net.set_options("""
    {
      "nodes": {
        "shape": "dot",
        "size": 16,
        "font": {
          "size": 14,
          "color": "#000000"
        },
        "borderWidth": 2
      },
      "edges": {
        "width": 2,
        "color": {
          "color": "#cccccc"
        },
        "arrows": {
          "to": {
            "enabled": false
          }
        }
      },
      "physics": {
        "stabilization": false
      }
    }
    """)

    # net.show_buttons(filter_=['physics'])
    net.save_graph(HTML_OUTPUT)
    print(f"[HTML] Карта сети сохранена: {HTML_OUTPUT}")