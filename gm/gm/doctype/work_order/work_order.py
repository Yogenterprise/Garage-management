# Copyright (c) 2024, aazar and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Workorder(Document):	
	# pass
	def validate(self):
		# frappe.msgprint("After save executed")
		if self.inspection_required == 1 and self.job_status == 1:
			# frappe.msgprint("Good, can submit")
			l = []
			for row in self.get('inspection_details'):
				l.append(row.parameter)
			s = set(l)
			if not (len(s) == len(l)):
				frappe.throw("Inspection parameters are repeated...cannot create qc")

			for row in self.get('inspection_details'):
				e = frappe.db.exists({
					"doctype" : "Quality Certificate",
					"parameter":row.parameter,
					"wo_reference":self.name,
				})
				if e:
					frappe.msgprint(f"Document exists...!")
					continue
				frappe.msgprint("Creating Quality Certificate Document")

				qc = frappe.get_doc({
					"doctype":"Quality Certificate",
					"job_card_reference": self.job_card_ref,
					"wo_reference":self.name,
					"parameter":row.parameter,
					"parameter_description": row.parameter_description,
					"acceptable_value":row.acceptable_value,					
				})								
				
				qc.insert()	
						
		else:					
			frappe.msgprint("Document Saved, Set inspection required to create inspection jobs.")

	def on_submit(self):
		if self.job_status == 1 and self.inspection_required == 1 and self.mechanic_remark != "":
			accepted = 0
			total = 0; rows = 0
			# frappe.throw("inside on submit")
			for row in self.get('inspection_details'):
				rows += 1
				# row.inspection_status = "Accepted" if row.acceptable_value == row.parameter_reading else "Rejected"
				# frappe.throw(f"inside row...{row.inspection_status}")
				if (row.inspection_status is not None) and (row.parameter_reading is not None):
					total += 1
					if (row.inspection_status.lower() == "accepted")  and (row.acceptable_value.lower() == row.parameter_reading.lower()):
						# row.inspection_status = "Accepted"
						accepted += 1
						frappe.msgprint(f"{accepted}")
					else:
						frappe.msgprint(f"inside row...{row.inspection_status}")
						
				else:
					frappe.throw("Status and reading required. cannot submit")
					
			average = accepted/total
			self.average_rating = round(average,2)
			frappe.db.set_value('Work order', self.name, 'average_rating', average)
			if average < 0.5:
				frappe.throw(f"Inspection not clear, cannot submit...{rows}...{total}")
			
			jc = frappe.get_doc('Job Cart', self.job_card_ref )
			service_details_ct = jc.get('service_details')
			for row in service_details_ct:
				if row.work_ord_ref == self.name:
					row.custom_service_status = "Completed"
			jc.save()

			frappe.msgprint("Accuracy achieved , can submit")
		else:					
			frappe.throw("Set Remarks and Inspection required to submit.")