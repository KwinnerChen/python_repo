from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from polls.models import Questions
from django.urls import reverse

# Create your views here.


def index(request):
    latest_question_list = Questions.objects.all()
    context = {
            'latest_question_list': latest_question_list,
            }
    return render(request, 'polls/index.html', context)
    

def detail(request, question_id):
    try:
        question = get_object_or_404(Questions, id=question_id)
    except Questions.DoesNotExist:
        raise Http404("Question does not exist")
    context = {
        'question': question,
        'choices': question.choice_set.all()
    }
    return render(request, "polls/detail.html", context)


def results(request, question_id):
    question = get_object_or_404(Questions, id=question_id)
    return render(request, 'polls/result.html', {'question': question, 'choices': question.choice_set.all()})


def vote(request, question_id):
    # 获取对应id的问题对象
    question = get_object_or_404(Questions, id=question_id)
    try:
        # 每个视图函数的第一个参数必须时request请求对象
        # post方法的request对象包含一个请求方法命名的字典，包含了请求的主题参数（一般对应前端的提交表格）
        selected_choice = question.choice_set.get(id=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # 没有选择就提交则返回一个包含提示信息的相应对象
        # render为快捷方式，可以是HttpResponse
        return render(request, 'polls/detail.html', {'question': question, 'error_message': "you didn't select a choice"})
    else:
        # 选择成功，就在选票基础上加一
        selected_choice.votes += 1
        selected_choice.save()
        # 最后没有直接放回结果像是页，而是重定向到相应的视图
        # 当然可以返回一个直接结果，但是设计上不是最优
        # 每个页面对应一个视图，以便复用
        # HttpResponseRedirect首参数应该是一个url路由路径
        # reverse函数使用路由引用（，避免硬编码
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    