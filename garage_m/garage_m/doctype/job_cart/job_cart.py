# Copyright (c) 2024, saloni and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Job_cart(Document):
	def validate(self):
		
		for row in self.get("service_table"):
			# create a new document
			wo = frappe.get_doc({
				'doctype': 'Work_order',
				'job_cart_reference': self.name,
				"service_name":row.service_or_product_name,
				"quantity":row.quantity,
				"vehicle_no":self.get("vehicle_no"),
				"vehichle_model":self.get("vehicle_model"),
				"brand_name":self.get("brand_name"),
				"engine_capacity":self.get("engine_capacity"),
			})
			wo.insert()
			row.work_order_reference=wo.name

	
