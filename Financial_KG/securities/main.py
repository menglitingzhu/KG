#coding:utf-8

import sys
import os

from pandas.io.sql import execute

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

execute(["scrapy", "crawl", "userinfo"])