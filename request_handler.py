from animals.request import get_animals_by_status
from employees.request import get_employees_by_location
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from animals import get_all_animals
from animals import get_single_animal
from animals import create_animal
from animals import delete_animal
from animals import update_animal
from animals import get_animals_by_location
from animals import get_animals_by_status
from locations import get_all_locations
from locations import get_single_location
from locations import create_location
from locations import delete_location
from locations import update_location
from employees import get_all_employees
from employees import get_single_employee
from employees import create_employee
from employees import delete_employee
from employees import update_employee
from employees import get_employees_by_location
from customers import get_all_customers
from customers import get_single_customer
from customers import create_customer
from customers import delete_customer
from customers import update_customer
from customers import get_customers_by_email

# Here's a class. It inherits from another class.


class HandleRequests(BaseHTTPRequestHandler):

    def parse_url(self, path): #need self when function is inside a class
        # Just like splitting a string in JavaScript. If the
        # path is "/animals/2", the resulting list will
        # have "" at index 0, "animals" at index 1, and "1"
        # at index 2.
        path_params = path.split("/") #split on /, create list: ['', 'animals', '2'] where 2 is the animal id
        resource = path_params[1] #because of the empty string at index [0]
        
        # Check if there is a query string parameter
        if "?" in resource:
            # GIVEN: /customers?email=jenna@solis.com

            param = resource.split("?")[1]  # email=jenna@solis.com
            resource = resource.split("?")[0]  # 'customers'
            pair = param.split("=")  # [ 'email', 'jenna@solis.com' ]
            key = pair[0]  # 'email'
            value = pair[1]  # 'jenna@solis.com'

            return ( resource, key, value )
        
        # No query string parameter
        else:
            id = None

            # Try to get the item at index 2
            try:
            # Convert the string "1" to the integer 1
                # This is the new parseInt()
                id = int(path_params[2])
            except IndexError:
                pass  # No route parameter exists: /animals
            except ValueError:
                pass  # Request had trailing slash: /animals/

            return (resource, id)  # This is a tuple

    # Here's a class function
    def _set_headers(self, status):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        self.send_response(404)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    # Here's a method on the class that overrides the parent's method.
    # It handles any GET request.
    def do_GET(self):
        self._set_headers(200)

        response = {}

        # Parse URL and store entire tuple in a variable
        parsed = self.parse_url(self.path)

        # Response from parse_url() is a tuple with 2
        # items in it, which means the request was for
        # `/animals` or `/animals/2`
        if len(parsed) == 2:
            ( resource, id ) = parsed

            if resource == "animals":
                if id is not None:
                    response = f"{get_single_animal(id)}"
                else:
                    response = f"{get_all_animals()}"
            elif resource == "customers":
                if id is not None:
                    response = f"{get_single_customer(id)}"
                else:
                    response = f"{get_all_customers()}"

        # Response from parse_url() is a tuple with 3
        # items in it, which means the request was for
        # `/resource?parameter=value`
        elif len(parsed) == 3:
            ( resource, key, value ) = parsed

            # Is the resource `customers` and was there a
            # query parameter that specified the customer
            # email as a filtering value?
            if key == "email" and resource == "customers":
                response = get_customers_by_email(value)
            if key == "location_id" and resource == "animals":
                response = get_animals_by_location(value)
            if key == "status" and resource == "animals":
                response = get_animals_by_status(value)
            if key == "location_id" and resource == "employees":
                response = get_employees_by_location(value)

        self.wfile.write(response.encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.
    def do_POST(self):
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Initialize new entry
        new_entry = None #consider a different name, new_entry is a little vague

        # Add a new entry to the list. Don't worry about
        # the orange squiggle, you'll define the create_entry
        # function next.
        if resource == "animals":
            new_entry = create_animal(post_body)
        
        if resource == "locations":
            new_entry = create_location(post_body)
        
        if resource == "employees":
            new_entry = create_employee(post_body)
        
        if resource == "customers":
            new_entry = create_customer(post_body)

        # Encode the new animal and send in response
        self.wfile.write(f"{new_entry}".encode())


    # Here's a method on the class that overrides the parent's method.
    # It handles any PUT request.
    def do_PUT(self):
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        success = False

        if resource == "animals":
            success = update_animal(id, post_body)
        # rest of the elif's

        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        self.wfile.write("".encode())
    
    def do_DELETE(self):
        # Set a 204 response code
        self._set_headers(204)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Delete a single animal from the list
        if resource == "animals":
            delete_animal(id)
        
        if resource == "customers":
            delete_customer(id)
        
        if resource == "employees":
            delete_employee(id)
        
        if resource == "locations":
            delete_location(id)

        # Encode the new animal and send in response
        self.wfile.write("".encode())

    def do_PUT(self):
        self._set_headers(204)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Delete a single animal from the list
        if resource == "animals":
            update_animal(id, post_body)
        
        if resource == "customers":
            update_customer(id, post_body)
        
        if resource == "employees":
            update_employee(id, post_body)
        
        if resource == "locations":
            update_location(id, post_body)

        # Encode the new animal and send in response
        self.wfile.write("".encode())

# This function is not inside the class. It is the starting
# point of this application.
def main():
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()

if __name__ == "__main__":
    main()
