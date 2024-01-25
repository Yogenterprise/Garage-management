# Copyright (c) 2024, saloni and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Job_cart(Document):
	def validate(self):
		l=[]
		child_ser_tab=self.get("service_table")
		for row in child_ser_tab:
			l.append(row.service_or_product_name)
		s=set(l)
		if len(s) != len(l):
			frappe.throw("service_or_product_name cant be repeated")

		if self.workflow_state == "Servicing":
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
			

	# def on_submit(self):
	# 	for row in self.get("service_table"):
	# 		# create a new document
	# 		wo = frappe.get_doc({
	# 			'doctype': 'Work_order',
	# 			'job_cart_reference': self.name,
	# 			"service_name":row.service_or_product_name,
	# 			"quantity":row.quantity,
	# 			"vehicle_no":self.get("vehicle_no"),
	# 			"vehichle_model":self.get("vehicle_model"),
	# 			"brand_name":self.get("brand_name"),
	# 			"engine_capacity":self.get("engine_capacity"),
	# 		})
	# 		wo.insert()
	# 		# row.work_order_reference=wo.name
	# 		# frappe.db.commit()
			
	# 		frappe.db.set_value("Job_cart", self.name, row.work_order_reference, wo.name)



		



		




	
