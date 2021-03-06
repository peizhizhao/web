#-*- coding=UTF-8 -*-
import os 
import json 
from flask import render_template
from flask import abort
from flask import Flask


app=Flask(__name__)

class Files(object):
    directory=os.path.join(os.path.abspath(os.path.dirname(__name__)),'..','files')
    #os.path.join()函数-将多个路径组合后返回\\join()——连接字符串数组
    def __init__(self):
        self._files=self._read_all_files()

    def _read_all_files(self):
        result={}
        for filename in os.listdir(self.directory):
            file_path=os.path.join(self.directory,filename)
            with open(file_path) as f:
                result[filename[:-5]]=json.load(f)
        return result
    def get_title_list(self):
        return [item['title'] for item in self._files.values()]

    def get_by_filename(self,filename):
        return self._files.get(filename)

files=Files()


#路由实现

@app.route('/')
def index():
    #show title name's table 
    return render_template('/index.html',title_list=files.get_title_list())

@app.route('/files/helloshiyanlou.json')
def file(helloshiyanlou):
    # read and show 'filename.json'  内容
    file_item=files.get_by_filename(helloshiyanlou)
    if not file_item:
        abort(404)
    return render_tempalte('/file.html',file_item=file_item)

@app.errorhandler(404)
def not_found(error):
    return render_template('/404.html'),404

if __name__=='__main__':
    app.debug=True
    app.run(port=3000)







