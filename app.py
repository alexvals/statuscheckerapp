import requests, json, threading
from socket import gaierror, gethostbyname
from multiprocessing.dummy import Pool as ThreadPool
from urllib.parse import urlparse
from flask import Flask, render_template, jsonify
from time import gmtime, strftime
from settings import refresh_interval, filename, site_down

def is_reachable(url):
    try:
        gethostbyname(url)
    except (gaierror):
        return False
    return True

def get_status_code(url):
    try:
        return requests.get(url, timeout=30).status_code
    except requests.ConnectionError:
        return site_down

def check_single_url(url):
    if is_reachable(urlparse(url).hostname):
        return str(get_status_code(url))
    else:
        site_down

def check_multiple_urls():
    statuses = {}
    temp_list_urls = []
    global returned_statuses, last_update_time
    t = threading.Timer(refresh_interval, check_multiple_urls)
    t.start()
    
    for group, urls in checkurls.items():
        temp_list_urls.extend(urls)
    
    pool = ThreadPool(8)
    temp_list_statuses = pool.map(check_single_url, temp_list_urls)
    
    for i in range(len(temp_list_urls)):
        statuses[temp_list_urls[i]] = temp_list_statuses[i]
    
    last_update_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    returned_statuses = statuses

app = Flask(__name__)

@app.route("/", methods=["GET"])
def display_returned_statuses():
    return render_template(
        "returned_status.html",
        returned_statuses=returned_statuses,
        checkurls=checkurls,
        last_update_time=last_update_time
    )

@app.route("/api", methods=["GET"])
def display_returned_api():
    return jsonify(returned_statuses), 200

with open(filename) as f:
    checkurls = json.load(f)

returned_statuses = {}
last_update_time = "time string"

if __name__ == "__main__":
    check_multiple_urls()
    app.run(debug=True)
