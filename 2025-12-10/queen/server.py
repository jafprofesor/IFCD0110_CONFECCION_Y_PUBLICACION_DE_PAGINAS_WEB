from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

class CORSHTTPRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # Si la ruta es un directorio, servimos index.html
        if self.path == '/':
            self.path = '/index.html'
        elif not os.path.exists(self.translate_path(self.path)):
            # Si el archivo no existe, redirigir a index.html (para SPA)
            self.path = '/index.html'
        
        # Llamar al método original
        super().do_GET()
    
    def end_headers(self):
        # Añadir los encabezados CORS y de referrer
        self.send_header('Referrer-Policy', 'strict-origin-when-cross-origin')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

if __name__ == '__main__':
    PORT = 8000
    server_address = ('', PORT)
    
    print(f'Servidor iniciado en http://localhost:{PORT}')
    print('Accede a http://localhost:8000/index.html')
    
    with HTTPServer(server_address, CORSHTTPRequestHandler) as httpd:
        httpd.serve_forever()