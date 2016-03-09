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
                    output += "<a href='/restaurants/%s/edit'>Edit</a>" % restaurant.id
                    output += "</br>"
                    output += "<a href='/restaurants/%s/delete'>Delete</a>" % restaurant.id
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


            if self.path.endswith("/edit"):
                restaurantIDPath = self.path.split("/")[2]
                queryRestaurant = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
                if queryRestaurant !=[]:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    # Beginning to render the page
                    output = "<html><body>"
                    output += "<h1>"
                    output += queryRestaurant.name
                    output += "</h1>"
                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'>" % restaurantIDPath
                    output += "<input name='newHotPotRestaurant' type='text' placeholder='Type in a new name'>"
                    output += "<input type='submit' value='Rename'></form>"
                    output += "</form></body></html>"
                    self.wfile.write(output)


            if self.path.endswith("/delete"):
                restaurantIDPath = self.path.split("/")[2]
                queryRestaurant = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
                if queryRestaurant !=[]:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    # Beginning to render the page
                    output = "<html><body>"
                    output += "<h1>"
                    output += "Are you sure you want to delete %s?" % queryRestaurant.name
                    output += "</h1>"
                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete'>" % restaurantIDPath
                    output += "<input type='submit' value='Delete'></form>"
                    output += "</form></body></html>"
                    self.wfile.write(output)

        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)

    def do_POST(self):
        try:
            if(self.path.endswith("/edit")):
                ctype,pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newHotPotRestaurant')

                    restaurantIDPath= self.path.split('/')[2]
                    queryRestaurant = session.query(Restaurant).filter_by(id = restaurantIDPath).one()

                    if queryRestaurant != []:
                        queryRestaurant.name = messagecontent[0]
                        session.add(queryRestaurant)
                        session.commit()
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        # Redirect to home page
                        self.send_header('Location', '/restaurants')
                        self.end_headers()

            if(self.path.endswith("/delete")):
                restaurantIDPath= self.path.split('/')[2]
                queryRestaurant = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
                if queryRestaurant:
                    session.delete(queryRestaurant)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    # Redirect to home page
                    self.send_header('Location', '/restaurants')
                    self.end_headers()


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
