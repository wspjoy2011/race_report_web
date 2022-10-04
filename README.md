 Web report of Monaco 2018 Racing


The application has to have a few routes. E.g.

http://localhost:5000/report shows common statistic

http://localhost:5000/report/drivers/  shows list of drivers name and code. Code should be a link on info about drivers

http://localhost:5000/report/drivers/?driver_id=SVF shows info about a driver

Also, each route could get order parameter

http://localhost:5000/report/drivers/?order=desc


Use jinja2 package for html template.


Write tests using Unittest module or py.test.

Resources:
1. Flask https://flask.palletsprojects.com/en/1.1.x/
1. Jinja https://jinja.palletsprojects.com/en/2.11.x/**

