import os
from waitress import serve 
from whitenoise import WhiteNoise 
from optimization.wsgi import application

if __name__ == '__main__':
    static_root = os.path.join(os.path.realpath(__file__),'static')
    serve(WhiteNoise(application, root=static_root, prefix='/static'),host='0.0.0.0', port=8001)