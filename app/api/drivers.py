from collections import namedtuple
from pathlib import Path
import os

from flasgger import swag_from
from flask import jsonify, request, current_app
from flask_restful import Resource, Api, abort
from xml.etree import ElementTree

from report_framework.report import main as main_report
import app.api.config as yaml_config

PATH_TO_YAML_CONFIG = os.path.join(Path(yaml_config.__file__).parent.absolute(), 'drivers.yml')


class DriverReport(Resource):
    """Race drivers """
    def __init__(self):
        self.order = request.args.get('order')
        self.format_type = request.args.get('format')
        self.check_order()
        self.check_format()

        _, self.divers = main_report(current_app.config['PATH_TO_RACE_DATA'])
        self.divers_info = self.make_drivers_response_data()

    @swag_from(PATH_TO_YAML_CONFIG)
    def get(self):
        """Handle get request"""
        if self.format_type == 'json':
            response = jsonify(self.prepare_drivers_to_json_convert())
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

    def make_drivers_response_data(self):
        """Make dict like {abbr: driver}"""
        DriverInfo = namedtuple('DriverInfo', 'abbr name')
        drivers_info = [DriverInfo(abbr, driver[0]) for abbr, driver in self.divers.items()]
        return drivers_info if self.order == 'asc' else sorted(drivers_info, reverse=True)

    def prepare_drivers_to_xml_convert(self):
        """Prepare drivers info to xml convert"""
        root = ElementTree.Element('Drivers')
        for driver in self.divers_info:
            title = ElementTree.Element('Driver')
            root.append(title)
            abbr = ElementTree.SubElement(title, 'Abbr')
            abbr.text = driver.abbr
            name = ElementTree.SubElement(title, 'Driver')
            name.text = driver.name
        tree = ElementTree.ElementTree(root)
        ElementTree.indent(tree, '  ')
        return current_app.response_class(ElementTree.tostring(root), mimetype='application/xml')

    def prepare_drivers_to_json_convert(self):
        """Prepare drivers info to json convert"""
        drivers = []
        for driver in self.divers_info:
            temp = {
                'abbr':   driver.abbr,
                'driver': driver.name
            }
            drivers.append(temp)
        return drivers


def init_api(app):
    api = Api(app)
    api.add_resource(DriverReport, '/api/v1/drivers/')
