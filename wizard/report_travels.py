from odoo import models, fields
from odoo.exceptions import ValidationError
import json
from odoo.tools import date_utils
import io
import xlsxwriter


class ReportTravelsManagement(models.TransientModel):
    _name = 'report.travels'

    customer_id = fields.Many2one('res.partner', string='Customer')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')

    def sql_values(self):
        query = """
          select location_travels.location,(select location_travels.location as
          destination_location from location_travels where package_travels.
          destination_location_id = location_travels.id),vehicle_travels.name,
          state from package_travels 
          inner join location_travels on location_travels.id = package_travels.
          source_location_id
          inner join vehicle_travels on vehicle_travels.id = package_travels.
          vehicle_id where 1=1 """
        if self.customer_id:
            query += """and package_travels.customer_id=%s""" % self.customer_id.id
        if self.start_date:
            query += """and package_travels.start_date>='%s'""" % self.start_date
        if self.end_date:
            query += """and package_travels.end_date<='%s'""" % self.end_date
        self._cr.execute(query)
        dict_sql = self._cr.dictfetchall()
        return dict_sql

    def print_report(self):
        if self.start_date > self.end_date:
            raise ValidationError('End date must be greater than start date')
        values = self.sql_values()
        data = {
            'model_id': self.id,
            'customer': self.customer_id.name,
            'from_date': self.start_date,
            'to_date': self.end_date,
            "data": values
            }
        return self.env.ref('travels_management.travels_management_report')\
              .report_action(None, data=data)

    def print_excel_report(self):
        if self.start_date >= self.end_date:
            raise ValidationError('Start Date must be less than End Date')
        values = self.sql_values()
        data = {
            'doc': self,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'customer': self.customer_id.name,
            'customer_id': self.customer_id.id if self.customer_id.id else False,
            'sql_dict': values
        }
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'report.travels',
                     'options': json.dumps(data, default=date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Travels Management Excel Report',
                     },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response):
        from_date = data['start_date']
        to_date = data['end_date']
        customer = data['customer']
        datas = data.get('sql_dict')
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        cell_format = workbook.add_format(
            {'font_size': '12px', 'align': 'center', 'color':'skyblue'})
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '20px'})
        heading = workbook.add_format({'font_size': '13px', 'color': 'skyblue',
                                       'border': 5, 'border_color': 'black'})
        txt = workbook.add_format({'font_size': '10px', 'align': 'center'})
        border = workbook.add_format({'border': 5, 'border_color': 'gray'})
        sheet.merge_range('H2:O3', 'TRAVELS MANAGEMENT EXCEL REPORT', head)
        sheet.merge_range('H5:I5', 'From Date:', cell_format)
        sheet.merge_range('J5:K5', from_date, txt)
        sheet.merge_range('H7:I7', 'To Date:', cell_format)
        sheet.merge_range('J7:K7', to_date, txt)
        sheet.merge_range('H9:I9', 'Customer:', cell_format)
        sheet.merge_range('J9:K9', customer, txt)
        sheet.merge_range('H11:I11', 'Source Location', heading)
        sheet.merge_range('J11:L11', 'Destination Location', heading)
        sheet.merge_range('M11:N11', 'Vehicle', heading)
        sheet.write('O11', 'Status', heading)
        row = 10
        for line in datas:
            row = row+1
            print(line)
            sheet.merge_range(f'H{row+1}:I{row+1}', line['location'], border),
            sheet.merge_range(f'J{row+1}:L{row+1}', line['destination_location']
                              , border),
            sheet.merge_range(f'M{row+1}:N{row+1}', line['name'], border),
            sheet.write(f'O{row+1}:O{row+1}', line['state'], border)
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()

