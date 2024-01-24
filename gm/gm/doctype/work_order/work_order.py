# Copyright (c) 2024, aazar and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Workorder(Document):	
	# pass
	def validate(self):
		if self.job_status == 1 and self.mechanic_remark != "":
			frappe.msgprint("Good, can submit")
			
			for row in self.get('inspection_details'):
				qc = frappe.get_doc({
					"doctype":"Quality Certificate",
					"job_card_reference": self.job_card_ref,
					"wo_reference":self.name,
					"parameter":row.parameter,
					"parameter_description": row.parameter_description,
					"acceptable_value":row.acceptable_value,					
				})

				qc.insert()
			
			# all_status = True
			# for row in self.get('inspection_details'):
				# row.inspection_status = "Accepted" if row.acceptable_value == row.parameter_reading else "Rejected"
				# if row.acceptable_value == row.parameter_reading:
				# 	row.inspection_status = "Accepted"
				# 	frappe.msgprint(f"{row.inspection_status}")
				# else:
				# 	row.inspection_status = "Rejected"
				# 	all_status = False

			# if not all_status:
			# 	frappe.throw("All inspections are not clear, cannot submit")
			# frappe.msgprint("Check box and mechanic remark present , can submit")			
		else:			
			frappe.throw("Set Remarks and Job Status to Submit.")