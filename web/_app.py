from flask import Flask, render_template, jsonify, request
import pandas as pd
import os
import random
from datetime import datetime, timedelta, time

from services import LexiconiaService

"""
Lexiconia App
"""


app = Flask(__name__)

updateTime = time(5, 0, 0)  # 05:00:00

lexiconia_service  = LexiconiaService()

""" =============== Guide Page =============== """
@app.route('/')
def guide():
    return render_template('_guidepage.html')

if __name__ == '__main__':
    app.run(debug=True)