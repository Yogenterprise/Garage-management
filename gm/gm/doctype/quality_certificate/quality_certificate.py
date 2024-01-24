# Copyright (c) 2024, aazar and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class QualityCertificate(Document):
	def on_submit(self):
		# frappe.throw(f"{type(self.acceptable_value.lower())}")
		av = self.acceptable_value.lower()
		pr = self.parameter_reading.lower()
		if av == pr:
			# frappe.throw("inside if")
			self.inspection_status = "Accepted"
		else:
			self.inspection_status = "Rejected"

		wo_doc_1 = frappe.get_doc('Work order', self.wo_reference)
		child_table = wo_doc_1.get('inspection_details')
		for row in child_table:
			if row.parameter == self.parameter:
				frappe.msgprint(f"parameter {self.parameter} found")
				
				row.inspection_status = self.inspection_status
				row.parameter_reading = self.parameter_reading
				
				frappe.msgprint(row.inspection_status)
								
		wo_doc_1.save()