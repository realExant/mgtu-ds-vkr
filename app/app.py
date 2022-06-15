import flask
from flask import Flask, render_template, request
import pandas as pd
import pickle
import tensorflow as tf
#from tensorflow import keras

app = Flask(__name__, template_folder='templates')

features = {
    'density': 'Плотность, кг/м3',
    'elastic_modulus': 'модуль упругости, ГПа',
    'amount_hardener': 'Количество отвердителя, м.%',
    'content_epoxy_groups': 'Содержание эпоксидных групп,%_2',
    'flash_point': 'Температура вспышки, С_2',
    'surface_dens': 'Поверхностная плотность, г/м2',
    'tensile_modulus': 'Модуль упругости при растяжении, ГПа',
    'tensile_strength': 'Прочность при растяжении, МПа',
    'resin_consumption': 'Потребление смолы, г/м2',
    'patch_angle': 'Угол нашивки, град',
    'patch_pitch': 'Шаг нашивки',
    'patch_dens': 'Плотность нашивки'
}

params = dict(zip(features.keys(), ['1988.301966', '177.034495', '52.074364', '16.977083',
                                    '292.072967', '793.834135', '75.102747', '2371.373132',
                                    '172.99571', '0.0', '5.867705', '59.620426']))


def load_model(filename):
    file = open('./models/' + filename + '.pkl', 'rb')
    model = pickle.load(file)
    file.close()
    return model


def parse_data():
    data = {}
    data['density'] = float(request.form.get('density', 0))
    data['elastic_modulus'] = float(request.form.get('elastic_modulus', 0))
    data['amount_hardener'] = float(request.form.get('amount_hardener', 0))
    data['content_epoxy_groups'] = float(
        request.form.get('content_epoxy_groups', 0))
    data['flash_point'] = float(request.form.get('flash_point', 0))
    data['surface_dens'] = float(request.form.get('surface_dens', 0))
    data['tensile_modulus'] = float(request.form.get('tensile_modulus', 0))
    data['tensile_strength'] = float(
        request.form.get('tensile_strength', 0))
    data['resin_consumption'] = float(
        request.form.get('resin_consumption', 0))
    data['patch_angle'] = float(request.form.get('patch_angle', 0))
    data['patch_pitch'] = float(request.form.get('patch_pitch', 0))
    data['patch_dens'] = float(request.form.get('patch_dens', 0))

    data = dict(zip(features.values(), data.values()))
    return data


@app.route('/matrix_filler/', methods=['POST', 'GET'])
def matrix_filler():
    title = 'Прогнозирование соотношения матрица-наполнитель'
    df = pd.DataFrame()
    predict = ''

    if request.method == 'POST':
        data = parse_data()
        df = pd.DataFrame(data, index=[0])

        model = load_model('mf')
        predict = model.predict(df)[0][0]

    return render_template('predict.html', title=title, params=params, inputs=df.T.to_html(), predict=predict)


@app.route('/', methods=['GET'])
def main():
    if request.method == 'GET':
        return render_template('main.html')


if __name__ == '__main__':
    app.run()
