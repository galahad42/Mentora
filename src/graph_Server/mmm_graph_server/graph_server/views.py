from flask import request, jsonify
from flask_restful import Resource

from graph_server import graph, app, api
from graph_server.graph_db import create_data

import requests


def check_token(token):
    """Check if the token is valid"""
    #s = requests.Session()
    #s.headers.update({"Content-Type": "application/json"})
    #s.headers.update({"Authorization": token})
    #response = s.get(app.config.get('AUTH_DATABASE_URI'))
    #return response
    return create_success_response("Pass Through")


def create_success_response(result):
    response_object = {
        'status': 'success',
        'data': result
    }
    res = jsonify(response_object)
    res.status_code = 201

    return res


def create_message_response(status, message, status_code):
    response_object = {
        'status': status,
        'message': message
    }
    res = jsonify(response_object)
    res.status_code = status_code
    return res


def get_mentors_mentees(is_mentor):
    try:
        #token = request.headers['Authorization']
        #response = check_token(token).json()
        if True:#response.get('status') == 'success':
            result = graph.run("MATCH (student:Person {is_mentor:$status}) RETURN student", status=is_mentor).data()
            return create_success_response(result)
        #else:
        #    return create_message_response(response['status'], response['message'], 401)
    except Exception as e:
        print(e)
        return create_message_response('fail', 'Try again', 500)


class StudentListAPI(Resource):
    @staticmethod
    def get():
        try:
            #token = request.headers['Authorization']
            #response = check_token(token).json()
            if True:#response.get('status') == 'success':
                result = graph.data("MATCH (student:Person) RETURN student")
                return create_success_response(result)
            #else:
            #    return create_message_response(response['status'], response['message'], 401)
        except Exception as e:
            print(e)
            return create_message_response('fail', 'Try again', 500)


class StudentAPI(Resource):
    @staticmethod
    def get(student_id):
        try:
            #token = request.headers['Authorization']
            #response = check_token(token).json()
            if True:#response.get('status') == 'success':
                result = graph.run("MATCH (student:Person {student_id:$id}) RETURN student", id=student_id).data()
                return create_success_response(result)
            #else:
            #    return create_message_response(response['status'], response['message'], 401)
        except Exception as e:
            print(e)
            return create_message_response('fail', 'Try again', 500)


class MentorsAPI(Resource):
    @staticmethod
    def get():
        return get_mentors_mentees(True)


class MenteesAPI(Resource):
    @staticmethod
    def get():
        return get_mentors_mentees(False)


class GroupAPI(Resource):
    @staticmethod
    def get(student_id):
        try:
            stmt = """
MATCH(p:Person {student_id:$id})-[:MATCHED_WITH]-(mentor:Person {is_mentor:true})
 WITH mentor
 MATCH(student:Person)-[:MATCHED_WITH]-(mentor) RETURN student
"""
            result = graph.run(stmt, id=student_id).data()
            return create_success_response(result)
        except Exception as e:
            print(e)
            return create_message_response('fail', 'Try again', 500)


class GroupInsertion(Resource):
    @staticmethod
    def put():
        try:
            create_data(request.get_json())
            return create_message_response('success', 'Data Inserted', 201)
        except Exception as e:
            print(e)
            return create_message_response('fail', 'Try again', 500)


# Setting the routes
api.add_resource(StudentListAPI, '/students')
api.add_resource(StudentAPI, '/students/<int:student_id>')
api.add_resource(MentorsAPI, '/students/mentors/')
api.add_resource(MenteesAPI, '/students/mentees/')
api.add_resource(GroupAPI, '/groups/<int:student_id>')
api.add_resource(GroupInsertion, '/groupInsertion')
