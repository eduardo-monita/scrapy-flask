# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import logging as log


def clean_titulo(param):
    return param.strip()


def clean_link(param):
    return param.strip()


def clean_site(param):
    return param.strip()


def clean_data(param):
    return param


class CrawlingPipeline:
    def process_item(self, item, spider):
        titulo = clean_titulo(item["titulo"])
        link = clean_link(item["link"])
        site = clean_site(item["site"])
        data = clean_data(item["data"])
        # News.objects.create(
        #     titulo=titulo, link=link, site=site, data=data,
        # )

        return item
