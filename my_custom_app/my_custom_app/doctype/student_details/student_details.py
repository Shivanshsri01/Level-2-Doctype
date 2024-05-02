import frappe # This line imports the Frappe library, which helps in managing data in the system.
@frappe.whitelist()
def create_user_if_not_exists(name):
    try:
        # Checks if a user with the given name already exists.
        if not frappe.db.exists("User", name):
            # Fetches the details of the student with the given name.
            student = frappe.get_doc("Student Details", name)
            
            # Creates a new user document.
            new_user = frappe.new_doc("User")
            new_user.first_name = student.first_name
            new_user.last_name = student.last_name
            
            # Checks if the student has an email before setting it for the user.
            if student.email:
                new_user.email = student.email.strip().lower()
            
            # Assigns the role 'Student' to the new user.
            new_user.append("roles", {
                "role": "Student"  
            })
            
            # Saves the new user document.
            new_user.insert(ignore_permissions=True)  
            
            # Displays a message confirming the user creation.
            frappe.msgprint("User created successfully.")
        else:
            # If the user already exists, displays a message.
            frappe.msgprint("User already exists.")
    except Exception as e:
        frappe.msgprint(f"Error creating user: {str(e)}")

   
   
   
# This class defines a 'Student Details' document, which represents information about a student.
class StudentDetails(frappe.model.document.Document):
    
    # This method runs before the document is saved.
    def before_save(self):
        # It updates the 'full_name' field by combining the first name, middle name (if exists), and last name.
        self.update_full_name()

    # This method updates the 'full_name' field.
    def update_full_name(self):
        # It combines the first name, middle name (if exists), and last name.
        self.full_name = f'{self.first_name} {self.middle_name or ""} {self.last_name or ""}'

    # This method ensures the 'full_name' field is updated whenever the name fields change.
    def validate(self):
        # If the document is new, it updates the 'full_name' field.
        if self.is_new():
            self.update_full_name()

        # It also sets up an automatic update of 'full_name' when any name field changes.
        # This ensures the 'full_name' field stays up to date in the database.
        frappe.db.set_value('Student Details', self.name, 'first_name', self.first_name)
        frappe.db.set_value('Student Details', self.name, 'middle_name', self.middle_name)
        frappe.db.set_value('Student Details', self.name, 'last_name', self.last_name)
        
