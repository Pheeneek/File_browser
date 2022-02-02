import os
from functools import lru_cache
import hashlib
from flask import Flask, render_template
from dotenv import load_dotenv


class Search:
    dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    path = os.environ['VIDEO']

    def __init__(self, path_name=path):
        self.file_extensions = ['.avi', '.mkv', '.mp4', '.vob', '.mpg', '.flv', '.asx', '.exe']
        self.result_list = {}
        app = Flask(__name__)
        for item in os.walk(path_name):
            self.result_list[item[0]] = ["\\" + x for x in item[1]], \
                                        [y for y in item[2] if y[-4:] in self.file_extensions]

        @app.route("/<hashed>")
        def answer(hashed):
            for key in self.result_list:
                previous_dir = 0 if key.replace("/", "\\") == os.environ["VIDEO"]\
                    else os.path.dirname(key.replace("/", "\\"))
                if hashlib.md5(key.replace("/", "\\").encode()).hexdigest() == hashed:
                    return render_template("answer.html",
                                           directories=self.result_list[key][0],
                                           files=self.result_list[key][1],
                                           current_dir=key,
                                           previous_dir=previous_dir)
            return "Directory not found"

        @lru_cache()
        @app.route("/make_hash/")
        @app.route("/make_hash/<path:next_dir>")
        def make_hash(next_dir):
            previous_dir = 0 if next_dir.replace("/", "\\") == os.environ["VIDEO"] \
                else os.path.dirname(next_dir.replace("/", "\\"))
            next_dir = hashlib.md5(next_dir.replace("/", "\\").encode()).hexdigest()
            for key in self.result_list:
                if hashlib.md5(key.replace("/", "\\").encode()).hexdigest() == next_dir:
                    return render_template("answer.html",
                                           directories=self.result_list[key][0],
                                           files=self.result_list[key][1],
                                           current_dir=key,
                                           previous_dir=previous_dir)
            return "Directory not found"
        app.run()


if __name__ == '__main__':
    search = Search()
