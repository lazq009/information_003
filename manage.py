from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand



# 配置文件
class Config(object):
    '''配置文件的加载'''

    # 设置秘钥  csrf和session 都需要
    SECRET_KEY = 'M8Wc9z1r8ljaPAgDL/S45FQ67MauJltbZfDGpDMbMbaFhzX0Nk25Qhi25NNE+Pn+'
    # 开启调试模式
    DEBUG = True
    # 配置数据库
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/information_003'
    # 关闭开启追踪
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 配置redis数据库
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379

    # 配置flask_session 将session数据写入到服务器的redis 数据库
    # 指定数据库session 数据储存在redis
    SESSION_TYPE = 'redis'
    # 告诉session服务器redis的位置
    SESSION_REDIS = StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    # 是否将session 签名后在存储
    SESSION_USE_SIGNER = True
    # 当SESSION——PERMANENT为True时 设置session 的有效期才可以成立  正好默认是true
    PERMANENT_SESSION_LIFETIME = 60*60*24   #自定义1天


app = Flask(__name__)


# 配置文件的加载
app.config.from_object(Config)

# 创建mysql数据库的链接
db = SQLAlchemy(app)

# 创建redis 数据库的链接
redis_store = StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)

CSRFProtect(app)
# 配置flask_session 将session 数据写入到服务器的redis 数据录
Session(app)

# 创建脚本管理器对象
manager = Manager(app)
# 让迁移和app db 建立关联
Migrate(app, db)
# 将迁移的脚本命令添加到manager
manager.add_command('mysql', MigrateCommand)

@app.route('/')
def index():

    # 测试redis
    # redis_store.set('name', 'www')
    # 测试session
    from flask import session
    # 会将session 数据库（name : www）, 写入到浏览器的cookie
    session['name'] = 'www'
    return 'index'


if __name__ == '__main__':
    manager.run()


