from flask import Flask, render_template, request, redirect, send_file
from stack_over_flow import get_stackOverFlow_jobs
from exporter import save_to_file

app = Flask("SuperScrapper")


db = {}

# ! @는 데코레이터로 @요청이 들어오면 '바로 아래있는 함수'를 찾아서 실행한다.
# ! 다른 파일불러와서 띄워주기


@app.route("/")
def home():
    return render_template('home.html')


@app.route('/contact')
def contact():
    return 'Contact me!'


# ! dynamic URLs : url의 값을 사용할 수있다.
@app.route('/<username>')
def username(username):
    return f"Hello your name is : {username}"


# ! query arguments : request.args를 사용해서 안에 뭐가 있는지 뽑아올 수 있다.
@app.route('/search')
def search():
    # print(request.args.get('word'))
    word = request.args.get('word')
    if word:
        word = word.lower()
        fromDb = db.get(word)
        if fromDb:
            jobs = fromDb
        else:
            jobs = get_stackOverFlow_jobs(word)
            db[word] = jobs
    else:
        return redirect('/')
    return render_template('search.html', searchingBy=word, resultsNumber=len(jobs), jobs=jobs)


@app.route('/export')
def export():
    try:
        word = request.args.get('word')

        if not word:
            raise Exception()

        word = word.lower()
        jobs = db.get(word)
        if not jobs:
            raise Exception()
        save_to_file(jobs)
        return send_file('jobs.csv')
    except:
        return redirect('/')


app.run(host='127.0.0.1')
