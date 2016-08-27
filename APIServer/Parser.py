import re

class Parser():
    def __init__(self):
        self.buffer = ''
        self.version = ''
        self.statusCode = 0
        self.contentLength = -1
        self.headers = []
        self.body = ''
        self.bodyStarted = False
    
    def parse(self, msg):
        if self.bodyStarted:
            self.body += msg
            return
            
        self.buffer += msg
        if not '\n' in self.buffer:
            return
        
        parseable = self.buffer[:self.buffer.rfind('\n')]
        self.buffer = self.buffer[self.buffer.rfind('\n')+1:]
        
        tokens = parseable.split('\n')
        for token in tokens:
            self.__parseToken(token)
        
        if self.bodyStarted:
            self.body += self.buffer
            self.buffer = ''
                
    
    def __parseToken(self, msg):
        if self.bodyStarted:
            self.body += msg + '\n'
            return
        
        msg = msg.strip('\r\n')
        if not msg and self.statusCode: # empty line
            self.bodyStarted = True
            return
        
        self.__parseHeader(msg)
    
    def __parseHeader(self, msg):
        #HTTP/1.1 200 OK
        match = re.match(r'^HTTP/(.*) (\d{3}) .*', msg)
        if match and not self.statusCode:
            self.version = match.group(1)
            self.statusCode = int(match.group(2))
            return
        
        #Content-type: text/html
        match = re.match(r'^([^:]*): (.*)', msg)
        if match:
            self.headers.append((match.group(1), match.group(2)))
            if match.group(1) == 'Content-Length':
                self.contentLength = int(match.group(2))
            return
                
    def end(self):
        return self.contentLength >= 0 and len(self.body) >= self.contentLength
            
            
