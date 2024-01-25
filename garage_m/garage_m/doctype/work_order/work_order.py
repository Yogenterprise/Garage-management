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
		# JC=frappe.get_doc({'doctype':"Job_cart"})
		# for row in JC.get("service_table"):
		# 	frappe.msgprint("hahhhaha")
		# 	row.status_of_work_order="accepted"



	def validate(self):
		l = []
		child_Qid_tab = self.get("quality_inspect")

		# Check for repeated parameters
		for row in child_Qid_tab:
			l.append(row.parameter)

		s = set(l)
		if len(s) != len(l):
			frappe.throw("Parameter can't be repeated")

		# Iterate over quality_inspect and insert Quality_certification documents
		for row in self.get("quality_inspect"):
			# Check if Quality_certification document already exists with the given name and parameter
			qc_exists = frappe.db.exists(
				"Quality_certification",
				{"work_order_reference": self.name, "parameter": row.parameter},
			)

			if qc_exists:
				frappe.msgprint(f"Quality Certification with parameter '{row.parameter}' already exists.")
				continue

			# Create a new Quality_certification document
			QC = frappe.get_doc({
				'doctype': 'Quality_certification',
				"job_cart_reference": self.job_cart_reference,
				"work_order_reference": self.name,
				"parameter": row.get("parameter"),
				"description": row.get("description"),
				"acceptable_value": row.get("acceptable_value"),
				"reading": row.get("reading")
			})

			# Insert the document
			QC.insert()
			frappe.msgprint(f"Quality Certification inserted for parameter '{row.parameter}'.")








	def on_update(self):
		total = 0
		accepted_count = 0

		for row in self.get("quality_inspect"):
			if row.status == "accepted":
				accepted_count += 1
			total += 1

		if total > 0:
			average = (accepted_count / total) * 100
			self.average = f"{average:.2f}%"  # Corrected the string formatting

			if average > 50:  # Corrected to use 'average' instead of 'self.average'
				self.submit()
		else:
			# frappe.msgprint("No quality inspections available.")
			pass


				





