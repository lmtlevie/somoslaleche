import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

app = dash.Dash()

my_css_url = "dashboard/app.css"
app.css.append_css({
"external_url": my_css_url
})


df = pd.read_csv(
    "scrapper/results.csv"
)

df = df[df["Precio"] < 1100 and df["Categoria"] ]

fig = px.histogram(
    df,
    x="Precio",
    nbins=60

)

fig.update_layout(xaxis={'categoryorder':'total ascending'}) # add only this line


#app.layout = html.Div([dcc.Graph(id="precio leches", figure=fig)])


app.layout = html.Div(
    [
        html.H1(
            "Monitore Leche Argentina",
        ),
        html.Div(dcc.Graph(id="precio leches", figure=fig,config={
        'displayModeBar': False
    })),

    ],
    className="container",
)



if __name__ == "__main__":
    app.run_server(debug=True)
