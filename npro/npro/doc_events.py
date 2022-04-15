from __future__ import unicode_literals
import frappe, json


def on_validate_job_applicant(doc, method):
    from npro.npro.doctype.npro_status_log.npro_status_log import make_status_log

    make_status_log(doc, "status")


def on_submit_job_offer(doc, method):
    if not doc.status == "Offer Released & Awaiting Response":
        frappe.throw("Job Offer status must be Offer Released & Awaiting Response")


def on_validate_employee(doc, method):
    from frappe.desk.form.load import get_attachments

    # copy attachments from job offer to employee
    attachments = [d.file_name for d in get_attachments(doc.doctype, doc.name)]
    for d in frappe.get_all("Job Offer", {"job_applicant": doc.job_applicant}, limit=1):
        for att in get_attachments("Job Offer", d.name):
            print(att)
            if not att.file_name in attachments:
                _file = frappe.copy_doc(frappe.get_doc("File", att.name))
                _file.attached_to_doctype = "Employee"
                _file.attached_to_name = doc.name
                _file.save(ignore_permissions=True)