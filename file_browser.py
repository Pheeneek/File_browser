import os
from functools import lru_cache
import hashlib
from flask import Flask, render_template
from dotenv import load_dotenv


class Search:
    def __init__(self):
        self.file_extensions = ['.avi', '.mkv', '.mp4', '.vob', '.mpg', '.flv', '.asx', '.exe']
        dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
        if os.path.exists(dotenv_path):
            load_dotenv(dotenv_path)
        self.path_name = os.environ['VIDEO']
        app = Flask(__name__)

        @lru_cache()
        @app.route("/<hashed>")
        def answer(hashed):
            result_list = self.get_file_tree()
            hash_dict = {self.path_name.lower():
                         hashlib.md5(self.path_name.replace("/", "\\").lower().encode()).hexdigest()}
            for key in result_list:
                hash_dict[key] = hashlib.md5(key.replace("/", "\\").lower().encode()).hexdigest()
            for key in result_list:
                previous_dir = 0 if key.replace("/", "\\") == os.environ["VIDEO"].lower() \
                    else os.path.dirname(key.replace("/", "\\").lower())
                if hashlib.md5(key.replace("/", "\\").lower().encode()).hexdigest() == hashed:
                    return render_template("answer.html",
                                           directories=result_list[key][0],
                                           files=result_list[key][1],
                                           current_dir=key,
                                           previous_dir=previous_dir,
                                           hash_dict=hash_dict)
            return "Directory not found"

        app.run()

    def get_file_tree(self):
        result_list = {}
        for item in os.walk(self.path_name):
            result_list[item[0].lower()] = ["\\" + x.lower() for x in item[1]], \
                                           [y for y in item[2] if y[-4:] in self.file_extensions]
        return result_list


if __name__ == '__main__':
    search = Search()
