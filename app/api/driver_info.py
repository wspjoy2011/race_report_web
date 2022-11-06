import os
from pathlib import Path
from flask import jsonify, request, current_app
from flask_restful import Resource, abort, Api
from xml.etree import ElementTree
from flasgger import swag_from

from models.race_model import Driver
import app.api.config as yaml_config

PATH_TO_YAML_CONFIG = os.path.join(Path(yaml_config.__file__).parent.absolute(), 'driver_info.yml')


class DriverInfo(Resource):
    """Driver info report API"""
    def __init__(self):
        self.format_type = request.args.get('format')
        self.check_format()
        self.drivers = Driver.select(Driver.abbr, Driver.name).dicts()
        self.driver = None

    @swag_from(PATH_TO_YAML_CONFIG)
    def get(self, driver_abbr):
        """Handle get request"""
        driver_abbr = driver_abbr.upper()
        self.driver = [driver for driver in self.drivers if driver['abbr'] == driver_abbr]

        if not self.driver:
            response = jsonify({'error': 'driver not found'})
            response.status_code = 404
            return response

        self.driver = self.driver.pop()

        if self.format_type == 'json':
            response = jsonify(self.driver)
        else:
            response = self.prepare_drivers_to_xml_convert()
        return response

    def check_format(self):
        """Check format json, xml"""
        if not self.format_type:
            self.format_type = 'json'
        if self.format_type not in ['json', 'xml']:
            abort(404)

    def prepare_drivers_to_xml_convert(self):
        """Prepare driver info to xml convert"""
        root = ElementTree.Element('Driver')
        abbr = ElementTree.SubElement(root, 'Abbr')
        abbr.text = self.driver['abbr']
        name = ElementTree.SubElement(root, 'Name')
        name.text = self.driver['name']
        tree = ElementTree.ElementTree(root)
        ElementTree.indent(tree, '  ')
        return current_app.response_class(ElementTree.tostring(root), mimetype='application/xml')


def init_api(app):
    api = Api(app)
    api.add_resource(DriverInfo, '/api/v1/drivers/<string:driver_abbr>/')
