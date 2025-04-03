from functools import total_ordering
from http.client import responses
from django.shortcuts import render
import requests
from datetime import datetime


def index(request):
    return render(request, 'analytics/index.html')


def get_user_data(handle, start_epoch, end_epoch):
    api_url = f"https://codeforces.com/api/user.status?handle={handle}&from=1&count=100"
    response = requests.get(api_url)
    fetched_data = response.json()

    if fetched_data['status'] == 'OK':
        solved_problems = []
        total_score = 0

        for submission in fetched_data['result']:
            creation_time = int(submission['creationTimeSeconds'])
            if submission['verdict'] == 'OK' and start_epoch <= creation_time <= end_epoch:
                problem = submission['problem']
                modified_problem = {
                    'name': problem['name'],
                    'rating': problem.get('rating', 'No Rating'),
                    'time': datetime.fromtimestamp(creation_time)
                }
                solved_problems.append(modified_problem)
                if modified_problem['rating'] is not 'No Rating':
                    total_score += int(modified_problem['rating']) / 100
        total_solved = len(solved_problems)
        return solved_problems, total_score, total_solved
    else:
        return [], 0, 0

def user_stats(request):
    handle = request.GET.get('handle')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
    end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')

    start_epoch = int(start_date_obj.timestamp())
    end_epoch = int(end_date_obj.timestamp())

    if handle:
        solved_problems, total_score, total_solved = get_user_data(handle, start_epoch, end_epoch)
        return render(request, 'analytics/user_stats.html', {
            'handle': handle,
            'problems': solved_problems,
            "total_score": total_score,
            "total_solved": total_solved
        })
    else:
        return render(request, 'analytics/index.html', {'error': 'No Handle Provided'})