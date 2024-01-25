# Copyright (c) 2024, saloni and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Quality_certification(Document):
	def on_submit(self):
		if self.acceptable_value.lower()==self.reading:
			self.status="accepted"
		else:
			self.status="rejected"
		
		wo=frappe.get_doc('Work_order',self.work_order_reference
		)
		child_table=wo.get("quality_inspect")
		for row in child_table:
			if row.parameter==self.parameter:
				row.reading=self.reading
				row.status=self.status
		wo.save()
