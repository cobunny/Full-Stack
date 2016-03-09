from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi  # cgi stands for Common Gateway Interface

# Import, register database with ORM Sqlalchemy
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create session and connect to DB
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class webServerHandler(BaseHTTPRequestHandler):
    """docstring for webServerHandler"""

    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Hello!</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text'><input type='submit' value='Submit'></form>'''
                output += "</body></html>"
                self.wfile.write(output)
                """
					Printing output in console comes handy for debugging.
				"""
                print output
                return

            if self.path.endswith("/restaurants"):
                restaurants = session.query(Restaurant).all()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Hot Pot Cohort</h1></br>"
                output += "<h2><a href = '/restaurants/new' > Add New </a></h2></br></br>"
                for restaurant in restaurants:
                    output += restaurant.name
                    output += "</br>"
                    output += "<a href='#'>Edit</a>"
                    output += "</br>"
                    output += "<a href='#'>Delete</a>"
                    output += "</br></br></br>"

                output += "</body></html>"
                self.wfile.write(output)
                return

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>New Fav Pot</h1>"
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>"
                output += "<input name='newHotPotRestaurant' type='text' placeholder='New Fav Hot Pot'>"
                output += "<input type='submit' value='Go'></form>"
                output += "</form></body></html>"
                self.wfile.write(output)
                return

            if self.path.endswith("/hi"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>hi</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text'><input type='submit' value='Submit'></form>'''
                output += "</body></html>"
                self.wfile.write(output)
                """
					Printing output in console comes handy for debugging.
				"""
                print output
                return

        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)

    def do_POST(self):
        try:
            if(self.path.endswith("/restaurants/new")):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('newHotPotRestaurant')

            # Create new hot pot Restaurant object
            newRestaurant = Restaurant(name=messagecontent[0])
            session.add(newRestaurant)
            session.commit()

            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            # Redirect to home page
            self.send_header('Location', '/restaurants')
            self.end_headers()
        except:
            pass


def main():
    try:
        port = 8080
        """
			For now set host to empty string ''
		"""
        server = HTTPServer(('', port), webServerHandler)
        print "Web server running on port %s" % port
        server.serve_forever()

    except KeyboardInterrupt:
        print '^C entered, stopping web server...'
        server.socket.close()


if __name__ == '__main__':
    main()
