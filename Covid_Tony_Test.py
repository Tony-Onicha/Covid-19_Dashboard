import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import us
from dash.dependencies import Input, Output
from dateutil import parser
import gunicorn

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# server = app.server

US_covid_deaths = pd.read_csv(
    "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv")

US_confirmed_cases = pd.read_csv(
    "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv")


# All states and territories
# function for daily US covid19 deaths
def get_US_daily_deaths(df):
    # We make a copy of the data frame to be able to delete unnecessary columns
    US_daily_deaths = df[df.Country_Region == "US"].copy()
    # We remove unnecessary columns
    US_daily_deaths.drop(
        ["UID", "iso2", "iso3", "code3", "FIPS", "Admin2", "Province_State", "Combined_Key", "Population", "Lat",
         "Long_"], axis=1, inplace=True)
    # We list all columns so we can summarize them
    cols = list(US_daily_deaths.columns)
    # Aggregate (sum) all columns
    US_daily_deaths = US_daily_deaths.groupby(["Country_Region"])[cols].sum()
    # reset index in the resulting dataframe
    US_daily_deaths = US_daily_deaths.reset_index()
    # Pivot all the date columns into rows
    US_daily_deaths = pd.melt(US_daily_deaths, id_vars=["Country_Region"], var_name="Date", value_name="Value")
    # do a difference of the value in a row with the one before it to undo the cumulative values
    US_daily_deaths["Daily_Deaths"] = US_daily_deaths["Value"].diff(1)
    return US_daily_deaths


# function for daily US confirmed covid19 cases
def get_US_daily_confirmed_cases(df):
    # We make a copy of the data frame to be able to delete unnecessary columns
    US_daily_confirmed_cases = df[df.Country_Region == "US"].copy()
    # We remove unnecessary columns
    US_daily_confirmed_cases.drop(
        ["UID", "iso2", "iso3", "code3", "FIPS", "Admin2", "Province_State", "Lat", "Long_", "Combined_Key"], axis=1,
        inplace=True)
    # We list all columns so we can summarize them
    cols = list(US_daily_confirmed_cases.columns)
    # Aggregate (sum) all columns
    US_daily_confirmed_cases = US_daily_confirmed_cases.groupby(["Country_Region"])[cols].sum()
    # reset index in the resulting dataframe
    US_daily_confirmed_cases = US_daily_confirmed_cases.reset_index()
    # Pivot all the date columns into rows
    US_daily_confirmed_cases = pd.melt(US_daily_confirmed_cases, id_vars=["Country_Region"], var_name="Date",
                                       value_name="Value")
    # do a difference of the value in a row with the one before it to undo the cumulative values
    US_daily_confirmed_cases["Daily_Confirmed_Cases"] = US_daily_confirmed_cases["Value"].diff(1)
    return US_daily_confirmed_cases


# function for US confirmed convid19 cases(cumulative)
def get_US_confirmed_cases(df):
    # We make a copy of the data frame to be able to delete unnecessary columns
    US_confirmed_cases = df[df.Country_Region == "US"].copy()
    # We remove unnecessary columns
    US_confirmed_cases.drop(
        ["UID", "iso2", "iso3", "code3", "FIPS", "Admin2", "Province_State", "Lat", "Long_", "Combined_Key"], axis=1,
        inplace=True)
    # We list all columns so we can summarize them
    cols = list(US_confirmed_cases.columns)
    # Aggregate (sum) all columns
    US_confirmed_cases = US_confirmed_cases.groupby(["Country_Region"])[cols].sum()
    # reset index in the resulting dataframe
    US_confirmed_cases = US_confirmed_cases.reset_index()
    # Pivot all the date columns into rows
    US_confirmed_cases = pd.melt(US_confirmed_cases, id_vars=["Country_Region"], var_name="Date",
                                 value_name="Confirmed_Cases")
    return US_confirmed_cases


# function for US covid19 deaths (cumulative)
def get_US_deaths(df):
    # We make a copy of the data frame to be able to delete unnecessary columns
    US_deaths = df[df.Country_Region == "US"].copy()
    # We remove unnecessary columns
    US_deaths.drop(
        ["UID", "iso2", "iso3", "code3", "FIPS", "Admin2", "Province_State", "Combined_Key", "Population", "Lat",
         "Long_"], axis=1, inplace=True)
    # We list all columns so we can summarize them
    cols = list(US_deaths.columns)
    # Aggregate (sum) all columns
    US_deaths = US_deaths.groupby(["Country_Region"])[cols].sum()
    # reset index in the resulting dataframe
    US_deaths = US_deaths.reset_index()
    # Pivot all the date columns into rows
    US_deaths = pd.melt(US_deaths, id_vars=["Country_Region"], var_name="Date", value_name="US_Deaths_Count")
    return US_deaths


# Individual states and territories
# state names and abbreviation
states_abbr = pd.DataFrame([[x, x.abbr] for x in us.states.STATES_AND_TERRITORIES],
                           columns=(["Province_State", "abbr"])).astype(str)

# territories with no counties
no_counties = ["American Samoa", "Guam", "Northern Mariana Islands", "Virgin Islands"]


# function for US state daily covid19 deaths
def get_US_state_daily_deaths(state, df):
    # We make a copy of the data frame to be able to delete unnecessary columns
    US_state_daily_deaths = df[df.Province_State == state].copy()
    # We remove unnecessary columns
    US_state_daily_deaths.drop(
        ["UID", "iso2", "iso3", "code3", "FIPS", "Admin2", "Country_Region", "Combined_Key", "Population", "Lat",
         "Long_"], axis=1, inplace=True)
    # We list all columns so we can summarize them
    cols = list(US_state_daily_deaths.columns)
    # Aggregate (sum) all columns
    US_state_daily_deaths = US_state_daily_deaths.groupby(["Province_State"])[cols].sum()
    # reset index in the resulting dataframe
    US_state_daily_deaths = US_state_daily_deaths.reset_index()
    # Pivot all the date columns into rows
    US_state_daily_deaths = pd.melt(US_state_daily_deaths, id_vars=["Province_State"], var_name="Date",
                                    value_name="Value")
    # do a difference of the value in a row with the one before it to undo the cumulative values
    US_state_daily_deaths["US_state_daily_deaths"] = US_state_daily_deaths["Value"].diff(1)
    return US_state_daily_deaths


# function for US state cumulative covid19 deaths
def get_US_state_deaths(state, df, county="None"):
    # We make a copy of the data frame to be able to delete unnecessary columns
    if state == 'US':
        US_state_deaths = df[df.Country_Region == 'US'].copy()
    else:
        US_state_deaths = df[df.Province_State == state].copy()

    if county == "None" or state in no_counties:
        # We remove unnecessary columns
        US_state_deaths.drop(
            ['UID', 'iso2', 'iso3', 'code3', 'FIPS', 'Admin2', 'Country_Region', 'Combined_Key', 'Population', 'Lat',
             'Long_'], axis=1, inplace=True)
        # We list all columns so we can summarize them
        cols = list(US_state_deaths.columns)
        # Aggregate (sum) all columns
        US_state_deaths = US_state_deaths.groupby(['Province_State'])[cols].sum()
        # reset index in the resulting dataframe
        US_state_deaths = US_state_deaths.reset_index()
        # Pivot all the date columns into rows
        US_state_deaths = pd.melt(US_state_deaths, id_vars=['Province_State'], var_name="Date",
                                  value_name="US_state_deaths")

    else:
        # We remove unnecessary columns
        US_state_deaths.drop(
            ['UID', 'iso2', 'iso3', 'code3', 'FIPS', 'Province_State', 'Country_Region', 'Combined_Key', 'Population',
             'Lat',
             'Long_'], axis=1, inplace=True)
        # We list all columns so we can summarize them
        cols = list(US_state_deaths.columns)
        # Aggregate (sum) all columns
        US_state_deaths = US_state_deaths.groupby(['Admin2'])[cols].sum()
        # reset index in the resulting dataframe
        US_state_deaths = US_state_deaths.reset_index()
        # Pivot all the date columns into rows
        US_state_deaths = pd.melt(US_state_deaths, id_vars=['Admin2'], var_name="Date",
                                  value_name="US_state_deaths")

    return US_state_deaths


# function for US state daily covid19 confirmed cases
def get_US_state_daily_confirmed_cases(state, df):
    # We make a copy of the data frame to be able to delete unnecessary columns
    US_state_daily_confirmed_cases = df[df.Province_State == state].copy()
    # We remove unnecessary columns
    US_state_daily_confirmed_cases.drop(
        ["UID", "iso2", "iso3", "code3", "FIPS", "Admin2", "Country_Region", "Lat", "Long_", "Combined_Key"], axis=1,
        inplace=True)
    # We list all columns so we can summarize them
    cols = list(US_state_daily_confirmed_cases.columns)
    # Aggregate (sum) all columns
    US_state_daily_confirmed_cases = US_state_daily_confirmed_cases.groupby(["Province_State"])[cols].sum()
    # reset index in the resulting dataframe
    US_state_daily_confirmed_cases = US_state_daily_confirmed_cases.reset_index()
    # Pivot all the date columns into rows
    US_state_daily_confirmed_cases = pd.melt(US_state_daily_confirmed_cases, id_vars=["Province_State"],
                                             var_name="Date", value_name="Value")
    # do a difference of the value in a row with the one before it to undo the cumulative values
    US_state_daily_confirmed_cases["US_state_daily_confirmed_cases"] = US_state_daily_confirmed_cases["Value"].diff(1)
    return US_state_daily_confirmed_cases


# function for US state and county cumulative covid19 confirmed cases
def get_US_state_confirmed_cases(state, df, county="None"):
    # We make a copy of the data frame to be able to delete unnecessary columns
    if state == 'US':
        US_state_confirmed_cases = df[df.Country_Region == 'US'].copy()
    else:
        US_state_confirmed_cases = df[df.Province_State == state].copy()
    if county == "None" or state in no_counties:
        # We remove unnecessary columns
        US_state_confirmed_cases.drop(
            ['UID', 'iso2', 'iso3', 'code3', 'FIPS', 'Admin2', 'Country_Region', 'Lat', 'Long_', 'Combined_Key'],
            axis=1,
            inplace=True)
        # We list all columns so we can summarize them
        cols = list(US_state_confirmed_cases.columns)
        # Aggregate (sum) all columns
        US_state_confirmed_cases = US_state_confirmed_cases.groupby(['Province_State'])[cols].sum()
        # reset index in the resulting dataframe
        US_state_confirmed_cases = US_state_confirmed_cases.reset_index()
        # Pivot all the date columns into rows
        US_state_confirmed_cases = pd.melt(US_state_confirmed_cases, id_vars=['Province_State'], var_name="Date",
                                           value_name="US_state_confirmed_cases")
    else:
        # We remove unnecessary columns
        US_state_confirmed_cases.drop(
            ['UID', 'iso2', 'iso3', 'code3', 'FIPS', 'Province_State', 'Country_Region', 'Lat', 'Long_',
             'Combined_Key'], axis=1,
            inplace=True)
        # We list all columns so we can summarize them
        cols = list(US_state_confirmed_cases.columns)
        # Aggregate (sum) all columns
        US_state_confirmed_cases = US_state_confirmed_cases.groupby(['Admin2'])[cols].sum()
        # reset index in the resulting dataframe
        US_state_confirmed_cases = US_state_confirmed_cases.reset_index()
        # Pivot all the date columns into rows
        US_state_confirmed_cases = pd.melt(US_state_confirmed_cases, id_vars=['Admin2'], var_name="Date",
                                           value_name="US_state_confirmed_cases")
    return US_state_confirmed_cases


# call functions to get daily and cumulative covid19 deaths in the US
Daily_deaths = get_US_daily_deaths(US_covid_deaths)
US_deaths = get_US_deaths(US_covid_deaths)

# call function to get daily and cumulative confirmed covid19 cases
Daily_confirmed_cases = get_US_daily_confirmed_cases(US_confirmed_cases)
US_Confirmed_cases = get_US_confirmed_cases(US_confirmed_cases)

# make df for the chloropleth
cplt_death = get_US_state_deaths("US", US_covid_deaths).groupby(["Province_State"]).max().reset_index()
cplt_confirmed_cases = get_US_state_confirmed_cases("US", US_confirmed_cases).groupby(
    ["Province_State"]).max().reset_index()
cplt_ = cplt_confirmed_cases.merge(cplt_death, how="left", on=["Province_State", "Date"])
cplt_data = cplt_.merge(states_abbr, how="left", on="Province_State")
cplt_data["text"] = cplt_data["Province_State"] + "<br>" + "Confirmed Cases: " + cplt_data[
    "US_state_confirmed_cases"].astype(str) + \
                    "<br>" + "Deaths: " + cplt_data["US_state_deaths"].astype(str)
territories = pd.DataFrame([[x, x.abbr] for x in us.states.STATES_AND_TERRITORIES],
                           columns=(["Province_State", "abbr"])).astype(str).sort_values(by="Province_State")
drpdn = territories["Province_State"]


# call function to get state from clickData
def get_state(code):
    state = list(cplt_data[cplt_data.abbr == code]["Province_State"])[0]
    return state


# variables for plots
# total cumulative US confirmed cases and deaths
total_US_confirmed = Daily_confirmed_cases.sum().iloc[-1]
total_US_deaths = Daily_deaths.sum().iloc[-1]
avg_US_state_confirmed = round(cplt_confirmed_cases["US_state_confirmed_cases"].mean(), 2)
avg_US_state_deaths = round(cplt_death["US_state_deaths"].mean(), 2)
states_max_c = cplt_confirmed_cases[
    cplt_confirmed_cases.US_state_confirmed_cases == cplt_confirmed_cases["US_state_confirmed_cases"].max()]
states_min_c = cplt_confirmed_cases[
    cplt_confirmed_cases.US_state_confirmed_cases == cplt_confirmed_cases["US_state_confirmed_cases"].min()]
states_max_d = cplt_death[cplt_death.US_state_deaths == cplt_death["US_state_deaths"].max()]
states_min_d = cplt_death[cplt_death.US_state_deaths == cplt_death["US_state_deaths"].min()]

fig_date = str(parser.parse(list(get_US_state_confirmed_cases("US", US_confirmed_cases)["Date"].tail(1))[0]).date())

# create and plot figures
daily_deaths_fig = px.bar(Daily_deaths, x="Date", y="Daily_Deaths", title="<b>Daily Covid Deaths in the USA</b>",
                          labels={"Daily_Deaths": """Number of Deaths (Daily Total)"""})
deaths_fig = px.bar(US_deaths, x="Date", y="US_Deaths_Count", title="<b>Cumulative Covid Deaths in the USA</b>",
                    labels={"US_Deaths_Count": """Number of Deaths (Running Total)"""})
daily_confirmed_fig = px.bar(Daily_confirmed_cases, x="Date", y="Daily_Confirmed_Cases",
                             title="<b>Daily Confirmed Covid Cases in the USA</b>",
                             labels={"Daily_Confirmed_Cases": """Number of New Cases (Daily Total)"""})
confirmed_fig = px.bar(US_Confirmed_cases, x="Date", y="Confirmed_Cases",
                       title="<b>Cumulative Confirmed Covid Cases in the USA</b>",
                       labels={"Confirmed_Cases": """Number of New Cases (Running Total)"""})
tab_style = {"fontWeight": "bold", "fontSize": "20px", "color": "black", "borderRadius": "25px", "textAlign": "center",
             "line-height": "5px"}
tab_selected_style = {"fontWeight": "bold", "fontSize": "20px", "color": "white", "borderRadius": "25px",
                      "line-height": "5px", "background": "rgb(190, 100, 200)", "textAlign": "center"}

# chloropleth map
df = cplt_data
df = df.reset_index()
locations = cplt_data["abbr"]

fig_clp = go.Figure(data=go.Choropleth(locations=locations,  # Spatial coordinates
                                       z=df["US_state_confirmed_cases"],  # Data to be color-coded
                                       locationmode="USA-states",  # set of locations match entries in `locations`
                                       #     hoverinfo = locations + z, #df["Province_State"],
                                       colorscale="Reds",  # "Plasma",# "Bluered",
                                       autocolorscale=False,
                                       text=df["text"],
                                       colorbar_title="Cumulative Total",
                                       )
                    )

fig_clp.update_layout(  # title_text="Covid19 Deaths in the USA",
    title_text="Click on a state on the map or select a state or territory from the dropdown list to view confirmed cases and deaths",
    geo=dict(scope="usa",  # limit map scope to USA
             projection=go.layout.geo.Projection(type="albers usa"),
             showlakes=True,
             lakecolor="rgb(255, 255, 255)"
             )
)

app.layout = html.Div(children=([
    html.Div(
        html.H1(children="Covid-19 Dashboard for the United States of America"),
        style={"textAlign": "center",
               "border": "5px black",
               "background": "rgb(190, 100, 200)",
               "borderRadius": "15px",
               "color": "white",
               "fontWeight": "bold"
               }
    ),
    # Total numbers
    html.Div([html.Div(html.H4("Covid-19 Summary as of {}".format(fig_date))),
              html.Div(html.H4("(All States and Territories inclusive)"),
                       style={"fontSize": "10px"}),
              html.Div(html.H4("Total Confirmed Cases: {}".format(total_US_confirmed)),
                       style={"width": "50%", "display": "inline-block"}),
              html.Div(html.H4("Total Deaths: {}".format(total_US_deaths)),
                       style={"width": "50%", "display": "inline-block"}),
              html.Div(html.H4("Avg Confirmed Cases in States: {}".format(avg_US_state_confirmed)),
                       style={"width": "50%", "display": "inline-block"}),
              html.Div(html.H4("Avg Deaths in States: {}".format(avg_US_state_deaths)),
                       style={"width": "50%", "display": "inline-block"}),
              html.Div(html.H4("""Max Confirmed Cases: {} ({})""".format(list(states_max_c.Province_State)[0],
                                                                         list(states_max_c.US_state_confirmed_cases)[
                                                                             0])),
                       style={"width": "50%", "display": "inline-block"}),
              html.Div(html.H4("""Max Deaths: {} ({})""".format(list(states_max_d.Province_State)[0],
                                                                list(states_max_d.US_state_deaths)[0])),
                       style={"width": "50%", "display": "inline-block"}),
              html.Div(html.H4("""Min Confirmed Cases: {} ({})""".format(list(states_min_c.Province_State)[0],
                                                                         list(states_min_c.US_state_confirmed_cases)[
                                                                             0])),
                       style={"width": "50%", "display": "inline-block"}),
              html.Div(html.H4("""Min Deaths: {} ({})""".format(list(states_min_d.Province_State)[0],
                                                                list(states_min_d.US_state_deaths)[0])),
                       style={"width": "50%", "display": "inline-block"})
              ],
             style={"textAlign": "center",
                    "border": "5px black",
                    "background": "rgb(215, 100, 200)",
                    "borderRadius": "25px",
                    "color": "white",
                    "fontWeight": "bold"}
             ),
    html.Br(),

    # confirmed cases tabs
    html.Div([
        html.Div([dcc.Tabs(id="confirmed_tabs",
                           value="tab-1",
                           children=[dcc.Tab(label="Daily",
                                             value="tab-1",
                                             style=tab_style,
                                             selected_style=tab_selected_style
                                             ),
                                     dcc.Tab(label="Running Total",
                                             value="tab-2",
                                             style=tab_style,
                                             selected_style=tab_selected_style
                                             )],
                           ),
                  dcc.Graph(id="confirmed_cases"),
                  ], style={"width": "50%", "display": "inline-block", "borderRadius": "25px",
                            "borderBottom": "1px solid rgb(214, 214, 214)"}
                 ),

        # deaths tabs
        html.Div([dcc.Tabs(id="death_tabs",
                           value="tab-1",
                           children=[dcc.Tab(label="Daily",
                                             value="tab-1",
                                             style=tab_style,
                                             selected_style=tab_selected_style
                                             ),
                                     dcc.Tab(label="Running Total",
                                             value="tab-2",
                                             style=tab_style,
                                             selected_style=tab_selected_style
                                             )],
                           ),
                  dcc.Graph(id="deaths")
                  ], style={"width": "50%", "display": "inline-block", "borderRadius": "25px",
                            "borderBottom": "1px solid rgb(214, 214, 214)"}
                 )
    ]),
    html.Br(),
    html.Br(),
    html.Br(),

    # US chloropleth map
    html.Div([html.H4(id="state_terr_header"),
              html.H4(id="selected_state_confirmed",
                      style={"width": "50%", "display": "inline-block"}
                      ),
              html.H4(id="selected_state_death",
                      style={"width": "50%", "display": "inline-block"}
                      ),
              html.H4(id="state_cnty_confirmed",
                      style={"width": "50%", "display": "inline-block"}
                      ),
              html.H4(id="state_cnty_deaths",
                      style={"width": "50%", "display": "inline-block"}
                      ),
              html.H4(id="county_max_c",
                      style={"width": "50%", "display": "inline-block"}
                      ),
              html.H4(id="county_max_d",
                      style={"width": "50%", "display": "inline-block"}
                      ),
              html.H4(id="county_min_c",
                      style={"width": "50%", "display": "inline-block"}
                      ),
              html.H4(id="county_min_d",
                      style={"width": "50%", "display": "inline-block"}
                      ),
              html.Footer(id="state_footer",
                          style={"width": "50%", "fontWeight": "normal", "fontSize": "15px"}
                          )
              ],
             style={"textAlign": "center", "width": "100%", "display": "inline-block", "fontSize": "25px",
                    "fontWeight": "bold", "border": "5px black", "background": "rgb(215, 100, 200)",
                    "borderRadius": "25px", "color": "white"
                    }),
    html.Div(dcc.Graph(id="chloro_graph",
                       figure=fig_clp)),

    # states and territories dropdown
    html.Div(dcc.Dropdown(id="territories",
                          options=[{"label": i, "value": i} for i in drpdn],
                          # value="US Territories"
                          searchable=True,
                          placeholder="Select a US State or Territory to display its Covid-19 data"
                          )),
    html.Br(),
    html.Div(dcc.RadioItems(id="states_and_territories")),
    html.Br(),
    html.Div([dcc.Tabs(id="state_confirmed_tabs",
                       value="tab-1",
                       children=[dcc.Tab(label="Daily",
                                         value="tab-1",
                                         style=tab_style,
                                         selected_style=tab_selected_style
                                         ),
                                 dcc.Tab(label="Running Total",
                                         value="tab-2",
                                         style=tab_style,
                                         selected_style=tab_selected_style)
                                 ]
                       ),
              dcc.Graph(id="state_confirmed")
              ], style={"width": "50%", "display": "inline-block", "borderRadius": "25px",
                        "borderBottom": "1px solid rgb(214, 214, 214)"}
             ),
    html.Div([dcc.Tabs(id="state_death_tabs",
                       value="tab-1",
                       children=[dcc.Tab(label="Daily",
                                         value="tab-1",
                                         style=tab_style,
                                         selected_style=tab_selected_style
                                         ),
                                 dcc.Tab(label="Running Total",
                                         value="tab-2",
                                         style=tab_style,
                                         selected_style=tab_selected_style)
                                 ]
                       ),
              dcc.Graph(id="state_death")
              ], style={"width": "50%", "display": "inline-block", "borderRadius": "25px",
                        "borderBottom": "1px solid rgb(214, 214, 214)"}
             ),
    html.Footer(id="data-source",
                children=[html.H6(dcc.Link("Data Source: JHU CSSE COVID-19 Dataset",
                                           href="https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series",
                                           target='_blank',
                                           style={"width": "50%", "display": "inline-block", "borderRadius": "25px",
                                                  "fontSize": "10px", "color": "black"}))
                          ]
                ),
]))


@app.callback(Output("confirmed_cases", "figure"),
              [Input("confirmed_tabs", "value")])
def render_confirmed(tab):
    if tab == "tab-1":
        figure = daily_confirmed_fig
        figure.update_xaxes(nticks=20)
        return figure
    elif tab == "tab-2":
        figure = confirmed_fig
        figure.update_xaxes(nticks=20)
        return figure


@app.callback(Output("deaths", "figure"),
              [Input("death_tabs", "value")])
def render_deaths(tab):
    if tab == "tab-1":
        figure = daily_deaths_fig
        figure.update_xaxes(nticks=20)
        return figure
    elif tab == "tab-2":
        figure = deaths_fig
        figure.update_xaxes(nticks=20)
        return figure


# chloropleth and dropdown state confirmed callbacks
@app.callback(Output("state_confirmed", "figure"),
              [Input("state_confirmed_tabs", "value"),
               Input("states_and_territories", "value")])
def display_click_data(tab, state):
    # state confirmed cases dfs
    Daily_state_confirmed = get_US_state_daily_confirmed_cases(state, US_confirmed_cases)
    US_state_confirmed = get_US_state_confirmed_cases(state, US_confirmed_cases)

    # state confirmed cases figs
    state_daily_confirmed_fig = px.bar(Daily_state_confirmed, x="Date", y="US_state_daily_confirmed_cases",
                                       title="<b>Daily Confirmed Covid Cases in {}</b>".format(state),
                                       labels={
                                           "US_state_daily_confirmed_cases": """Number of New Cases (Daily Total)"""})

    state_confirmed_fig = px.bar(US_state_confirmed, x="Date", y="US_state_confirmed_cases",
                                 title="<b>Confirmed Covid Cases in {}</b>".format(state),
                                 labels={"US_state_confirmed_cases": """Number of New Cases (Running Total)"""})

    if tab == "tab-1":
        figure = state_daily_confirmed_fig
        figure.update_xaxes(nticks=20)
        return figure
    else:
        tab == "tab-2"
        figure = state_confirmed_fig
        figure.update_xaxes(nticks=20)
        return figure

    return figure


@app.callback([Output("selected_state_confirmed", "children"),
               Output("selected_state_death", "children"),
               Output("state_terr_header", "children"),
               Output("state_cnty_confirmed", "children"),
               Output("state_cnty_deaths", "children"),
               Output("county_max_c", "children"),
               Output("county_min_c", "children"),
               Output("county_max_d", "children"),
               Output("county_min_d", "children"),
               Output("state_footer", "children")],
              [Input("states_and_territories", "value")])
def display_click_data(state):
    # state confirmed cases dfs
    state_confirmed = "Total Confirmed Cases: {} ".format(
        str(list(cplt_data[cplt_data.Province_State == state]["US_state_confirmed_cases"])[0]))
    state_deaths = "Total Deaths: {} ".format(
        str(list(cplt_data[cplt_data.Province_State == state]["US_state_deaths"])[0]))
    state_header = "Covid-19 Summary for {} as of {}".format(state, fig_date)
    if state in no_counties:
        county_avg_confirmed = "Avg Confirmed Cases in counties: **"
        county_avg_deaths = "Avg Deaths in counties: **"
        max_c = """Max Confirmed Cases: **"""
        min_c = """Min Confirmed Cases: **"""
        max_d = """Max Deaths: **"""
        min_d = """Min Deaths: **"""
        state_footer = """**County data not available"""
    else:
        county_confirmed = get_US_state_confirmed_cases(state, US_confirmed_cases, 'C').groupby(
            ['Admin2']).max().reset_index()
        county_avg_confirmed = "Avg Confirmed Cases in counties: {}".format(
            round(county_confirmed["US_state_confirmed_cases"].mean(), 2))
        county_deaths = get_US_state_deaths(state, US_covid_deaths, 'C').groupby(['Admin2']).max().reset_index()
        county_avg_deaths = "Avg Deaths in counties: {}".format(round(county_deaths["US_state_deaths"].mean(), 2))
        cnt_max_c = county_confirmed[
            county_confirmed.US_state_confirmed_cases == county_confirmed["US_state_confirmed_cases"].max()]
        cnt_min_c = county_confirmed[
            county_confirmed.US_state_confirmed_cases == county_confirmed["US_state_confirmed_cases"].min()]
        max_c = """Max Confirmed Cases: {} ({})""".format(list(cnt_max_c.Admin2)[0],
                                                          list(cnt_max_c.US_state_confirmed_cases)[0])
        min_c = """Min Confirmed Cases: {} ({})""".format(list(cnt_min_c.Admin2)[0],
                                                          list(cnt_min_c.US_state_confirmed_cases)[0])
        cnt_max_d = county_deaths[county_deaths.US_state_deaths == county_deaths["US_state_deaths"].max()]
        cnt_min_d = county_deaths[county_deaths.US_state_deaths == county_deaths["US_state_deaths"].min()]
        max_d = """Max Deaths: {} ({})""".format(list(cnt_max_d.Admin2)[0], list(cnt_max_d.US_state_deaths)[0])
        min_d = """Min Deaths: {} ({})""".format(list(cnt_min_d.Admin2)[0], list(cnt_min_d.US_state_deaths)[0])
        state_footer = ""

    return state_confirmed, state_deaths, state_header, county_avg_confirmed, county_avg_deaths, max_c, min_c, max_d, min_d, state_footer


# chloropleth and dropdown state deaths callback
@app.callback(Output("state_death", "figure"),
              [Input("state_death_tabs", "value"),
               Input("states_and_territories", "value")])
def display_click_data(tab, state):
    # state deaths dfs
    Daily_state_deaths = get_US_state_daily_deaths(state, US_covid_deaths)
    US_state_deaths = get_US_state_deaths(state, US_covid_deaths)

    # state deaths figs
    state_daily_death_fig = px.bar(Daily_state_deaths, x="Date", y="US_state_daily_deaths",
                                   title="<b>Daily Covid Deaths in {}</b>".format(state),
                                   labels={"US_state_daily_deaths": """Number of Deaths (Daily Total)"""})
    state_death_fig = px.bar(US_state_deaths, x="Date", y="US_state_deaths",
                             title="<b>Cumulative Covid Deaths in {}</b>".format(state),
                             labels={"US_state_deaths": """Number of Deaths (Running Total)"""})
    #
    if tab == "tab-1":
        figure = state_daily_death_fig
        figure.update_xaxes(nticks=20)
        return figure
    else:
        tab == "tab-2"
        figure = state_death_fig
        figure.update_xaxes(nticks=20)
        return figure

    return figure


# chloropleth and dropdown state deaths callback
@app.callback(Output("states_and_territories", "value"),
              [Input("chloro_graph", "clickData"),
               Input("territories", "value")])
def display_click_data(clickData, dropdown):
    # get state from map click or dropdown input
    ctx = dash.callback_context
    if clickData is None and dropdown is None:
        state = "Florida"
    else:
        pie = ctx.triggered[0]["prop_id"].split(".")[0]
        if pie == "territories":
            state = dropdown
        else:
            single_state = clickData["points"][0]["location"]
            state = get_state(single_state)
    return state


if __name__ == "__main__":
    app.run_server(debug=True)
    # server(gunicorn)
