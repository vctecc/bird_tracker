from flask import Flask, render_template, url_for, redirect, send_from_directory
from flask_wtf import CSRFProtect
from flask_bootstrap import Bootstrap5
from pathlib import Path
from image_pager import ImgPager

app = Flask(
    __name__,
    template_folder='./templates',
    static_folder='./static',
    )
app.config['SECRET_KEY'] = 'iddqd'

bootstrap = Bootstrap5(app)
csrf = CSRFProtect(app)
pager = ImgPager(Path('./static/images'))


@app.route('/media/<path:path>')
def media_route(path):
    return send_from_directory("media", path, as_attachment=True)


@app.route('/camera')
def camera():
    return render_template('camera.html', path='preview.jpeg')


@app.route('/')
def home():
    return redirect('/0')


@app.route('/<int:index>/')
def gallery(index):
    pager.set(index)
    print('get idx', index, pager.idx)
    return render_template(
        'index.html',
         index=pager.idx,
         path=pager.get(index).name,
         pager=pager
        )


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000, debug=True)
