import os
from pathlib import Path
from app import app
from flasgger import swag_from
from flask import jsonify, request
from flask_restful import Resource, Api, abort
from xml.etree import ElementTree

from report_framework.report import main as main_report, sort_race_logs
from report_framework.cli_report import prepare_race_table
import app.api.config as yaml_config

api = Api(app)
PATH_TO_RACE_DATA = app.config['PATH_TO_RACE_DATA']
PATH_TO_YAML_CONFIG = os.path.join(Path(yaml_config.__file__).parent.absolute(), 'reports_race.yml')


class RaceReport(Resource):
    """Race report API"""
    def __init__(self):
        self.order = request.args.get('order')
        self.format_type = request.args.get('format')
        self.check_order()
        self.check_format()

        race_results, abbrs = main_report(PATH_TO_RACE_DATA)
        race_results_sorted = sort_race_logs(race_results, self.order)
        self.race_table = prepare_race_table(race_results_sorted, abbrs, '')

    @swag_from(PATH_TO_YAML_CONFIG)
    def get(self):
        """Handle get request"""
        if self.format_type == 'json':
            response = jsonify(self.prepare_report_to_json_convert())
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
            place.text = str(race.place)
            driver = ElementTree.SubElement(title, 'Driver')
            driver.text = race.driver
            company = ElementTree.SubElement(title, 'Company')
            company.text = race.company
            time = ElementTree.SubElement(title, 'Time')
            time.text = race.race_time
        tree = ElementTree.ElementTree(root)
        ElementTree.indent(tree, '  ')
        return app.response_class(ElementTree.tostring(root), mimetype='application/xml')

    def prepare_report_to_json_convert(self):
        """Prepare drivers info to json convert"""
        races = []
        for race in self.race_table:
            temp = {
                'place':   race.place,
                'driver':  race.driver,
                'company': race.company,
                'time':    race.race_time
            }
            races.append(temp)
        return races


api.add_resource(RaceReport, '/api/v1/report/')
