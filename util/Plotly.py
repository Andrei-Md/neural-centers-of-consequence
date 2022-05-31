import plotly.graph_objs as go
import plotly.io as pio  ## Open in Browser
# colors
import plotly.express as px
import matplotlib.colors as mcolors
import pandas as pd


def plot_coordinates_plotly(data,
                            data_source_name, title='',
                            browser=True):
    '''
    function to plot the coordinates
    :param data: the list of data_db dictionary
    :param data_source_name: data_db source name
    :param title: the plot title
    :param browser: True - render the plot in the browser
                    False - render the plot in the IDE
    :return: None
    '''
    if browser:
        pio.renderers.default = "browser"

    traces = create_trace(data)

    axis = dict(showbackground=False,
                showline=False,
                zeroline=False,
                showgrid=False,
                showticklabels=False,
                title=''
                )

    layout = go.Layout(
        title="Center Coordinates",
        width=1500,
        height=1500,
        showlegend=False,
        scene=dict(
            xaxis=dict(axis),
            yaxis=dict(axis),
            zaxis=dict(axis),
        ),
        margin=dict(
            t=100
        ),
        hovermode='closest',
        annotations=[
            dict(
                showarrow=False,
                text="Data source: " + data_source_name,
                xref='paper',
                yref='paper',
                x=0,
                y=0.1,
                xanchor='left',
                yanchor='bottom',
                font=dict(
                    size=14
                )
            )
        ],
        template='plotly_white'
    )

    data = traces
    fig = go.Figure(data=data, layout=layout, layout_title_text=title)
    fig.show()


def create_trace(data):
    '''
    function used to create trace
    :param data: list of dictionary containing coordinates Xn, Yz, Zn, colors and labels
                can also contain:
                 - line_color
                 - opacity
    :return: list of created traces
    '''
    traces = []
    for data_dict in data:
        Xn = data_dict['Xn']
        Yn = data_dict['Yn']
        Zn = data_dict['Zn']
        color_group = data_dict['colors']['color_group']
        labels = data_dict['labels']

        # opacity
        opacity = get_key_value(data_dict, key="opacity")

        # line color
        line_color = get_key_value(data_dict, key="line_color")
        if line_color is None:
            line_color = 'rgb(50,50,50)'

        traces.append(go.Scatter3d(x=Xn,
                                   y=Yn,
                                   z=Zn,
                                   mode='markers',
                                   name='coordinate',
                                   opacity=opacity,
                                   marker=dict(symbol='circle',
                                               size=6,
                                               color=color_group,
                                               # color=color_group_id,
                                               # colorscale='Viridis',
                                               line=dict(color=line_color, width=0.5)
                                               ),
                                   text=labels,
                                   hoverinfo='text'
                                   ))
    return traces


def get_key_value(data_dict, key):
    if key in data_dict:
        return data_dict[key]
    else:
        return None


def create_data(df, cols, grouping_col=None, labels_col_list=None,
                colors=None, check_nan=False, color_nan='#ebeded', nan_val='nan', **kwargs):
    '''
    function used to create data_db
    :param df: data_db frame
    :param grouping_col: grouping column for colors
    :param cols: dict containing the df column for X,Y and Z position
    :param labels_col_list: list of column used for labels
    :param colors: list of colors or a single color to use
    :param check_nan: check nan values: True - check nan value and assign them color_nan
                                        False - otherwise
    :param color_nan: color to assign to nan values
    :param kwargs: keyword args to add to data_db dict
    :return: the created data_db dict containing coordinates Xn, Yz, Zn, colors and labels
    '''

    if labels_col_list is None:
        labels_col_list = ['Broadman Area', 'index_col', 'Name']

    group_idx, no_colors = create_group_idx(df, grouping_col)

    if colors is None:
        if no_colors < len(px.colors.qualitative.Alphabet):
            colors = px.colors.qualitative.Alphabet[:no_colors]
        else:
            colors = mcolors.XKCD_COLORS[:no_colors]  # huge number of colors

    Xn = df[cols['x']].to_numpy()
    Yn = df[cols['y']].to_numpy()
    Zn = df[cols['z']].to_numpy()

    color_group = []
    labels = []

    # create the color list
    if type(colors) is list:
        for val in df[grouping_col].to_numpy():
            if check_nan:
                if (isinstance(val, str) and val == nan_val) or (pd.isna(val)):
                    color_group.append(color_nan)
                else:
                    color_group.append(colors[group_idx[str(val)]])
            else:
                color_group.append(colors[group_idx[str(val)]])
    else:
        color_group = colors

    # create the labels
    for val in df[labels_col_list].to_numpy():
        label_str = ''
        for cnt in range(len(labels_col_list)):
            label_str += str(labels_col_list[cnt]) + ": " + str(val[cnt]) + "; "
        labels.append(label_str[:-2])

    # data_db dict to return
    data_dict = dict(Xn=Xn, Yn=Yn, Zn=Zn,
                     colors=dict(color_group=color_group),
                     labels=labels)
    data_dict.update(kwargs)
    return data_dict


def create_group_idx(df, grouping_col):
    '''
    create a dictionary of unique elements from the grouping column and their unique index
    :param df: data_db frame
    :param grouping_col: the grouping column
    :return: the dictionary of unique elements from the grouping column and their unique index
    '''

    if grouping_col is not None:
        grouping_list = df[grouping_col].unique().tolist()
        group_idx = {str(x): grouping_list.index(x) for x in grouping_list}
        no_colors = len(grouping_list)
        return group_idx, no_colors
    else:
        return {}, 0
