# Copyright (c) 2024, saloni and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Work_order(Document):
	def on_submit(self):
		if self.job_cart_reference and  self.job_status==1:
			pass
		else:
			frappe.throw(f"please fill chek box and reference")

	def validate(self):
		for row in self.get("quality_inspect"):
			QC=frappe.get_doc({

				'doctype': 'Quality_certification',
				"job_cart_reference":self.job_cart_reference,
				"work_order_reference":self.name,
				"parameter":row.get("parameter"),
				"description":row.get("description"),
				"acceptable_value":row.get("acceptable_value"),
				"reading":row.get("reading")

			})

			QC.insert()
			frappe.msgprint("comm")

	def on_update(self):
		total=0
		for row in self.get("quality_inspect"):
			





