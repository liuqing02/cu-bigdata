from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random
from flask_cors import CORS



server = Flask(__name__, static_folder='')
CORS(server)
server.config['JSON_AS_ASCII'] = False

server.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1:3306/cu-bigdata'
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(server)


class ShoppingInfo(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger)
    item_id = db.Column(db.BigInteger)
    cat_id = db.Column(db.BigInteger)
    merchant_id = db.Column(db.BigInteger)
    brand_id = db.Column(db.BigInteger)
    month = db.Column(db.BigInteger)
    day = db.Column(db.Integer)
    action = db.Column(db.Integer)
    age_range = db.Column(db.Integer)
    gender = db.Column(db.Integer)
    province = db.Column(db.Integer)
    score = db.Column(db.Integer)


@server.route('/')
def index():
    return 'hello world hhhh'


@server.route('/id/<int:record_id>', methods=['GET'])
def get_shopping_info(record_id):
    try:
        current_time = datetime.now()

        # 获取当前秒数
        random_number = random.randint(1, 500)
        record = ShoppingInfo.query.filter_by(id=random_number).first()
        if record:
            # 将数据转换为字典
            data = {
                'id': record.id,
                'user_id': record.user_id,
                'item_id': record.item_id,
                'cat_id': record.cat_id,
                'merchant_id': record.merchant_id,
                'brand_id': record.brand_id,
                'month': record.month,
                'day': record.day,
                'action': record.action,
                'age_range': record.age_range,
                'gender': record.gender,
                'province': record.province,
                'score': record.score,
                'alarmNum':record.user_id,
                'offlineNum':record.cat_id,
                'onLineNum':record.merchant_id,
                'totalNum':record.brand_id
            }
            print(data)
            return jsonify(data)
        else:
            return jsonify({'message': 'Record not found'}), 404
    except Exception as e:
        return jsonify({'message': 'Error: {}'.format(str(e))}), 500


if __name__ == '__main__':
    server.run(host='0.0.0.0', port=8081, debug=True)