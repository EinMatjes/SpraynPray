from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort


app = Flask(__name__)
api = Api(app)

names = {
    "tim": {
        "age": 19,
        "gender": "male"
    },

    "bill": {
        "age": 18,
        "gender": "male"
    }
}

videos = {}


def abort_if_non_exist(video_id):
    if video_id not in videos: 
        abort("Video id is not valid...")





video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the Video is required", required = True)
video_put_args.add_argument("views", type=int, help="views of the Video is required", required = True)
video_put_args.add_argument("likes", type=int, help="likes of the Video is required", required = True)



class Video(Resource):
    def get(self, video_id):
        abort_if_non_exist(video_id)
        return videos[video_id]
    
    def put(self,video_id):
        args = video_put_args.parse_args()
        videos[video_id] = args
        return videos[video_id], 201


api.add_resource(Video, "/video/<int:video_id>")




if __name__ == "__main__":
    app.run(debug=True)
