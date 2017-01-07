from bokeh.plotting import figure
import jinja2
from bokeh.embed import components
from flask import Flask, render_template



p = figure(title='空床情報グラフ')
p.line(x=[1,22,35,43,54,69,100], y=[6,5,8,100,10,30,20])

p2 = figure(title='処置件数グラフ')
p2.circle(x=[4,5,6,7], y=[11,23,12,4], size=20, alpha=0.5)

p3 = figure(title='死亡件数')
p3.vbar(top=[1,2,3,4], x=[1,2,3,4],bottom=0, width=0.5, color="#CAB2D6")


import numpy as np
from bokeh.layouts import row, widgetbox
from bokeh.models import CustomJS, Slider
from bokeh.plotting import figure, ColumnDataSource

x = np.linspace(0, 10, 500)
y = np.sin(x)

source = ColumnDataSource(data=dict(x=x, y=y))
plot = figure(y_range=(-10, 10), plot_width=400, plot_height=400)
plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)
callback = CustomJS(args=dict(source=source), code="""
    var data = source.data;
    var A = amp.value;
    var k = freq.value;
    var phi = phase.value;
    var B = offset.value;
    x = data['x']
    y = data['y']
    for (i = 0; i < x.length; i++) {
        y[i] = B + A*Math.sin(k*x[i]+phi);
    }
    source.trigger('change');
""")
amp_slider = Slider(start=0.1, end=10, value=1, step=.1,
                    title="Amplitude", callback=callback)

callback.args["amp"] = amp_slider

freq_slider = Slider(start=0.1, end=10, value=1, step=.1,
                     title="Frequency", callback=callback)
callback.args["freq"] = freq_slider

phase_slider = Slider(start=0, end=6.4, value=0, step=.1,
                      title="Phase", callback=callback)
callback.args["phase"] = phase_slider

offset_slider = Slider(start=-5, end=5, value=0, step=.1,
                       title="Offset", callback=callback)
callback.args["offset"] = offset_slider

p4 = row(
    plot,
    widgetbox(amp_slider, freq_slider, phase_slider, offset_slider),
)


script, div = components(p)
script2,div2 = components(p2)
script3,div3 = components(p3)
script4,div4 = components(p4)

app = Flask(__name__)

@app.route('/')
def hello_bokeh():
	return render_template('index.html', script=script, div=div, script2=script2, div2=div2, script3=script3, div3=div3, script4=script4, div4=div4)

if __name__ == '__main__':
    app.run(host='0.0.0.0')