import pathlib

import clingo
import numpy as np
import pandas as pd

from py_arg_visualisation.functions.graph_data_functions.get_color import \
    get_color

PATH_TO_ENCODINGS = pathlib.Path(__file__).parent / 'encodings'


def generate_plain_dot_string(argumentation_framework, color_blind_mode=False):
    colored_node_df = get_node_properties(argumentation_framework,
                                          color_blind_mode)
    colored_edge_df = get_edge_properties(argumentation_framework,
                                          color_blind_mode)

    dot_string = "digraph {\n"
    dot_string += "    // Node defaults can be set here if needed\n"

    # Adding node information
    for index, row in colored_node_df.iterrows():
        node = f'    "{row["node"]}" [fontsize=14]\n'
        dot_string += node

    # Adding edge information
    dot_string += f'    edge[labeldistance=1.5 fontsize=12]\n'
    for index, row in colored_edge_df.iterrows():
        edge = f'"{row["source"]}" -> "{row["target"]}" ' \
               f'[dir="{row["direction"]}"]\n'
        dot_string += "    " + edge
    dot_string += "}"
    return dot_string


def generate_dot_strings(argumentation_framework, color_blind_mode=False):
    wfs_stb_pws, df_wfs_stb = node_stb_cal(argumentation_framework)
    dot_strings = []
    for pw in wfs_stb_pws:
        dot_strings.append(
            generate_dot_string(argumentation_framework, pw, color_blind_mode))
    return dot_strings


def generate_dot_string(
        argumentation_framework, model, color_blind_mode=False):
    colored_node_df = get_node_properties(argumentation_framework,
                                          color_blind_mode)
    colored_edge_df = get_edge_properties(argumentation_framework,
                                          color_blind_mode)

    node_color_col = model + "_color"
    edge_color_col = model + "_edge_color"
    dot_string = "digraph {\n"
    dot_string += "    // Node defaults can be set here if needed\n"

    # Adding node information
    for index, row in colored_node_df.iterrows():
        node = f'    "{row["node"]}" [style="filled" ' \
               f'fillcolor="{row[node_color_col]}" label="{row["label"]}" ' \
               f'fontsize=14]\n'
        dot_string += node

    dot_string += f'    edge[labeldistance=1.5 fontsize=12]\n'
    # Adding edge information
    for index, row in colored_edge_df.iterrows():
        if row["wfs_edge_color"] == "black":
            constraint = "constraint=false"
        else:
            constraint = ''
        color = (
            f'color="{row[edge_color_col]}:{row[edge_color_col]}"'
            if row[edge_color_col] != "black" and
               row["wfs_edge_color"] == "black"
            else f'color="{row[edge_color_col]}"'
        )

        if row[edge_color_col] == "black":
            edge_style = "dotted"
        else:
            edge_style = row["wfs_edge_style"]

        edge = f'"{row["source"]}" -> "{row["target"]}" [{color} ' \
               f'style="{edge_style}" dir="{row["direction"]}" ' \
               f'taillabel="{row["edge_label"]}" {constraint}]\n'
        dot_string += "    "+edge

    numeric_state_ids = pd.to_numeric(
        colored_node_df["state_id"], errors="coerce"
    ).dropna()
    min_state_id, max_state_id = \
        numeric_state_ids.min(), numeric_state_ids.max()
    if np.isnan(min_state_id) or np.isnan(max_state_id):
        dot_string += " "
    else:
        for state_id, group in colored_node_df.groupby("state_id"):
            if state_id == str(int(min_state_id)):
                rank_label = "max"
            elif state_id == str(int(max_state_id)):
                rank_label = "min"
            else:
                continue
            nodes_same_rank = " ".join(f"{node}" for node in group["node"])
            dot_string += f"    {{rank = {rank_label} {nodes_same_rank}}}\n"

    dot_string += "}"
    return dot_string


def read_edges(argumentation_framework):
    edges = []
    for defeat in argumentation_framework.defeats:
        start_node = defeat.from_argument.name
        end_node = defeat.to_argument.name
        edges.append((end_node, start_node, 'back'))
    edge_df = pd.DataFrame(edges, columns=["source", "target", "direction"])
    return edge_df


def get_edge_properties(argumentation_framework, color_blind_mode):
    """
    Process edge data to add color, style, and label based on node statuses.
    """

    wfs_stb_pws, df_wfs_stb = node_stb_cal(argumentation_framework)
    edge_df = read_edges(argumentation_framework)

    merged_df = edge_df.merge(
        df_wfs_stb,
        left_on="source",
        right_on="node",
        how="left",
        suffixes=("", "_source"),
    )
    merged_df = merged_df.merge(
        df_wfs_stb,
        left_on="target",
        right_on="node",
        how="left",
        suffixes=("_source", "_target"),
    )

    # For each status, apply get_edge_properties function and create the
    # color columns.
    for status in wfs_stb_pws:
        merged_df[f"{status}_edge_color"], \
            merged_df[f"{status}_edge_style"], _ = zip(
            *merged_df.apply(
                lambda row: get_edge_color(
                    row[f"{status}_source"], row[f"{status}_target"],
                    color_blind_mode),
                axis=1,
            )
        )

    merged_df["edge_label"] = merged_df.apply(
        lambda row: ""
        if row["wfs_edge_color"] == "black"
        else str(int(row["state_id_target"]) + 1)
        if can_be_number(row["state_id_target"])
        else row["state_id_target"],
        axis=1,
    )
    # Select the required columns for the final DataFrame.
    colored_edge_df = merged_df[
        ["source", "target", "direction", "edge_label"]
        + [f"{status}_edge_color" for status in wfs_stb_pws]
        + [f"{status}_edge_style" for status in wfs_stb_pws]
    ]
    return colored_edge_df


def get_edge_color(source_status, target_status, color_blind_mode):
    """Retrieve edge properties based on source and target statuses."""
    edge_color_dict_dict = {
        'defeated_accepted':
            {"color": get_color('red', color_blind_mode),
             "style": "solid",
             "show_label": True},
        'accepted_defeated':
            {"color": get_color('green', color_blind_mode),
             "style": "solid",
             "show_label": True},
        'undefined_undefined':
            {"color": get_color('yellow', color_blind_mode),
             "style": "solid",
             "show_label": True},
        'defeated_defeated':
            {"color": get_color('black', color_blind_mode),
             "style": "dashed",
             "show_label": False},
        'undefined_defeated':
            {"color": get_color('black', color_blind_mode),
             "style": "dashed",
             "show_label": False},
        'defeated_undefined':
            {"color": get_color('black', color_blind_mode),
             "style": "dashed",
             "show_label": False}
    }
    color_dict = edge_color_dict_dict[f'{source_status}_{target_status}']
    return color_dict['color'], color_dict['style'], color_dict['show_label']


def can_be_number(s):
    """Check if a string can be converted to a number."""
    try:
        float(s)  # try to convert to a float
        return True
    except ValueError:
        return False


def get_node_properties(argumentation_framework, color_blind_mode=False):
    wfs_stb_pws, df_wfs_stb = node_stb_cal(argumentation_framework)

    colored_node_df = df_wfs_stb.copy()

    for pw in wfs_stb_pws:
        if "pw" in pw:
            colored_node_df[pw + "_color"] = colored_node_df.apply(
                lambda row: get_color_for_row(row, pw, color_blind_mode),
                axis=1
            )
        else:
            colored_node_df[pw + "_color"] = colored_node_df.apply(
                lambda row: get_color_by_status(row[pw], color_blind_mode),
                axis=1
            )

    colored_node_df["label"] = colored_node_df.apply(
        lambda row: create_label(row), axis=1
    )

    return colored_node_df.sort_values(
        by=["state_id", "wfs"], ascending=[True, True]
    ).reset_index(drop=True)


def create_label(row, show_existential=False):
    try:
        row["node"] = int(row["node"])
        row["node"] = "p" + str(row["node"])
    except ValueError:
        pass

    if show_existential:
        exist_symbol = "∃"
        all_symbol = "∀"
    else:
        exist_symbol = ""
        all_symbol = ""
    if row["wfs"] == 'accepted':  # assuming 'status' key should be 'wfs'
        return f'{all_symbol} {row["node"]}.{row["state_id"]}'
    elif row["wfs"] == 'defeated':  # assuming 'status' key should be 'wfs'
        return f'{exist_symbol} {row["node"]}.{row["state_id"]}'
    else:
        return f'{row["node"]}.{row["state_id"]}'


def get_color_by_status(status, color_blind_mode):
    color_dict = {
        "accepted": get_color('green', color_blind_mode),
        "defeated": get_color('red', color_blind_mode),
        "undefined": get_color('yellow', color_blind_mode)}
    return color_dict[status]


def get_color_for_row(row, pw, color_blind_mode):
    color_dict = {
        "undefined_accepted": get_color('light-green', color_blind_mode),
        "undefined_defeated": get_color('light-red', color_blind_mode)}
    return color_dict[f"undefined_{row[pw]}"]


def node_wfs_cal(argumentation_framework):
    """function to calculate the state of the game."""
    ctl = clingo.Control()
    ctl.load(str(PATH_TO_ENCODINGS / 'grounded_encoding.dl'))
    for argument in argumentation_framework.arguments:
        ctl.add('base', [], f'pos({argument.name}).')
    for defeat in argumentation_framework.defeats:
        ctl.add('base', [], f'attack({defeat.from_argument.name}, '
                            f'{defeat.to_argument.name}).')
    ctl.ground([("base", [])])
    models = []
    ctl.solve(on_model=lambda m: models.append(m.symbols(shown=True)))
    atoms = models[0]
    nodes = []
    for atom in atoms:
        if atom.name == "fr" and atom.arguments[0] == 0:
            nodes.append((str(atom.arguments[1]), 0, 'accepted'))
        if atom.name == "len":
            if str(atom.arguments[0]) == 'undefined':
                nodes.append(
                    (str(atom.arguments[1]), "∞", str(atom.arguments[0])))
            else:
                nodes.append(
                    (
                        str(atom.arguments[1]),
                        str(atom.arguments[2]),
                        str(atom.arguments[0]),
                    )
                )
    node_wfs_df = pd.DataFrame(nodes, columns=["node", "state_id", "wfs"])
    node_wfs_df = node_wfs_df.sort_values(by="state_id")
    return node_wfs_df


def node_stb_cal(argumentation_framework):
    ctl = clingo.Control()
    ctl.configuration.solve.models = "0"
    ctl.load(str(PATH_TO_ENCODINGS / 'stable_encoding.dl'))
    for argument in argumentation_framework.arguments:
        ctl.add('base', [], f'pos({argument.name}).')
    for defeat in argumentation_framework.defeats:
        ctl.add('base', [], f'attack({defeat.from_argument.name}, '
                            f'{defeat.to_argument.name}).')
    ctl.ground([("base", [])])
    stb_output = []
    ctl.solve(on_model=lambda m: stb_output.append(m.symbols(shown=True)))
    nodes_status = {}
    pw_id = 1
    for model in stb_output:
        accepted_ls = []
        defeated_ls = []
        nodes_status[f"pw_{pw_id}"] = {}
        for atom in model:
            if atom.name == 'accepted':
                accepted_ls.append(str(atom.arguments[0]))
                nodes_status[f"pw_{pw_id}"]['accepted'] = accepted_ls
            elif atom.name == 'defeated':
                defeated_ls.append(str(atom.arguments[0]))
                nodes_status[f"pw_{pw_id}"]['defeated'] = defeated_ls
        pw_id = pw_id + 1
    node_wfs_df = node_wfs_cal(argumentation_framework)
    node_pws_df = add_multiple_pws_to_df(node_wfs_df, nodes_status)
    df_wfs_stb = node_pws_df.sort_values(
        by=["state_id", "wfs"], ascending=[True, True]
    ).reset_index(drop=True)
    wfs_stb_pws = list(nodes_status.keys())
    wfs_stb_pws.append("wfs")
    return wfs_stb_pws, df_wfs_stb


def add_multiple_pws_to_df(node_wfs_df, nodes_status):
    """Update a DataFrame with multiple possible worlds statuses."""
    for pw_key in nodes_status:
        node_wfs_df[pw_key] = node_wfs_df["node"].apply(
            lambda x: get_status(x, pw_key, nodes_status)
        )
    return node_wfs_df


def get_status(node, pw, nodes_status):
    """Retrieve status of a node in a given possible world."""
    for status, nodes in nodes_status[pw].items():
        if node in nodes:
            return status
    return None
