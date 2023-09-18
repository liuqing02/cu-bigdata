import json

from flask import Flask, request, jsonify
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, BigInteger, TIMESTAMP
import time
import redis
import datetime
from flask_cors import CORS

# 创建 Flask 应用
server = Flask(__name__, static_folder='')
CORS(server)
server.config['JSON_AS_ASCII'] = False

# 连接到 PostgreSQL 数据库
db_uri = 'postgresql://root:Root@localhost:5432/database'
engine = create_engine(db_uri)
Session = sessionmaker(bind=engine)
Base = declarative_base()


# 创建数据模型类
class UserBehavior(Base):
    __tablename__ = 'user_behavior_partitioned'

    id = Column(Integer, primary_key=True, nullable=False,
                server_default='nextval(\'user_behavior_partitioned_id_seq\'::regclass)')
    user_id = Column(Integer)
    product_id = Column(Integer)
    category_id = Column(Integer)
    action_type = Column(Integer)
    action_time = Column(TIMESTAMP, nullable=False)


# 路由：根据 ID 获取数据
@server.route('/id/<int:record_id>', methods=['GET'])
def get_user_behavior(record_id):
    try:
        current_time_in_seconds = int(time.time())

        # 创建数据库会话
        session = Session()

        # 查询记录
        record = session.query(UserBehavior).filter_by(id=record_id + current_time_in_seconds).first()
        session.close()

        if record:
            # 将数据转换为字典
            data = {
                'id': record.id,
                'user_id': record.user_id,
                'product_id': record.product_id,
                'category_id': record.category_id,
                'action_type': record.action_type,
                'action_time': record.action_time.strftime('%Y-%m-%d %H:%M:%S')
            }
            return jsonify(data)
        else:
            return jsonify({'message': 'Record not found'}), 404
    except Exception as e:
        return jsonify({'message': 'Error: {}'.format(str(e))}), 500


@server.route('/category/top', methods=['GET'])
def get_category_top():
    redis_client = redis.Redis(
        host='',  # 远程 Redis 服务器的 IP 地址
        port=6379,  # 远程 Redis 服务器的端口号，默认为 6379
        db=0,  # 数据库索引，通常为 0
        password=''  # 如果 Redis 服务器启用了密码认证，请提供密码
    )
    v = redis_client.get('category_top')
    # print(v)
    if v:
        data = json.loads(v)
        print(data)
        return jsonify(data)
    else:
        return 'no data'

@server.route('/pfcb/minute', methods=['GET'])
def get_pfcb_minute_data():
    redis_client = redis.Redis(
        host='',  # 远程 Redis 服务器的 IP 地址
        port=6379,  # 远程 Redis 服务器的端口号，默认为 6379
        db=0,  # 数据库索引，通常为 0
        password=''
        # password='your-redis-password'  # 如果 Redis 服务器启用了密码认证，请提供密码
    )
    v = redis_client.get('pfcb_minute_data')
    if v:
        data = json.loads(v)
        # print(data)
        return jsonify(data)
    else:
        return 'no data'

@server.route('/pfcb/day', methods=['GET'])
def get_pfcb_day_data():
    redis_client = redis.Redis(
        host='',  # 远程 Redis 服务器的 IP 地址
        port=6379,  # 远程 Redis 服务器的端口号，默认为 6379
        db=0,  # 数据库索引，通常为 0
        password=''
        # password='your-redis-password'  # 如果 Redis 服务器启用了密码认证，请提供密码
    )
    v = redis_client.get('pfcb_day_data')
    if v:
        data = json.loads(v)
        return jsonify(data)
    else:
        return 'no data'

@server.route('/variety', methods=['GET'])
def get_variety_percent_data():
    redis_client = redis.Redis(
        host='',  # 远程 Redis 服务器的 IP 地址
        port=6379,  # 远程 Redis 服务器的端口号，默认为 6379
        db=0,  # 数据库索引，通常为 0
        password=''
        # password='your-redis-password'  # 如果 Redis 服务器启用了密码认证，请提供密码
    )
    v = redis_client.get('variety_percent_data')
    if v:
        data = json.loads(v)
        return jsonify(data)
    else:
        return 'no data'

@server.route('/heatmap', methods=['GET'])
def get_heatmap_data():
    redis_client = redis.Redis(
        host='',  # 远程 Redis 服务器的 IP 地址
        port=6379,  # 远程 Redis 服务器的端口号，默认为 6379
        db=0,  # 数据库索引，通常为 0
        password=''
        # password='your-redis-password'  # 如果 Redis 服务器启用了密码认证，请提供密码
    )
    v = redis_client.get('heat_map_data')
    if v:
        data = json.loads(v)
        return jsonify(data)
    else:
        return 'no data'

@server.route('/conversion/rate', methods=['GET'])
def get_conversion_rate_data():
    redis_client = redis.Redis(
        host='',  # 远程 Redis 服务器的 IP 地址
        port=6379,  # 远程 Redis 服务器的端口号，默认为 6379
        db=0,  # 数据库索引，通常为 0
        password=''
        # password='your-redis-password'  # 如果 Redis 服务器启用了密码认证，请提供密码
    )
    v = redis_client.get('conversion_rate')
    if v:
        data = json.loads(v)
        return jsonify(data)
    else:
        return 'no data'



def get_time():
    current_datetime = datetime.datetime.now()
    return current_datetime.strftime("%Y-%m-%d %H:%M:%S")


if __name__ == '__main__':
    server.run(host='0.0.0.0', port=8888, debug=True)
