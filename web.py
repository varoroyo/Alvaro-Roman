# Copyright [2017] [name of copyright owner]

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.

# Author : Álvaro Román Royo (alvaro.varo98@gmail.com)


import http.server
import http.client
import json
import socketserver

class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    OPENFDA_API_URL = "api.fda.gov"
    OPENFDA_API_EVENT = "/drug/event.json"
    OPENFDA_API_LYRICA = '?search=patient.drug.medicinalproduct:"LYRICA"&limit=10'

    def get_main_page(self):
        html = '''
        <html>
            <head>
                <title>OpenFDA app</title>
            </head>
            <body>
                <h1>OpenFDA Client</h1>
                <form method='get' action='receivedrug'>
                    <input type='submit' value='Enviar a OpenFDA'>
                    </input>
                </form>
                <form method='get' action='searchmed'>
                    <input type='text' name='drug'></input>
                    <input type='submit' value='Buscar Medicamento'></input>
                </form>
                <form method='get' action='receivecompany'>
                    <input type='submit' value='Find companies'></input>
                </form>
                <form method='get' action='searchcom'>
                    <input type='text' name='drug'></input>
                    <input type='submit' value='Buscar medicinalproduct'></input>
                </form>
            </body>
        </html>
                '''
        return html
    def get_med(self,drug):
        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request("GET", self.OPENFDA_API_EVENT + '?search=patient.drug.medicinalproduct:'+drug+'&limit=10')
        r1 = conn.getresponse()
        print(r1.status, r1.reason)
        data1 = r1.read()
        data = data1.decode('utf8')
        events = json.loads(data)
        #event = events['results'][0]['patient']['drug']
        return events
    def get_medicinalproduct(self,com_num):
        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request("GET", self.OPENFDA_API_EVENT + '?search=companynumb:'+com_num+'&limit=10')
        r1 = conn.getresponse()
        print(r1.status, r1.reason)
        data1 = r1.read()
        data = data1.decode('utf8')
        events = json.loads(data)

        return events

    def get_events(self):

        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request("GET", self.OPENFDA_API_EVENT + '?limit=10')
        r1 = conn.getresponse()
        print(r1.status, r1.reason)
        data1 = r1.read()
        data = data1.decode('utf8')
        events = json.loads(data)
        #event = events['results'][0]['patient']['drug']
        return events

    def get_drugs(self, events):
        medicamentos=[]
        for event in events['results']:
            medicamentos+=[event['patient']['drug'][0]['medicinalproduct']]

        return medicamentos

    def get_companies_num(self, events):
        com_num=[]
        for event in events['results']:
            com_num+=[event['companynumb']]
        return com_num

    def get_html_list(self, list_items):
        s=''
        for item in list_items:
            s += "<li>"+item+"</li>"
        html='''
        <html>
            <head></head>
                <body>
                    <ul>
                        %s
                    </ul>
                </body>
        </html>''' %(s)
        return html

    def do_GET(self):

        print (self.path)

        self.send_response(200)

        self.send_header('Content-type','text/html')
        self.end_headers()

        if self.path == '/' :
            html = self.get_main_page()
        elif self.path == '/receivedrug?':
            events = self.get_events()
            drugs = self.get_drugs(events)
            html = self.get_html_list(drugs)
        elif self.path == '/receivecompany?':
            events = self.get_events()
            companies_num = self.get_companies_num(events)
            html = self.get_html_list(companies_num)
        elif 'searchmed' in self.path:
            drug=self.path.split('=')[1]
            print (drug)
            events = self.get_med(drug)
            com_num = self.get_com_num(events)
            html = self.get_html_list(com_num)
        elif 'searchcom' in self.path:
            com_num = self.path.split('=')[1]
            print (com_num)
            events = self.get_medicinalproduct(com_num)
            medicinalproduct = self.get_drugs(events)
            html = self.get_html_list(medicinalproduct)
        
        self.wfile.write(bytes(html,'utf8'))

        return
