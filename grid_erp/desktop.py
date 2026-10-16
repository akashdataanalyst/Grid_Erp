"""Removes desk items that older versions of grid_erp (and the apps merged into it) created.

Desk navigation itself is plain Frappe 16.51 data, nothing here builds it:

    /apps  →  "Grid ERP" tile              hooks.py add_to_apps_screen
                └── rail (Dock)            dock/grid_erp/grid_erp.json
                    ├── WhatsApp           grid_whatsapp/sidebar/grid_whatsapp/
                    ├── Recruitment …      recruitment_assessment/sidebar/recruitment_assessment/
                    ├── AI Assistant       grid_ai/sidebar/grid_ai/
                    └── Branding           grid_erp/sidebar/grid_erp/

Older versions grouped the modules in a "Business Suite" desktop folder (Desktop Icons linked to
Workspace Sidebars). Frappe 16.51 no longer syncs app Workspace Sidebars, so those icons led
nowhere; `remove_old_desk_items` (after_install / after_migrate) deletes what is left of them.
"""

from __future__ import annotations

import frappe

# Desktop Icons this app created ("Business Suite" folder and its children, and earlier ones).
OLD_ICONS = [
	"Business Suite", "Communication", "Hiring", "WhatsApp", "Recruitment Assessment",
	"Assessment Result", "AI Assistant", "Grid", "Operations", "Automations", "Alert Rules",
]

# Workspace Sidebars this app shipped before Frappe 16.51 (now Sidebars, see above).
OLD_SIDEBARS = ["WhatsApp", "Recruitment Assessment", "Assessment Result", "AI Assistant", "Grid", "Alert Rules"]

# App icons of former apps merged into grid_erp (akash_recruitment_assessment, grid_ai).
REMOVED_APP_ICONS = ["Akash Recruitment Assessment", "Grid AI"]


def remove_old_desk_items():
	for label in OLD_ICONS:
		if frappe.db.get_value("Desktop Icon", label, "app") == "grid_erp":
			frappe.delete_doc("Desktop Icon", label, ignore_permissions=True, force=True)
	for label in REMOVED_APP_ICONS:
		if frappe.db.exists("Desktop Icon", label):
			frappe.delete_doc("Desktop Icon", label, ignore_permissions=True, force=True)
	for name in OLD_SIDEBARS:
		if frappe.db.get_value("Workspace Sidebar", name, "app") == "grid_erp":
			frappe.delete_doc("Workspace Sidebar", name, ignore_permissions=True, force=True)

	frappe.cache.delete_key("desktop_icons")
	frappe.cache.delete_key("bootinfo")
