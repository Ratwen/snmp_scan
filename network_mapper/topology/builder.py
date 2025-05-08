import networkx as nx
from config import COLOR_MAP

def build_topology(devices):
    """
    Строит граф сети с использованием networkx.
    Каждый узел содержит IP, hostname и тип устройства.
    Соединения пока простые: все устройства подключаются к главному маршрутизатору.
    """
    graph = nx.Graph()

    for device in devices:
        graph.add_node(
            device['ip'],
            label=f"{device['ip']}\n{device['hostname']}",
            type=device['type'],
            color=COLOR_MAP.get(device['type'], '#888888')
        )

    # Простая логика — все подключаются к первому маршрутизатору
    routers = [d for d in devices if d['type'] == 'router']
    if routers:
        main_router_ip = routers[0]['ip']
        for device in devices:
            if device['ip'] != main_router_ip:
                graph.add_edge(main_router_ip, device['ip'])

    return graph