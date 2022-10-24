import os
from pathlib import Path
from collections import namedtuple
from app import app
from flask import jsonify, request
from flask_restful import Resource, Api, abort
from xml.etree import ElementTree
from flasgger import swag_from

from report_framework.report import main as main_report
import app.api.config as yaml_config

api = Api(app)
PATH_TO_RACE_DATA = app.config['PATH_TO_RACE_DATA']
PATH_TO_YAML_CONFIG = os.path.join(Path(yaml_config.__file__).parent.absolute(), 'driver_info.yml')


class DriverInfo(Resource):
    """Driver info report API"""
    def __init__(self):
        self.format_type = request.args.get('format')
        self.check_format()

        _, self.driver = main_report(PATH_TO_RACE_DATA)
        self.driver_info = None

    @swag_from(PATH_TO_YAML_CONFIG)
    def get(self, driver_abbr):
        """Handle get request"""
        driver_abbr = driver_abbr.upper()
        self.driver_info = self.make_driver_response_data(driver_abbr)

        if not self.driver_info:
            response = jsonify({'error': 'driver not found'})
            response.status_code = 404
            return response

        if self.format_type == 'json':
            response = jsonify(self.prepare_drivers_to_json_convert())
        else:
            response = self.prepare_drivers_to_xml_convert()
        return response

    def check_format(self):
        """Check format json, xml"""
        if not self.format_type:
            self.format_type = 'json'
        if self.format_type not in ['json', 'xml']:
            abort(404)

    def make_driver_response_data(self, driver_abbr):
        """Make dict like {abbr: driver}"""
        Driver = namedtuple('Driver', 'abbr name')
        driver_info = [Driver(abbr, driver[0]) for abbr, driver in self.driver.items() if abbr == driver_abbr]
        return driver_info.pop() if driver_info else []

    def prepare_drivers_to_xml_convert(self):
        """Prepare driver info to xml convert"""
        root = ElementTree.Element('Driver')
        abbr = ElementTree.SubElement(root, 'Abbr')
        abbr.text = self.driver_info.abbr
        name = ElementTree.SubElement(root, 'Name')
        name.text = self.driver_info.name
        tree = ElementTree.ElementTree(root)
        ElementTree.indent(tree, '  ')
        return app.response_class(ElementTree.tostring(root), mimetype='application/xml')

    def prepare_drivers_to_json_convert(self):
        """Prepare driver info to json convert"""
        driver = {
            'abbr': self.driver_info.abbr,
            'name': self.driver_info.name
        }
        return driver


api.add_resource(DriverInfo, '/api/v1/drivers/<string:driver_abbr>/')
