import dash
import plotly.graph_objects as go
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
from utils import fetchData

external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    title="YouTube Trending Videos Dashboard",
)

server = app.server
df = fetchData()


header = dbc.Row(
    dbc.Col(
        [
            html.Div(style={"height": 30}),
            html.H1("YouTube Trending Videos Dashboard", className="text-center"),
            html.H3("(2022)", className="text-center"),
        ]
    ),
    className="mb-4",
)

control_panel = dbc.Card(
    [
        html.H2("Filters"),
        dcc.Dropdown(
            id="date-dropdown",
            options=[
                {"label": "All Data", "value": "all"},
                {"label": "January", "value": "1"},
                {"label": "February", "value": "2"},
                {"label": "March", "value": "3"},
                {"label": "April", "value": "4"},
                {"label": "May", "value": "5"},
                {"label": "June", "value": "6"},
                {"label": "July", "value": "7"},
                {"label": "August", "value": "8"},
                {"label": "September", "value": "9"},
                {"label": "October", "value": "10"},
                {"label": "November", "value": "11"},
                {"label": "December", "value": "12"},
            ],
            value="all",
            placeholder="Date Range",
            searchable=True,
            multi=False,
        ),
        dcc.Dropdown(
            id="category-dropdown",
            options=[
                {"label": "All Categories", "value": "all"},
                {"label": "Film & Animation", "value": "Film & Animation"},
                {"label": "Autos & Vehicles", "value": "Autos & Vehicles"},
                {"label": "Music", "value": "Music"},
                {"label": "Pets & Animals", "value": "Pets & Animals"},
                {"label": "Sports", "value": "Sports"},
                {"label": "Short Movies", "value": "Short Movies"},
                {"label": "Travel & Events", "value": "Travel & Events"},
                {"label": "Gaming", "value": "Gaming"},
                {"label": "Videoblogging", "value": "Videoblogging"},
                {"label": "People & Blogs", "value": "People & Blogs"},
                {"label": "Comedy", "value": "Comedy"},
                {"label": "Entertainment", "value": "Entertainment"},
                {"label": "News & Politics", "value": "News & Politics"},
                {"label": "Howto & Style", "value": "Howto & Style"},
                {"label": "Education", "value": "Education"},
                {"label": "Science & Technology", "value": "Science & Technology"},
                {"label": "Movies", "value": "Movies"},
                {"label": "Anime/Animation", "value": "Anime/Animation"},
                {"label": "Action/Adventure", "value": "Action/Adventure"},
                {"label": "Classics", "value": "Classics"},
                {"label": "Comedy", "value": "Comedy"},
                {"label": "Documentary", "value": "Documentary"},
                {"label": "Drama", "value": "Drama"},
                {"label": "Family", "value": "Family"},
                {"label": "Foreign", "value": "Foreign"},
                {"label": "Horror", "value": "Horror"},
                {"label": "Sci-Fi/Fantasy", "value": "Sci-Fi/Fantasy"},
                {"label": "Thriller", "value": "Thriller"},
                {"label": "Shorts", "value": "Shorts"},
                {"label": "Shows", "value": "Shows"},
                {"label": "Trailers", "value": "Trailers"},
            ],
            value="all",
            placeholder="Select Category",
            searchable=True,
        ),
        # dcc.Dropdown(
        #     id="branch-select",
        #     placeholder="Select Branch",
        #     options=[
        #         {"label": "CSE", "value": "CSE"},
        #         {"label": "IT", "value": "IT"},
        #         {"label": "MAE", "value": "MAE"},
        #         {"label": "EEE", "value": "EEE"},
        #         {"label": "ECE", "value": "ECE"},
        #         {"label": "ITE", "value": "ITE"},  # New branch
        #         {"label": "ME", "value": "ME"},  # New branch
        #         {"label": "CST", "value": "CST"},  # New branch
        #         {"label": "CIV", "value": "CIV"},  # New branch
        #         {"label": "EE", "value": "EE"},  # New branch
        #         {"label": "ICE", "value": "ICE"},  # New branch
        #         {"label": "MET", "value": "MET"},  # New branch
        #         {"label": "TE", "value": "TE"},  # New branch
        #     ],
        #     value="CSE",
        #     searchable=False,
        # ),
        # dcc.Dropdown(
        #     id="column-select",
        #     placeholder="Select Subject",
        #     value="Percentage",
        #     searchable=False,
        #     optionHeight=70,
        # ),
    ],
    className="shadow-sm bg-light p-4 mb-2",
    style={"minWidth": "250px"},
    id="cross-filter-options",
)


kpi_container = dbc.CardDeck(
    [
        dbc.Card(
            [
                html.H3(children="{:,}".format(df.shape[0])),
                html.P("Records in Database (Total)"),
            ],
            className="p-4 mr-2 shadow-sm bg-light",
            id="total_records_card",
        ),
        dbc.Card(
            [html.H3(id="total_month_records"), html.P(id="total_month_records_text")],
            className="p-4 mr-2 shadow-sm bg-light",
            id="month_records_card",
        ),
        # dbc.Card(
        #     [
        #         html.H3(id="total_branch_records"),
        #         html.P(id="total_branch_records_text"),
        #     ],
        #     className="p-4 mr-2 shadow-sm bg-light",
        #     id="branch_records_card",
        # ),
    ]
)

app.layout = dbc.Container(
    [
        header,
        dbc.Row(
            [
                dbc.Col([control_panel,], width=3,),
                dbc.Col(
                    [
                        kpi_container,
                        dbc.Card(
                            dcc.Graph(
                                id="graph-1",
                                config={"displayModeBar": False, "responsive": True},
                            ),
                            className="my-4 mr-2 shadow-sm",
                        ),
                    ],
                    width=8,
                    style={"minWidth": "500px"},
                ),
            ],
        ),
        # dbc.Row(
        #     [
        #         dbc.Col(
        #             [
        #                 dbc.Card(
        #                     dcc.Graph(
        #                         id="graph-2",
        #                         config={"displayModeBar": False, "responsive": True},
        #                     ),
        #                     className="my-4 mr-2 shadow-sm",
        #                 ),
        #             ],
        #             width=8,
        #             style={"minWidth": "500px"},
        #         ),
        #     ],
        # ),
    ],
    fluid=True,
    className="bg-light",
)


def monthString(numberStr: str) -> str:
    reverse_map = {
        "all": "All Data",
        "1": "January",
        "2": "February",
        "3": "March",
        "4": "April",
        "5": "May",
        "6": "June",
        "7": "July",
        "8": "August",
        "9": "September",
        "10": "October",
        "11": "November",
        "12": "December",
    }
    return reverse_map[numberStr]


# Total Month records callbacks
@app.callback(
    [
        Output("total_month_records", "children"),
        Output("total_month_records_text", "children"),
    ],
    [
        Input(component_id="date-dropdown", component_property="value"),
        Input(component_id="category-dropdown", component_property="value"),
    ],
)
def update_total_month_records(dateRange, categoryChosen):

    if dateRange != "all" and categoryChosen != "all":
        date_mask = df.publishedAt.dt.month == int(dateRange)
        category_mask = df.category_name == categoryChosen
        month_records = df[date_mask & category_mask].shape[0]
    elif dateRange != "all" and categoryChosen == "all":
        date_mask = df.publishedAt.dt.month == int(dateRange)
        month_records = df[date_mask].shape[0]
    elif dateRange == "all" and categoryChosen != "all":
        category_mask = df.category_name == categoryChosen
        month_records = df[category_mask].shape[0]
    else:
        month_records = df.shape[0]
    return (
        "{:,}".format(month_records),
        "Videos in {} Date Range & {} Category".format(
            monthString(dateRange), categoryChosen
        ),
    )


# Graph Callbacks
@app.callback(
    Output(component_id="graph-1", component_property="figure"),
    [
        Input(component_id="date-dropdown", component_property="value"),
        Input(component_id="category-dropdown", component_property="value"),
    ],
)
def update_graph(dateRange, categoryChosen):

    try:
        if dateRange != "all" and categoryChosen != "all":
            date_mask = df.publishedAt.dt.month == int(dateRange)
            category_mask = df.category_name == categoryChosen
            filteredData = df[date_mask & category_mask]
        elif dateRange != "all" and categoryChosen == "all":
            date_mask = df.publishedAt.dt.month == int(dateRange)
            filteredData = df[date_mask]
        elif dateRange == "all" and categoryChosen != "all":
            category_mask = df.category_name == categoryChosen
            filteredData = df[category_mask]
        else:
            filteredData = df

        data = filteredData.publishedAt.dt.hour.value_counts()
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data.values,
                mode="markers",
                marker=dict(
                    size=20,
                    line_width=2,
                    color=data.values,
                    colorscale="Rainbow",
                    showscale=True,
                ),
            )
        )

        fig.update_layout(
            xaxis_tickangle=-45,
            font=dict(size=15),
            yaxis={"visible": True, "showticklabels": False, "showgrid": False},
            xaxis={"visible": True, "showgrid": False},
            xaxis_title="Hour of Day (24-hour clock)",
            yaxis_title="Number of Videos",
            template="simple_white",
            title={"text": "Publishing Trend"},
        )

        fig.update_layout(hovermode="x")
        fig.update_traces(hovertemplate="Hour: %{x}<br>Videos: %{y}<extra></extra>",)

        return fig

    except:
        graph = ""
        return graph


if __name__ == "__main__":
    app.run_server(debug=True)
