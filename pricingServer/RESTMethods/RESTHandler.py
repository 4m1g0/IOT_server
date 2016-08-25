
class RESTHandler():
    def __init__(self, request):
        self.request = request
    
    def do_GET(self):
        self.request.send_response(404)
    
    def do_POST(self):
        self.request.send_response(404)
    
    def do_PUT(self):
        self.request.send_response(404)
    
    def do_DELETE(self):
        self.request.send_response(404)
