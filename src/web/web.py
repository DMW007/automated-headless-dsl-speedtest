from http.server import BaseHTTPRequestHandler, HTTPServer
from jinja2 import Template, Environment, FileSystemLoader
import os, sys, json, time
from dateutil.parser import parse
from dateutil import tz
from tzlocal import get_localzone

# ToDo: Works, but generates wrong VS Code errors
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db import DB

serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        db = DB()
        rows = db.get()

        dates = []
        date_objects = []
        download_speeds = []
        upload_speeds = []
        pings = []
        for row in rows:
            dates.append(row['date'])
            download_speeds.append(row['download'])
            upload_speeds.append(row['upload'])
            pings.append(row['ping'])

            # Parse for UI
            date_objects.append(self.convert_to_local_time(row['date']))

        cwd = os.path.dirname(os.path.realpath(__file__))
        env = Environment(loader=FileSystemLoader(cwd))
        template = env.get_template('index.j2')
        html = template.render(dates=dates, date_objects=date_objects, download_speeds=download_speeds, upload_speeds=upload_speeds, pings=pings)
        self.wfile.write(bytes(html, 'utf-8'))

    def convert_to_local_time(self, raw_utc_dt):
        # We need to add the timezone for proper parsing, since sqlite doesnt do this
        parsed_utc_dt = parse(raw_utc_dt + ' UTC')
        target_tz = get_localzone()

        local = parsed_utc_dt.replace(tzinfo=tz.gettz('UTC'))
        local = parsed_utc_dt.astimezone(target_tz)
        return local

if __name__ == "__main__":
    webServer = HTTPServer(('', serverPort), MyServer)
    print("Server started at http://*:%s" % (serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")