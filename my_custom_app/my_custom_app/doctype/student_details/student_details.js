// Copyright (c) 2024, me and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Student Details", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on('Student Details', {
    refresh: function(frm) {
        // Add a custom button to the form
        frm.add_custom_button(__('Create User'), function() {
            // When the button is clicked, call the server-side method to create the user
            frappe.call({
                method: 'my_custom_app.my_custom_app.doctype.student_details.student_details.create_user_if_not_exists',
                // Pass the name of the student document as an argument
                args: {
                    name: frm.doc.name
                },
                // Handle the response from the server
                callback: function(response) {
                    // If the response contains a message
                    if (response.message) {
                        // Display the message to the user
                        frappe.msgprint(response.message);
                    } else {
                        // If there is no message in the response, display a generic failure message
                        frappe.msgprint('Failed to create user.');
                    }
                }
            });
        });
    },
});
