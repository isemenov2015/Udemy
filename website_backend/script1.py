from flask import Flask, render_template

app = Flask(__name__)

@app.route('/plot/')
def plot():
    from pandas_datareader import data
    import datetime
    from bokeh.plotting import figure, show, output_file
    from bokeh.models.annotations import Title
    from bokeh.embed import components
    from bokeh.resources import CDN

    start = datetime.datetime(2017, 2, 10)
    end = datetime.datetime(2017, 3, 10)
    df = data.DataReader(name = 'GOOG', data_source = 'morningstar',
                            start = start, end = end)
    def inc_dec(o, c):
        return "Increase" if c > o else "Decrease"

    df["Status"] = [inc_dec(o, c) for o, c in zip(df.Open, df.Close)]
    df["Middle"] = (df.Open + df.Close) / 2
    df["Height"] = abs(df.Open - df.Close)
    p = figure(x_axis_type = 'datetime', width = 1000, height = 300,
                sizing_mode = 'scale_width')
    p.grid.grid_line_alpha = .3

    t = Title()
    t.text = "Candlestick Chart"
    p.title = t

    hour12 = 12 * 60 * 60 * 1000 # 12 hours in milliseconds

    #since decrease and increase days should be of different colors we ude two different DFs for graph
    p.segment(df.index, df.High, df.index, df.Low, color = "black")

    gdf = df[df.Status == "Increase"]
    p.rect(gdf.index, gdf.Middle, hour12, gdf.Height,
                       fill_color = '#CCFFFF', line_color = 'black')

    gdf = df[df.Status == "Decrease"]
    p.rect(gdf.index, gdf.Middle, hour12, gdf.Height,
                       fill_color = '#FF3333', line_color = 'black')

    #output_file("candlestick2.html")
    #show(p)

    script1, div1 = components(p)
    cdn_js = CDN.js_files
    cdn_css = CDN.css_files
    return render_template('plot.html', script1 = script1, div1 = div1,
                            cdn_css = cdn_css[0], cdn_js = cdn_js[0])

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about/')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug = True)
