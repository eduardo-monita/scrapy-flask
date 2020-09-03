

from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_pymongo import PyMongo

from scrapy import signals
from scrapy.crawler import CrawlerRunner
from scrapy.signalmanager import dispatcher
import time

# Importing our Scraping Function from the amazon_scraping file

from crawling.crawling.spiders.estadao import EstadaoSpider
from crawling.crawling.spiders.folha_uol import FolhaUolSpider
from crawling.crawling.spiders.nexojornal import NexoJornalSpider
import hashlib
import crochet

crochet.setup()

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config["MONGO_URI"] = "mongodb://localhost:27017/APS"
mongo = PyMongo(app)
news_collection = mongo.db.news_collection

output_data = []
crawl_runner = CrawlerRunner()


@app.route("/")
def index():
    cursor = news_collection.find({})
    news_documents = [document for document in cursor]

    return render_template("news_list.html", news=news_documents)


@app.route("/scrape")
def scrape():
    spiders = [EstadaoSpider, FolhaUolSpider, NexoJornalSpider]
    for spider in spiders:
        scrape_with_crochet(spider)
        time.sleep(3)

    for data in output_data:
        data["data"] = str(data["data"])
        data["_id"] = hashlib.md5(bytes(data["titulo"], "utf-8")).hexdigest()
        news_collection.replace_one(data, data, upsert=True)

    return render_template("news_list.html", news=output_data)


@crochet.run_in_reactor
def scrape_with_crochet(spider):
    dispatcher.connect(_crawler_result, signal=signals.item_scraped)

    eventual = crawl_runner.crawl(spider)
    return eventual


def _crawler_result(item, response, spider):
    output_data.append(dict(item))


if __name__ == "__main__":
    app.run(debug=True)
