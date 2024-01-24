# Copyright (c) 2024, aazar and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class DemoDoctype1(Document):
	def validate(self):
		self.demo_status = "status from code"
