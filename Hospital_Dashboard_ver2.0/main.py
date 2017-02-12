from bokeh.plotting import figure
import jinja2
from bokeh.embed import components
from bokeh.charts import Bar
import pandas as pd
from flask import Flask, render_template

import pandas.io.sql as psql
import psycopg2 as pg

from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable, TableColumn
#import win32com.client
#import shutil
#import pythoncom



#def refresh():
#    pythoncom.CoInitialize()
#    SourcePathName = "C:\\Users\\Administrator\\Documents\\Python_files\\Byoin_Dashboard_ajax_mono"
#    FileName = "BedData_odbc.xlsx"
#    Application = win32com.client.Dispatch("Excel.Application")
#	#Application.Visible = 0
#    Workbook = Application.Workbooks.Open(SourcePathName + "\\" + FileName)
#    Workbook.RefreshAll()
#    Workbook.Save()
#    Workbook.Close()
#    Application.Quit()
    


app = Flask(__name__)

@app.route('/', methods=["GET"])
def hello_bokeh():
    #refresh()
    with pg.connect(database='postgres',user='postgres',host='localhost',port=5432) as conn:
        sql = "SELECT * FROM byoto;"
        df = psql.read_sql(sql, conn)

    df.sort_values("id", inplace=True)
    #df = []
    #df = pd.read_excel("BedData_odbc.xlsx")
    #df = df[["ward","inflag"]]
    df2 = df
    df2 = df2[["id","ward","room","inflag"]]
    df2["inflag"] = df2["inflag"].apply(lambda x: "●在室" if x==True else "空室")
    source = ColumnDataSource(df2)
    columns = [TableColumn(field="id",title="id"),
               TableColumn(field="ward",title="病棟"),
               TableColumn(field="room",title="病室"),
               TableColumn(field="inflag",title="状態")]
    data_table = DataTable(source=source, columns=columns, width=550, height=600, sortable=False)
    script2,div2 = components(data_table)

    df = df[["ward", "inflag"]]
    df.rename(columns={"ward":"病棟","inflag":"在室フラグ"},inplace=True)
    exist = df.groupby("病棟").sum()
    exist.reset_index(inplace=True)
    exist["空床数"] = exist["在室フラグ"].apply(lambda x:3-x)
    p = Bar(exist, "病棟", "空床数", title="病棟別空床数", height=400, legend=False)

    script,div = components(p)
    

    return render_template('index.html', script=script, div=div,
                                         script2=script2, div2=div2)
        

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)