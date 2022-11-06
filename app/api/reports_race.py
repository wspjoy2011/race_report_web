import os
from pathlib import Path
from flasgger import swag_from
from flask import jsonify, request, current_app
from flask_restful import Resource, abort, Api
from xml.etree import ElementTree

from models.race_model import Race, Driver, Company
import app.api.config as yaml_config

PATH_TO_YAML_CONFIG = os.path.join(Path(yaml_config.__file__).parent.absolute(), 'reports_race.yml')


class RaceReport(Resource):
    """Race report API"""
    def __init__(self):
        self.order = request.args.get('order')
        self.format_type = request.args.get('format')
        self.check_order()
        self.order = True if self.order == 'desc' else False
        self.check_format()
        self.race_table = None

    @swag_from(PATH_TO_YAML_CONFIG)
    def get(self):
        """Handle get request"""
        race_table_rows = (
            Race.select(Race.place, Driver.name.alias('driver'), Company.name.alias('company'), Race.time)
            .join(Driver, on=(Race.driver == Driver.id))
            .join(Company, on=(Race.company == Company.id))
            .dicts())
        self.race_table = sorted(race_table_rows, key=lambda race: race['place'], reverse=self.order)

        if self.format_type == 'json':
            response = jsonify(self.race_table)
        else:
            response = self.prepare_report_to_xml_convert()
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

    def prepare_report_to_xml_convert(self):
        """Prepare race report to xml convert"""
        root = ElementTree.Element('Races')
        for race in self.race_table:
            title = ElementTree.Element('Race')
            root.append(title)
            place = ElementTree.SubElement(title, 'Place')
            place.text = str(race['place'])
            driver = ElementTree.SubElement(title, 'Driver')
            driver.text = race['driver']
            company = ElementTree.SubElement(title, 'Company')
            company.text = race['company']
            time = ElementTree.SubElement(title, 'Time')
            time.text = race['time']
        tree = ElementTree.ElementTree(root)
        ElementTree.indent(tree, '  ')
        return current_app.response_class(ElementTree.tostring(root), mimetype='application/xml')


def init_api(app):
    api = Api(app)
    api.add_resource(RaceReport, '/api/v1/report/')
