import plotly.graph_objects as go
import networkx as nx

def create_timeline_graph(G):
    if not G or G.number_of_nodes() == 0:
        return go.Figure().update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', xaxis=dict(visible=False), yaxis=dict(visible=False))

    pos = nx.circular_layout(G)
    
    edge_x, edge_y = [], []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(x=edge_x, y=edge_y, line=dict(width=0.7, color='#444'), hoverinfo='none', mode='lines')

    node_x, node_y, node_text, node_color, node_size = [], [], [], [], []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        
        # Display short labels for notes to avoid clumsiness
        if G.nodes[node].get('type') == 'note':
            node_text.append(f"Note {node}")
            node_color.append('#00ffa3')
            node_size.append(12)
        else:
            node_text.append(node)
            node_color.append('#7f77dd')
            node_size.append(18)

    node_trace = go.Scatter(
        x=node_x, y=node_y, mode='markers+text', text=node_text,
        textposition="top center", marker=dict(color=node_color, size=node_size, line=dict(width=1, color='white'))
    )

    return go.Figure(data=[edge_trace, node_trace], layout=go.Layout(
        showlegend=False, template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(b=0, l=0, r=0, t=0), xaxis=dict(visible=False), yaxis=dict(visible=False)
    ))