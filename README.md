# Hospital_dashboard_ver.0.1

I created the interface of hospital dashboard which shows clinical data on the web page.
Python's library Flask and Bokeh make it possible to create beautiful interactive web page without writing a piece of JavaSript.

For the purpose of letting the page work in the environment which stants alone, I saved BokehJS and BokehCSS in the "static"
repository. You don't nead to copy and paste the long scripted chunk of js and css.

Files and directory:
main.py
/static
  bokeh-0.12.2.min.js
  bokeh-0.12.2.min.css
  bokeh-widgets-0.12.2.min.js
  bokeh-widgets-0.12.2.min.css
/templates
  index.html
  
As you can see, the version of these files is 0.12.2, which must be equal to your Bokeh's version. 
So please change the number to fit to you.
And of course these are for only the web page interface. The database interactions are not concerned here and the 
plotted data(graph) is just sumple.

Future plan:
• Put pandas.DataFrame(table) into the page with csv download botton.
• Make the layout of index.html more attractive.
