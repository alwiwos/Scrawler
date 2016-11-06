# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


# -*- coding:utf-8 -*-

import requests
import os


# 图片下载类
class ImageDownloadPipeline(object):
    def process_item(self, item, spider):
        if 'image_urls' in item:                # 如何‘图片地址’在项目中
            images = []                         # 定义图片空集

 #           dir_path = '%s/%s' % (settings.IMAGES_STORE, spider.name)
            dir_path = '/Users/suxd/Desktop/image'
  #          if not os.path.exists(dir_path):
   #             os.makedirs(dir_path)
            for image_url in item['image_urls']:
                #split() 分割字符串
                us = image_url.split('/')[3:]
                image_file_name = '_'.join(us)

                file_path = '%s/%s' % (dir_path, image_file_name)
                images.append(file_path)
                if os.path.exists(file_path):
                    continue

                with open(file_path, 'wb') as handle:
                    response = requests.get(image_url, headers={'User-Agent': "your agent string"}, stream=True)
                    for block in response.iter_content(1024):
                        if not block:
                            break

                        handle.write(block)

            item['images'] = images
        return item

