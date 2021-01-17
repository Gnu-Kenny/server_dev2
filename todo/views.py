from rest_framework.views import APIView
from .models import Task
from rest_framework.response import Response
from datetime import datetime
from django.shortcuts import render  # 화면에 뿌린다
# Create your views here.


class Todo(APIView):
    def post(self, request):  # post 요청하면
        # create
        user_id = request.data.get('user_id', "")
        name = request.data.get('name', "")
        end_date = request.data.get('end_date', None)
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        Task.objects.create(user_id=user_id, name=name, end_date=end_date)
        # select 만들고 갱신된 리스트를 다시 보여야하기 때문
        tasks = Task.objects.all()
        task_list = []
        for task in tasks:
            task_list.append(dict(name=task.name, start_date=task.start_date,
                                  end_date=task.end_date, state=task.state))
        context = dict(task_list=task_list)

        return render(request, 'todo/todo.html', context=context)

    def get(self, request):
        tasks = Task.objects.all()
        task_list = []
        for task in tasks:
            task_list.append(dict(name=task.name, start_date=task.start_date,
                                  end_date=task.end_date, state=task.state))

        context = dict(task_list=task_list)

        return render(request, 'todo/todo.html', context=context)


class TaskCreate(APIView):
    def post(self, request):
        user_id = request.data.get('user_id', "")
        name = request.data.get('name', "")
        end_date = request.data.get('end_date', None)

        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            task = Task.objects.create(
                user_id=user_id, name=name, end_date=end_date)

        return Response(dict(msg="To-Do 생성 완료", name=task.name,
                             start_date=task.start_date.strftime('%Y-%m-%d'), end_date=task.end_date))


class TaskSelect(APIView):
    def post(self, request):
        user_id = request.data.get('user_id', "")
        tasks = Task.objects.filter(user_id=user_id)
        task_list = []

        for task in tasks:
            task_list.append(dict(name=task.name, start_date=task.start_date,
                                  end_date=task.end_date, state=task.state))

        return Response(dict(tasks=task_list))
