from flask import Flask, render_template, request, jsonify
import time

app = Flask(__name__)

# Global Variables
work_duration = 25 * 60  # in seconds
break_duration = 5 * 60  # in seconds
is_running = False
remaining_time = work_duration
start_time = None


@app.route('/')
def index():
    global work_duration, break_duration
    return render_template('index.html', work_duration=work_duration//60, break_duration=break_duration//60)


@app.route('/start', methods=['POST'])
def start():
    global is_running, remaining_time, start_time, work_duration
    is_running = True
    if not start_time:
        start_time = time.time()
    if remaining_time == 0:
        remaining_time = work_duration
    return jsonify(status="started", remaining_time=remaining_time)


@app.route('/pause', methods=['POST'])
def pause():
    global is_running, remaining_time, start_time
    if is_running:
        elapsed = time.time() - start_time
        remaining_time -= elapsed
        start_time = None
    is_running = not is_running
    return jsonify(status="paused" if not is_running else "resumed", remaining_time=remaining_time)


@app.route('/reset', methods=['POST'])
def reset():
    global is_running, remaining_time, start_time, work_duration
    is_running = False
    remaining_time = work_duration
    start_time = None
    return jsonify(status="reset", remaining_time=remaining_time)


@app.route('/update_durations', methods=['POST'])
def update_durations():
    global work_duration, break_duration
    work_duration = int(request.form['work_duration']) * 60
    break_duration = int(request.form['break_duration']) * 60
    return jsonify(status="updated")


if __name__ == '__main__':
    app.run(debug=True)
