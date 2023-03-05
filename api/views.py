from rest_framework.response import Response
from rest_framework.decorators import api_view
from . import models
from .serializers import TaskSerializer


@api_view(['GET'])
def getRoutes(request):
    routes = [
        {
            'Endpoint': '/tasks/',
            'method': 'GET',
            'body': None,
            'description': 'Returns an array of tasks'
        },
        {
            'Endpoint': '/task/id',
            'method': 'GET',
            'body': None,
            'description': 'Returns a single task object'
        },
        {
            'Endpoint': '/task/create/',
            'method': 'POST',
            'body': {'body': ""},
            'description': 'Creates new task with data sent in post request'
        },
        {
            'Endpoint': '/task/id/update/',
            'method': 'PUT',
            'body': {'body': ""},
            'description': 'Creates an existing task with data sent in post request'
        },
        {
            'Endpoint': '/tasks/id/delete/',
            'method': 'DELETE',
            'body': None,
            'description': 'Deletes and exiting task'
        },
    ]
    return Response(routes, )  # ensures data sent is not just python dictionary


@api_view(['GET'])
def getTasks(request):
    tasks = models.Task.objects.all()
    serializers = TaskSerializer(tasks, many=True)
    return Response(serializers.data)


@api_view(['GET'])
def getTask(request, pk):
    tasks = models.Task.objects.get(id=pk)
    serializers = TaskSerializer(tasks, many=False)
    return Response(serializers.data)


@api_view(['PUT'])
def updateNote(request, pk):
    data = request.data
    task = models.Task.objects.get(id=pk)
    serializers = TaskSerializer(instance=task, data=data)
    if serializers.is_valid():
        serializers.save()
    return Response(serializers.data)
