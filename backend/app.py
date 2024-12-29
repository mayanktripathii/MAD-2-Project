from flask import Flask, redirect, url_for, flash, make_response

from flask_jwt_extended import JWTManager
from flask_cors import CORS
from celery import Celery
from flask_mail import Mail
from config import cache,Config
from redis import Redis
#from werkzeug.security import generate_password_hash, check_password_hash
from model import db


from admin import admin
from api import api
from influencer import influencer
from sponsor import sponsor


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///iescp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY']='influencersponsorplatform'
app.config.from_object(Config)

db.init_app(app)
CORS(app, resources={r"/*": {"origins": "*"}})
cache.init_app(app)
jwt=JWTManager(app)
mail=Mail(app)
#api=Api(app)

app.register_blueprint(admin, url_prefix="/admin")
app.register_blueprint(api, url_prefix="/api")
app.register_blueprint(influencer, url_prefix="/influencer")
app.register_blueprint(sponsor, url_prefix="/sponsor")

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)
    return celery

celery = make_celery(app)

redis_client = Redis(host='localhost', port=6379, db=1)
try:
    redis_client.ping()
    print("\n\nRedis connection successful\n\n")
except Exception as e:
    print(f"\n\nRedis connection failed: {e}\n\n")



@app.route("/home", methods=["GET", "POST"])
def home():
    return {"message": "Hello, World!"}


@app.route("/logout", methods=["POST", "GET"])
def logout():
    response = make_response(redirect(url_for("home")))
    response.set_cookie('jwt', '', expires=0, path="/")
    
    if app.config.get('CACHE_TYPE') == 'redis':
        prefix = app.config.get('CACHE_KEY_PREFIX', '')
        for key in redis_client.scan_iter(f"{prefix}*"):
            redis_client.delete(key)

    flash("Log out successful", "success")
    return response

# class SignupResource(Resource):
#     def post(self):
#         parser=reqparse.RequestParser()
#         parser.add_argument('username',type=str,required=True,help='Username is required')
#         parser.add_argument('email',type=str,required=True,help='Email is required')
#         parser.add_argument('password',type=str,required=True,help='Password is required')
#         parser.add_argument('role',type=str,required=True,help='Role is required')
        
#         args=parser.parse_args()
        
#         if User.query.filter_by(username=args['username']).first():
#             return {'message':'Username already exists'},400
#         if User.query.filter_by(email=args['email']).first():
#             return {'message':'Email already exists'},400
        
#         hashed_password=generate_password_hash(args['password'])
        
#         new_user=User(username=args['username'],email=args['email'],password=hashed_password,role=args['role'])
        
#         db.session.add(new_user)
#         db.session.commit()
        
#         return {'message':'User created successfully'},201


# class LoginResource(Resource):
#     def post(self):
#         parser = reqparse.RequestParser()
#         parser.add_argument('email', type=str, required=True, help='Email is required')
#         parser.add_argument('password', type=str, required=True, help='Password is required')
        
#         args = parser.parse_args()

#         user = User.query.filter_by(email=args['email']).first()

#         if user and check_password_hash(user.password, args['password']):
#             access_token=create_access_token(identity=user.role)
#             user_info={
#                 'id':user.id,
#                 'username':user.username,
#                 'role':user.role
#             }
        
#             return {'access_token': access_token,'user': user_info},200
#         else:
#             return {'message':'Invalid credentials'},401




# api.add_resource(SignupResource,'/api/signup')    
# api.add_resource(LoginResource, '/api/login')     



if __name__ == '__main__':
    app.run(debug=True)

