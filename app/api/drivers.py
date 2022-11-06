import os
from pathlib import Path
from flasgger import swag_from
from flask import jsonify, request, current_app
from flask_restful import Resource, Api, abort
from xml.etree import ElementTree

from models.race_model import Driver
import app.api.config as yaml_config

PATH_TO_YAML_CONFIG = os.path.join(Path(yaml_config.__file__).parent.absolute(), 'drivers.yml')


class DriverReport(Resource):
    """Race drivers """
    def __init__(self):
        self.order = request.args.get('order')
        self.format_type = request.args.get('format')
        self.check_order()
        self.order = True if self.order == 'desc' else False
        self.check_format()
        self.drivers = None

    @swag_from(PATH_TO_YAML_CONFIG)
    def get(self):
        """Handle get request"""
        drivers_rows = Driver.select(Driver.abbr, Driver.name).dicts()
        self.drivers = sorted(drivers_rows, key=lambda driver: driver['abbr'], reverse=self.order)

        if self.format_type == 'json':
            response = jsonify(self.drivers)
        else:
            response = self.prepare_drivers_to_xml_convert()
        return response

    def check_order(self):
        """Check order asc, desc"""
        if not self.order:
            self.order = 'asc'
        if self.order not in ['asc', 'desc']:
            abort(404)

    def check_format(self):
        """Check format json, xml"""
        if not self.format_type:
            self.format_type = 'json'
        if self.format_type not in ['json', 'xml']:
            abort(404)

    def prepare_drivers_to_xml_convert(self):
        """Prepare drivers info to xml convert"""
        root = ElementTree.Element('Drivers')
        for driver in self.drivers:
            title = ElementTree.Element('Driver')
            root.append(title)
            abbr = ElementTree.SubElement(title, 'Abbr')
            abbr.text = driver['abbr']
            name = ElementTree.SubElement(title, 'Driver')
            name.text = driver['name']
        tree = ElementTree.ElementTree(root)
        ElementTree.indent(tree, '  ')
        return current_app.response_class(ElementTree.tostring(root), mimetype='application/xml')


def init_api(app):
    api = Api(app)
    api.add_resource(DriverReport, '/api/v1/drivers/')
