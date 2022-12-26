from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    likes = db.Column(db.Integer, nullable=False)
    views = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name={name}, views={views}, likes={likes})"

db.create_all()

"""
names = {"Muhammad": {"Major": "CS", "Session": "17"},
        "Ali": {"Major": "EE", "Session": "17"},
         }

class HelloWorld(Resource):

    def get(self, name):
        return names[name]

    def post(self):
        return {"data": "Posted"}


#api.add_resource(HelloWorld, "/hw/<string:name>/<int:test>") # accessing the passed parameters
api.add_resource(HelloWorld, "/hw/<string:name>")
"""
# Parsing the requests and making sure we have the req arguments(validating requests)
video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video is required", required=True)
video_put_args.add_argument("views", type=int, help="Views on the video are required", required=True)
video_put_args.add_argument("likes", type=int, help="Likes on the video are required", required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Name of the video is required",)
video_update_args.add_argument("views", type=int, help="Views on the video are required",)
video_update_args.add_argument("likes", type=int, help="Likes on the video are required",)


"""

def unknown_video(video_id):
    if video_id not in videos:
        abort(404, message="Video id is not valid...") # 404 = not found

def existing_video(video_id):
    if video_id in videos:
        abort(409, message=f"Video already exits with {video_id} ID")
"""

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
}


class Video(Resource):

    # get data from DB
    @marshal_with(resource_fields)  # serializes model instance to json
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message=f"Could not find video with id: {video_id}")
        return result

    # update data on DB
    @marshal_with(resource_fields)
    def put(self, video_id):
        args = video_put_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message="video already exist")
        video = VideoModel(id=video_id, name = args['name'], views = args['views'], likes = args['likes'])
        db.session.add(video)
        db.session.commit()
        return video, 201

    # Update data on db
    @marshal_with(resource_fields)
    def patch(self, video_id):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort (404, message= f"Video does not exist with id: {video_id}")

        if args['name']:
            result.name = args['name']
        if args['views']:
            result.views = args['views']
        if args['likes']:
            result.likes = args["likes"]

        # db.session.add(result)
        db.session.commit()

        return result


    def delete(self, video_id):
        existing_video(video_id)
        del videos[video_id]
        print(videos)
        return '', 204 # 204 means deleted successfully



api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
    app.run(debug=True)

