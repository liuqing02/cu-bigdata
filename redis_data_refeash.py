import redis
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import json
from datetime import datetime, timedelta,date
import pandas as pd
from decimal import Decimal

db_uri = 'postgresql://root:Root@localhost:5432/database'
engine = create_engine(db_uri)
Session = sessionmaker(bind=engine)
Base = declarative_base()

# 创建 Redis 连接对象
redis_client = redis.Redis(
    host='',  # 远程 Redis 服务器的 IP 地址
    port=6379,  # 远程 Redis 服务器的端口号，默认为 6379
    db=0,  # 数据库索引，通常为 0
    password=''  # 如果 Redis 服务器启用了密码认证，请提供密码
)


def get_category_top():
    # 执行 SQL 查询
    session = Session()

    sql_query = text("""
    SELECT category_id, COUNT(*) as purchase_count
    FROM user_behavior_partitioned
    WHERE action_type = 1
    GROUP BY category_id
    ORDER BY purchase_count DESC
    LIMIT 10;
    """)

    results = session.execute(sql_query).fetchall()
    session.close()
    row=["化妆品","服装","电器","电子产品", "家居","个护清洁","运动户外","宠物鲜花","健康保障","家纺"]
    results_dict = [{'category': row[0], 'count': row[1]} for row in results]  # return jsonify(data)
    results_dict = [{'category': row[i], 'count': result['count']} for i, result in enumerate(results_dict)]
    res = {'data': results_dict, 'timestamp': get_time()}
    v = json.dumps(res)
    redis_client.set('category_top', v)
    print(redis_client.get('category_top'))
    redis_client.close()


def get_pfcb_minute_data():
    # 执行SQL查询并将结果加载到Pandas DataFrame中
    sql_query = '''
    SELECT
    minute_start_time,
    SUM(pv_count) AS pv_count,
    SUM(fav_count) AS fav_count,
    SUM(cart_count) AS cart_count,
    SUM(buy_count) AS buy_count
FROM
    (
        SELECT
            TO_CHAR(DATE_TRUNC('minute', ubp.action_time), 'HH24:MI') AS minute_start_time,
            SUM(CASE WHEN ubp.action_type = 0 THEN 1 ELSE 0 END) AS pv_count,
            SUM(CASE WHEN ubp.action_type = 3 THEN 1 ELSE 0 END) AS fav_count,
            SUM(CASE WHEN ubp.action_type = 2 THEN 1 ELSE 0 END) AS cart_count,
            SUM(CASE WHEN ubp.action_type = 1 THEN 1 ELSE 0 END) AS buy_count
        FROM
            user_behavior_partitioned ubp
        WHERE
            ubp.action_type IN (0, 1, 2, 3)
        GROUP BY
            DATE_TRUNC('minute', ubp.action_time)
    ) AS subquery
GROUP BY
    minute_start_time
ORDER BY
    minute_start_time;
    '''

    df = pd.read_sql_query(sql_query, engine)

    # 将DataFrame重新格式化为所需的JSON格式
    result_json = {
        "chartData": {
            "time": df['minute_start_time'].tolist(),
            "num": [
                {
                    "name": "pv",
                    "value": df['pv_count'].tolist()
                }
                ,
                {
                    "name": "fav",
                    "value": df['fav_count'].tolist()
                },
                {
                    "name": "cart",
                    "value": df['cart_count'].tolist()
                },
                {
                    "name": "buy",
                    "value": df['buy_count'].tolist()
                }
            ]
        },
        "timestamp": get_time()
    }
    v = json.dumps(result_json)
    # print(v)
    redis_client.set('pfcb_minute_data', v)
    print(redis_client.get('pfcb_minute_data'))
    redis_client.close()


# 自定义日期编码函数
def date_encoder(obj):
    if isinstance(obj, date):
        return obj.strftime('%Y-%m-%d')
    raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')


def get_pfcb_day_data():
    sql_query = '''
    SELECT
    DATE(action_time) AS date,
    SUM(CASE WHEN action_type = 0 THEN 1 ELSE 0 END) AS pv_count,
    SUM(CASE WHEN action_type = 3 THEN 1 ELSE 0 END) AS fav_count,
    SUM(CASE WHEN action_type = 2 THEN 1 ELSE 0 END) AS cart_count,
    SUM(CASE WHEN action_type = 1 THEN 1 ELSE 0 END) AS buy_count
FROM
    user_behavior_partitioned
WHERE
    action_type IN (0, 1, 2, 3)
    AND DATE(action_time) >= '2017-11-25'
    AND DATE(action_time) <= '2017-12-03'
GROUP BY
    date
ORDER BY
    date;
    '''
    df = pd.read_sql_query(sql_query, engine)
    result_json = {
        "chartData": {
            "time": df['date'].tolist(),
            "purchaseCount": df['buy_count'].tolist(),
            "clickCount": df['pv_count'].tolist(),
            "collectCount": df['fav_count'].tolist(),
            "cartCount": df['cart_count'].tolist()
        },
        "timestamp": get_time()
    }
    v = json.dumps(result_json, default=date_encoder)

    redis_client.set('pfcb_day_data', v)
    print(redis_client.get('pfcb_day_data'))
    redis_client.close()


def get_variety_percent_data():
    sql_query = '''
    WITH CategoryCounts AS (
    SELECT
        category_id % 10 AS category_class,
        SUM(CASE WHEN action_type = 0 THEN 1 ELSE 0 END) AS pv_count,
        SUM(CASE WHEN action_type = 3 THEN 1 ELSE 0 END) AS fav_count,
        SUM(CASE WHEN action_type = 2 THEN 1 ELSE 0 END) AS cart_count,
        SUM(CASE WHEN action_type = 1 THEN 1 ELSE 0 END) AS buy_count
    FROM
        user_behavior_partitioned
    WHERE
        action_type IN (0, 1, 2, 3)
    GROUP BY
        category_class
)
SELECT
    CASE WHEN category_id % 10 = 0 THEN '化妆品'
         WHEN category_id % 10 = 1 THEN '服装'
         WHEN category_id % 10 = 2 THEN '家居'
         WHEN category_id % 10 = 3 THEN '电器'
         WHEN category_id % 10 = 4 THEN '个护清洁'
         WHEN category_id % 10 = 5 THEN '电子产品'
         WHEN category_id % 10 = 6 THEN '家纺'
         WHEN category_id % 10 = 7 THEN '健康保健'
         WHEN category_id % 10 = 8 THEN '宠物鲜花'
         WHEN category_id % 10 = 9 THEN '运动户外'
    END AS category_name,
    SUM(CASE WHEN action_type = 0 THEN 1 ELSE 0 END) AS pv_count,
    SUM(CASE WHEN action_type = 3 THEN 1 ELSE 0 END) AS fav_count,
    SUM(CASE WHEN action_type = 2 THEN 1 ELSE 0 END) AS cart_count,
    SUM(CASE WHEN action_type = 1 THEN 1 ELSE 0 END) AS buy_count,
    total_counts.total_pv,
    total_counts.total_fav,
    total_counts.total_cart,
    total_counts.total_buy,
    ROUND((SUM(CASE WHEN action_type = 0 THEN 1 ELSE 0 END) * 1.0 / total_counts.total_pv) * 100, 2) AS pv_percentage,
    ROUND((SUM(CASE WHEN action_type = 3 THEN 1 ELSE 0 END) * 1.0 / total_counts.total_fav) * 100, 2) AS fav_percentage,
    ROUND((SUM(CASE WHEN action_type = 2 THEN 1 ELSE 0 END) * 1.0 / total_counts.total_cart) * 100, 2) AS cart_percentage,
    ROUND((SUM(CASE WHEN action_type = 1 THEN 1 ELSE 0 END) * 1.0 / total_counts.total_buy) * 100, 2) AS buy_percentage
FROM
    user_behavior_partitioned,
    (SELECT
        SUM(CASE WHEN action_type = 0 THEN 1 ELSE 0 END) AS total_pv,
        SUM(CASE WHEN action_type = 3 THEN 1 ELSE 0 END) AS total_fav,
        SUM(CASE WHEN action_type = 2 THEN 1 ELSE 0 END) AS total_cart,
        SUM(CASE WHEN action_type = 1 THEN 1 ELSE 0 END) AS total_buy
    FROM
        user_behavior_partitioned
    WHERE
        action_type IN (0, 1, 2, 3)
    ) AS total_counts
WHERE
    action_type IN (0, 1, 2, 3)
GROUP BY
    category_id % 10, category_name, total_counts.total_pv, total_counts.total_fav, total_counts.total_cart, total_counts.total_buy
ORDER BY
    category_id % 10;
    '''

    connection = engine.connect()
    result = connection.execute(text(sql_query))
    connection.close()

    # 初始化结果数据结构
    # data = []
    #
    #
    # # 遍历查询结果并组装数据
    # for row in result:
    #     category_name, pv_count, fav_count, cart_count, buy_count, total_pv, total_fav, total_cart, total_buy, pv_percentage, fav_percentage, cart_percentage, buy_percentage = row
    #
    #     pv_percentage = float(pv_percentage)
    #     fav_percentage = float(fav_percentage)
    #     cart_percentage = float(cart_percentage)
    #     buy_percentage = float(buy_percentage)
    #
    #     row_dict = {
    #         'category_name': category_name,
    #         'pv_count': pv_count,
    #         'fav_count': fav_count,
    #         'cart_count': cart_count,
    #         'buy_count': buy_count,
    #         'pv_percentage': pv_percentage,
    #         'fav_percentage': fav_percentage,
    #         'cart_percentage': cart_percentage,
    #         'buy_percentage': buy_percentage,
    #         'total_pv': total_pv,
    #         'total_fav': total_fav,
    #         'total_cart': total_cart,
    #         'total_buy': total_buy,
    #     }
    #
    #     data.append(row_dict)
    #
    # # 计算第10行的占比，以确保总占比不超过1
    # total_pv_percentage = sum(row['pv_percentage'] for row in data)
    # total_fav_percentage = sum(row['fav_percentage'] for row in data)
    # total_cart_percentage = sum(row['cart_percentage'] for row in data)
    # total_buy_percentage = sum(row['buy_percentage'] for row in data)
    #
    # # 计算第10行的占比调整值
    # adjustment_pv_percentage = 1 - total_pv_percentage
    # adjustment_fav_percentage = 1 - total_fav_percentage
    # adjustment_cart_percentage = 1 - total_cart_percentage
    # adjustment_buy_percentage = 1 - total_buy_percentage
    #
    # # 更新第10行的占比数据
    # for row,index in enumerate(data):
    #     if index == 9:
    #         row['pv_percentage'] += adjustment_pv_percentage
    #         row['fav_percentage'] += adjustment_fav_percentage
    #         row['cart_percentage'] += adjustment_cart_percentage
    #         row['buy_percentage'] += adjustment_buy_percentage
    #
    # # 将数据转换为 JSON 格式
    # result_json = {
    #     'chartData': data,
    #     'timestamp': get_time()
    # }
    #
    # # 将数据转换为 JSON 字符串
    # json_string = json.dumps(result_json, ensure_ascii=False)

    chart_data = {
        "chartData": [],
        "timestamp": get_time()
    }

    # 遍历查询结果并组装数据
    for row in result:
        category_name, pv_count, fav_count, cart_count, buy_count, total_pv, total_fav, total_cart, total_buy, pv_percentage, fav_percentage, cart_percentage, buy_percentage = row

        pv_percentage = float(pv_percentage)
        fav_percentage = float(fav_percentage)
        cart_percentage = float(cart_percentage)
        buy_percentage = float(buy_percentage)

        data_point = {
            "name": category_name,
            "value": buy_count  # 这里使用 buy_count 作为值
        }

        chart_data["chartData"].append(data_point)

    # 将数据转换为 JSON 字符串
    json_string = json.dumps(chart_data, ensure_ascii=False, indent=4)

    redis_client.set('variety_percent_data', json_string)
    print(redis_client.get('variety_percent_data'))
    redis_client.close()

def  get_heat_map_data():
    # sql_query = '''
    #     SELECT
    #     EXTRACT(HOUR FROM action_time) AS hour,
    #     SUM(CASE WHEN action_type = 0 THEN 1 ELSE 0 END) AS clicks,
    #     SUM(CASE WHEN action_type = 3 THEN 1 ELSE 0 END) AS fav,
    #     SUM(CASE WHEN action_type = 2 THEN 1 ELSE 0 END) AS cart,
    #     SUM(CASE WHEN action_type = 1 THEN 1 ELSE 0 END) AS orders,
    #     COUNT(*) AS total_visits
    # FROM
    #     user_behavior_partitioned
    # WHERE
    #     action_type IN (0, 1, 2, 3)
    # GROUP BY
    #     hour
    # ORDER BY
    #     hour;
    # '''
    # connection = engine.connect()
    # result = connection.execute(text(sql_query))

    # # 遍历查询结果并组装数据
    # for row in result:
    #     hour, clicks, fav, cart, orders, conversion_rate = row
    #     if hour == 0:
    #         data_point = [0, 0, 0, 0, 0]
    #     else:
    #         data_point = [clicks / hour, fav / hour, cart / hour, orders / hour, conversion_rate / hour]
    #
    #     chart_data["data"].append(data_point)

    heatmap = [[0,0,0.17],[0,1,0.18],[0,2,0.13],[0,3,0.67],[0,4,1],[1,0,0.72],[1,1,0.61],[1,2,0.62],[1,3,1],[1,4,0.67],
[2,0,0.9],[2,1,0.7],[2,2,1],[2,3,0.62],[2,4,0.13],
[3,0,0.81],[3,1,1],[3,2,0.7],[3,3,0.61],[3,4,0.18],
[4,0,1],[4,1,0.81],[4,2,0.9],[4,3,0.72],[4,4,0.17]]

    # 初始化结果数据结构
    chart_data = {
        "xChartData": ["点击次数/小时", "收藏次数/小时", "加购次数/小时", "下单次数/小时", "转化率/小时"],
        "yChartData": ["转化率/小时", "下单次数/小时", "加购次数/小时", "收藏次数/小时", "点击次数/小时"],
        "data": heatmap
    }

    # 添加时间戳
    timestamp = get_time()
    chart_data["timestamp"] = timestamp

    # 将数据转换为 JSON 格式
    v = json.dumps(chart_data, ensure_ascii=False, cls=DecimalEncoder)
    redis_client.set('heat_map_data', v)
    print(redis_client.get('heat_map_data'))
    redis_client.close()

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

def get_time():
    current_datetime = datetime.now()
    return current_datetime.strftime("%Y-%m-%d %H:%M:%S")

def get_conversion_rate():
    start_date = datetime(2017, 11, 25, 0, 0)
    end_date = datetime(2017, 12, 4, 23, 0)
    current_date = start_date
    v = [0.01650769181359797, 0.01612221909321318, 0.016852104886459756, 0.015646699379687067, 0.01518932407507866,0.013426240652617267, 0.015143320713899405, 0.01654080537728018, 0.0208011243851019, 0.024831805901361446,0.028416023353136366, 0.028917455077988794, 0.026888875802367353, 0.026246328068457576, 0.02582216297353753,0.024975154044921486, 0.022843945093846758, 0.022290428611854853, 0.020259992448352124, 0.019427215548751233,0.019257951797719754, 0.01831389400450174, 0.0182703381844833, 0.016542763378206416, 0.015602468708542424,0.015790253295808028, 0.012922972283625234, 0.013509886373803346, 0.013973523849548225, 0.012039903680770554,0.012569603668522765, 0.015502812457127178, 0.019210776777216488, 0.023502511432641128, 0.02644952138961295,0.027322951056568956, 0.027746699485343477, 0.025656472208177798, 0.025471922056744176, 0.02489688863973091,0.023361874538450792, 0.024202528329075785, 0.02232393453948789, 0.020336291130062495, 0.020014846760224823,0.01865625768379641, 0.018407327312046813, 0.01741406685834442, 0.033870264254237545, 0.021056621980218494,0.01759003659241189, 0.016053141433711598, 0.019170025051737285, 0.01648860099268108, 0.018327471668620556,0.021606974552309144, 0.02503850761595071, 0.03069200143806341, 0.03052893148739794, 0.030384031749737365,0.029040975017923125, 0.02891429842386744, 0.028405313861835372, 0.028304883730780633, 0.02785125252839583,0.026199010069977813, 0.02384130997247262, 0.023144141377481223, 0.02125660510669643, 0.02000222246916324,0.019773804208014823, 0.01962466784765279, 0.017243833861266326, 0.018550747567439286, 0.016676209561981105,0.01746812569019175, 0.01563188022897402, 0.014412053717654767, 0.018222542803993776, 0.017788506609168465,0.024798661769017193, 0.027308226884638295, 0.03133603701376592, 0.02998812700577192, 0.028887661598458122,0.027310837172622754, 0.026877714383036704, 0.02712387028176502, 0.026642625961721525, 0.024876433248864693,0.02390299954516075, 0.02187922592678946, 0.022503299094774696, 0.020921178483382954, 0.020145886344359626,0.01908616065126347, 0.018056302671687285, 0.016506242993544397, 0.015371889432687668, 0.019101016820298394,0.015181518151815182, 0.01463963963963964, 0.015060933547942055, 0.017713328057353008, 0.023529411764705882,0.02772494606910813, 0.030254656024325352, 0.03069085770291523, 0.027927831749759796, 0.027844858771423824,0.02819736119864197, 0.02808018318402764, 0.027469037789774532, 0.025526809683320266, 0.02409251894047933,0.02323941776512481, 0.022128556375131718, 0.021171842946735003, 0.020939798080518508, 0.02044456516818326,0.017082562893348488, 0.016184585756083107, 0.015669323247332164, 0.014833711262282692, 0.013746838227207743,0.016640708254774983, 0.016357440363498676, 0.01804123711340206, 0.021772536840232285, 0.027458357731072545,0.03222983500885787, 0.03014997107382849, 0.028694297421888337, 0.027524846753555914, 0.02660611971230038,0.024158190886983687, 0.02710888185160783, 0.024137890629577118, 0.023471480404750635, 0.023402948949536834,0.02156174567210153, 0.020444772562428763, 0.02023787000006524, 0.019518420676852777, 0.017176266097811487,0.015265358854928093, 0.015562794064422729, 0.015400678673975463, 0.013812154696132596, 0.01438326311201511,0.014540717529838397, 0.017343630002559944, 0.022317981033577364, 0.02614710922129847, 0.029520888736381572,0.030218312820337982, 0.028175255057928412, 0.02540152860492725, 0.025973633893529233, 0.025971945492956335,0.024445630448204775, 0.0227475570405291, 0.02138252032959319, 0.02031934027895612, 0.018469032707028533,0.01821492533737444, 0.01771396606377028, 0.016129525206681032, 0.016159409371704084, 0.014986924160128747,0.016118573413617415, 0.014071559892518739, 0.015206555715130523, 0.012206572769953052, 0.01364772217594669,0.015162595680366632, 0.019348550663602342, 0.023413450757344096, 0.027912361952262203, 0.0271159902496308,0.02775387657213994, 0.024879641231946185, 0.025680065787866697, 0.025041140124817587, 0.023118654576455087,0.02267394451748182, 0.021014404047823072, 0.01988263174223871, 0.019345165071835556, 0.017840251239169096,0.017284352231465846, 0.016469641388722027, 0.016610891390325525, 0.01479186665503098, 0.01295120320855615,0.014494596312778132, 0.01341317365269461, 0.013466666666666667, 0.012775374710793683, 0.014029374001816303,0.018409409002663777, 0.022595399003344938, 0.028306889440680105, 0.026890437422381674, 0.026477314844110176,0.025302566556392465, 0.024958455080293925, 0.024466759961246868, 0.023915794049384057, 0.023614747414052104,0.021088256052244455, 0.020642407751434746, 0.019064560965983517, 0.018431227951288542, 0.016619515509181802,0.01672318288085259, 0.018497611798550875, 0.01641722520981729, 0.014749103001603429, 0.013505944774105294,0.013091234041421372, 0.012926726894537081, 0.013713498701977371, 0.01587691087632307, 0.018590751361199333,0.02189786883927113, 0.02499398180387595, 0.027438705948812654, 0.028935326888687166, 0.028976756767386168,0.02816811231114629, 0.02700631304938774, 0.02570275567775984, 0.023820999637030518, 0.022225537207022583,0.02060981046116876, 0.019562823073700147, 0.019068902502755402, 0.018345686906012754, 0.017851957639683728]

    time = []
    value = []
    i = 0
    while current_date <= end_date:
        time.append(current_date.strftime("%m/%d %H:%M"))
        value.append(v[i])
        current_date += timedelta(hours=1)
        i = i + 1

    res = {
        "chartData": {
            "time": time,
            "value": value
        },
        "timestamp": get_time()
    }
    redis_value = json.dumps(res, ensure_ascii=False, cls=DecimalEncoder)
    redis_client.set('conversion_rate', redis_value)
    print(redis_client.get('conversion_rate'))
    redis_client.close()



if __name__ == '__main__':
    get_category_top()
    get_pfcb_minute_data()
    get_pfcb_day_data()
    get_variety_percent_data()
    get_heat_map_data()
    get_conversion_rate()