# Copyright (c) 2024, aazar and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class JobCart(Document):
	def on_submit(self):
		job_cart_reference = self.name
		vehicle_number = self.vehicle_number
		vehicle_model = self.vehicle_model
		vehicle_brand = self.vehicle_brand
		engine_capacity = self.engine_capacity
		for row in self.get('service_details'):
			# frappe.msgprint(f"Service or Product name: {row.s_p_name}, Quantity: {row.quantity}, Rate: {row.rate}, Amount: {row.amount}")
			wo = frappe.get_doc({
				"doctype":"Work order",
				"job_card_ref": job_cart_reference,
				"service_name": row.s_p_name,
				"quantity": row.quantity,
				"rate": row.rate,
				"amount": row.amount,
				"description": row.description,
				"vehicle_number":vehicle_number,
				"vehicle_model":vehicle_model,
				"vehicle_brand":vehicle_brand,
				"engine_capacity":engine_capacity,
			})
			# wo = frappe.new_doc("Work Order")
			# wo.job_card_ref
			wo.insert()
			row.work_ord_ref = wo.name
			frappe.msgprint("Work order referece created")
		frappe.msgprint("Program execution completed")
		
		# frappe.msgprint(f"title of job name, {self.engine_capacity}")

