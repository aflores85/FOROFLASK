import json
from flask import Flask, request, jsonify # diccionarios de python los convienrte en Json y en response
from flask_sqlalchemy import SQLAlchemy # libreria para BBDD
from flask_cors import CORS # por seguridad Cros Origin


# helpers
def get_database_uri(prod_or_local):
    with open('config.json') as config_file:
        config = json.load(config_file)
    if prod_or_local == 'prod':
        return config['database']['prod']
    elif prod_or_local == 'local':
        return config['database']['local']
    return None


# initialize app
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://postgres:admin@localhost:5432/forodb" # conexion a la base
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# create Post model

class Foro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.String(80), nullable=False)
    
    def __repr__(self):
        return '<Foro %r>' % self.title

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.String(80), nullable=False)
    foro_id = db.Column(db.Integer, db.ForeignKey('foro.id'), nullable=False)
    foro = db.relationship('Foro', 
    backref=db.backref('subjects', lazy=True))

    def __repr__(self):
        return '<Subject %r>' % self.title

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.String(80), nullable=False)
    image_url = db.Column(db.String(180), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    subject = db.relationship('Subject', 
    backref=db.backref('posts', lazy=True))


    def __repr__(self):
        return '<Post %r>' % self.title


# define las relaciones ver documentacion

# define endpoints a Foro
@app.route('/api/v1/newforo', methods=['POST'])
def new_foro():
    foro_to_create = Foro(title=request.json['title'],
                          content=request.json['content']
                                                        )

    db.session.add(foro_to_create)
    db.session.commit()
    return jsonify({'message': 'Foro created successfully'})

@app.route('/api/v1/newsubject', methods=['POST'])

def new_subject():
    subject_to_create = Subject(title=request.json['title'],
                          content=request.json['content'],
                          foro_id=request.json['foro_id'])

    db.session.add(subject_to_create)
    db.session.commit()
    return jsonify({'message': 'Subject created successfully'})


@app.route('/api/v1/newpost', methods=['POST'])
def new_post():
    post_to_create = Post(title=request.json['title'],
                          content=request.json['content'],
                          image_url=request.json['imageURL'],
                          subject_id=request.json['subjectid'])

    db.session.add(post_to_create)
    db.session.commit()
    return jsonify({'message': 'Post created successfully'})


@app.route('/api/v1/getforo', methods=['GET'])
def get_foro():
    foros_Query = Foro.query.all() 
    foros_list = []
    for foros in foros_Query:
        foros_list.append(
            {'title': foros.title,
             'id': foros.id,
             'content': foros.content           
             })
    return jsonify({'posts': foros_list, 'message': 'Posts fetched successfully'})


@app.route('/api/v1/getsubject', methods=['GET'])
def get_subject():    
    subject_Query = Subject.query.all()
    subject_list = []
    for subject in subject_Query:
        subject_list.append(
            {'title': subject.title,
             'id': subject.id,
             'content': subject.content
            })
    return jsonify({'posts': subject_list, 'message': 'Posts fetched successfully'})


@app.route('/api/v1/getPosts', methods=['GET'])
def get_posts():
    # current_app.logger.info('request')
    posts = Post.query.all()
    posts_list = []
    for post in posts:
        posts_list.append(
            {'title': post.title,
             'id': post.id,
             'content': post.content,
             'image': post.image_url
             })
    return jsonify({'posts': posts_list, 'message': 'Posts fetched successfully'})

#los deletes
@app.route('/api/v1/deletepost/<id>', methods=['DELETE'])
def delete_posts(id):
    query_post_to_delete = Post.query.filter_by(id=id).first()
    db.session.delete(query_post_to_delete)
    db.session.commit()
    return jsonify({'message': 'Posts fetched successfully'})



@app.route('/api/v1/deletesubject/<id>', methods=['DELETE'])
def delete_subject(id):
    query_subject_to_delete = Subject.query.filter_by(id=id).first()
    db.session.delete(query_subject_to_delete)
    db.session.commit()
    return jsonify({'message': 'Subject fetched successfully'})


#https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/
#export FLASK_APP=app
#flask run
#curl -X POST http://127.0.0.1:5000/api/v1/newforo -H 'Content-Type: application/json' -d '{"title":"nuevo titulo X","content":"contenido X"}'
#curl -X POST http://127.0.0.1:5000/api/v1/newsubject -H 'Content-Type: application/json' -d '{"title":"nuevo subject","content":"contenido1","foro_id":"1"}'
#curl -X POST http://127.0.0.1:5000/api/v1/newpost -H 'Content-Type: application/json' -d '{"title":"nuevo post","content":"contenido1","imageURL":"", "subjectid":"1"}'
db.create_all()
