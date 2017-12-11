# coding:utf-8
from application import app
from flask import Flask,request,render_template,flash,redirect,url_for,session,make_response,abort
from flask import send_file, send_from_directory
from flask_restful import Resource, Api, abort, reqparse
from flask.ext.login import LoginManager, login_required
from flask.ext.login import login_user,current_user,logout_user

import re,shutil,os,datetime
from werkzeug import secure_filename

from model import *
from dev_tools import * 
from middleware import * 


# 避免中文传给jinja2时候报错
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


# REDIS的全局变量
# R表示实例连接,缓存的过期时间
CACHE_TIME = config["default"].REDIS_PORT

# Flask-login 模块 =======
app.secret_key = app.config['SECRET_KEY']
login_manager = LoginManager()
login_manager.session_protection = 'none'
login_manager.login_view = 'login'
# 设置当未登录用户请求一个只有登录用户才能访问的视图时，闪现的错误消息的内容，
# 默认的错误消息是：Please log in to access this page.。
login_manager.login_message = u'请先登录'
# 设置闪现的错误消息的类别
login_manager.login_message_category = "login_info"
login_manager.init_app(app)





# 如果用户名存在则构建一个新的用户类对象，并使用用户名作为ID
# 如果不存在，必须返回None
@login_manager.user_loader
def load_user(username):

    # 回调，把信息放到这里，这样所有页面current_user可以传输用户的数据了

    curr_user = User()
    user_info = Data_Processor.get_user_info(username)
    curr_user.id = user_info.get('user_data').get('username') # 给用户名
    curr_user.data = user_info.get('user_data')
    return curr_user

# 注册登录

@app.route('/login',methods=['POST','GET'])
@app.route('/register',methods=['POST','GET'])
def login():
    
    if request.method == 'GET':
        return render_template('/pc/login.html')

    elif request.method == 'POST':
        print "表单数据"
        # 拿出来用户登录密码
        # 用户为登录
        if request.form.get('login_username',None) != None:

            login_username = request.form.get('login_username')
            login_password = request.form.get('login_password')
            #记住我功能
            remember_me_flag = True if request.form.get('remember_me_flag') == u'on' else  False

            print '表单提交数据',request.form
            print login_username,login_password,remember_me_flag

            # 判断交给user_login方法，返回 {'flag':True,"status":''}
            result = Data_Processor.user_login(login_username,login_password)

            # 通过认证，账户密码正确
            if result.get('flag') == True:
            # 这里改成用中间件来验证。

                curr_user = User()
                #  返回用户数据{'status':xxx, 'flag': False, 'user_data': {'username': u'yanggan', 'phone': None, 'email': None, 'id': 5, 'user_type': 1}}
                user_info = Data_Processor.get_user_info(login_username)
                curr_user.id = user_info.get('user_data').get('username') # 给用户名
                # 用用户数据传给data
                curr_user.data =user_info.get('user_data')
                # 通过Flask-Login的login_user方法登录用户
                login_user(curr_user,remember=remember_me_flag)

                # 如果请求中有next参数，则重定向到其指定的地址，
                # 没有next参数，则重定向到"index"视图
                next = request.args.get('next')
                return redirect(url_for('index'))
                # return redirect(next or url_for('index'))
            
            # 没有通过认证
            flash(result.get('status'),'login_error')
            return redirect(url_for('login'))
        # 用户提交的是注册表单
        elif request.form.get('register_username',None) != None:
            
            # 拿出来数据
            register_username = request.form.get('register_username').strip().lower()  
            register_password = request.form.get('register_password').strip().lower() 
            register_vipcode = request.form.get('register_vipcode').strip().lower()         
            
            # 不给输入为空,密码不能6位数以下            
            if register_username =='' or  register_password == '':
                result = {'flag':False,"status":'不能输入为空,请重试'}
            elif len(register_password) < 6:
                result = {'flag':False,"status":'密码小于6位数,请重试'}
            else: 
                # 判断交给user_login方法，返回 {'flag':True,"status":''}
                result = Data_Processor.user_register(register_username,register_password,register_vipcode)
                
            if result.get('flag') == False:

                flash(result.get('status'),'register_error')
                return redirect(url_for('login'))

            elif result.get('flag') == True:
               
                # 注册成功，免登陆
                curr_user = User()
                curr_user.id = register_username
     
                # 通过Flask-Login的login_user方法登录用户
                login_user(curr_user)
                return redirect(url_for('index'))


#针对前端登录模态的登录入口
@app.route('/fast_register', methods=['GET', 'POST'])
@app.route('/fast_login', methods=['GET', 'POST'])
def fast_login():
      
    if request.method == 'GET':
        return render_template('/pc/login.html')
    elif request.method == 'POST':
        print "表单数据"
        # 拿出来用户登录密码
        
        # 用户为登录
        if request.form.get('login_username',None) != None:

            login_username = request.form.get('login_username')
            login_password = request.form.get('login_password')
            #记住我功能
            remember_me_flag = True if request.form.get('remember_me_flag') == u'on' else  False

            print '表单提交数据',request.form
            print login_username,login_password,remember_me_flag

            # 判断交给user_login方法，返回 {'flag':True,"status":''}
            result = Data_Processor.user_login(login_username,login_password)

            # 通过认证，账户密码正确
            if result.get('flag') == True:
            # 这里改成用中间件来验证。

                curr_user = User()
                #  返回用户数据{'status':xxx, 'flag': False, 'user_data': {'username': u'yanggan', 'phone': None, 'email': None, 'id': 5, 'user_type': 1}}
                user_info = Data_Processor.get_user_info(login_username)
                curr_user.id = user_info.get('user_data').get('username') # 给用户名
                # 用用户数据传给data
                curr_user.data =user_info.get('user_data')
                # 通过Flask-Login的login_user方法登录用户
                login_user(curr_user,remember=remember_me_flag)

                # 如果请求中有next参数，则重定向到其指定的地址，
                # 没有next参数，则重定向到"index"视图
                next = request.args.get('next_url')
                # return redirect(url_for('index'))
                return redirect(next or url_for('index'))
            
            # 没有通过认证
            flash(result.get('status'),'login_error')
            return redirect(url_for('login'))
        
        # 用户提交的是注册表单
        elif request.form.get('register_username',None) != None:
            
            # 拿出来数据
            register_username = request.form.get('register_username').strip().lower()  
            register_password = request.form.get('register_password').strip().lower() 
            register_vipcode = request.form.get('register_vipcode').strip().lower()         
            

            print "注册表单数据",request.__dict__
            print "注册时候url给的参数",request.args
            # 不给输入为空,密码不能6位数以下            
            if register_username =='' or  register_password == '':
                result = {'flag':False,"status":'不能输入为空,请重试'}
            elif len(register_password) < 6:
                result = {'flag':False,"status":'密码小于6位数,请重试'}
            else: 
                # 判断交给user_login方法，返回 {'flag':True,"status":''}
                result = Data_Processor.user_register(register_username,register_password,register_vipcode)
                
            if result.get('flag') == False:

                flash(result.get('status'),'register_error')
                current_url = request.args.get('current_url') 
                return redirect('login')

            elif result.get('flag') == True:
               
                # 注册成功，免登陆
                curr_user = User()
                curr_user.id = register_username
     
                # 通过Flask-Login的login_user方法登录用户
                login_user(curr_user)
                next_url = request.args.get('next_url') 
                return redirect(next_url or url_for('index'))


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    # 清除缓存
    # 清除首页的redis缓存
    cache_name = current_user.id if current_user.is_authenticated else 'nologin' 
    R.delete("obj_index_user_"+cache_name)
    # R.delete('page_membership')
    logout_user()
    return redirect(url_for('index'))

                                                                                            

# 首页
@app.route('/',methods=['GET'])
@app.route('/index',methods=['GET'])
@app.route('/course',methods=['GET'])
def index():

    # 加入Redis缓存
    # 有缓存

    cache_name = current_user.id if current_user.is_authenticated else 'nologin' 
    if R.get('obj_index_user_'+ cache_name)!= None:
        print "首页 %s 来自Redis缓存" % ('obj_index_user_'+ cache_name)
        cate_data = eval(R.get('obj_index_user_'+ cache_name))
    else:
        # 缓存过期,重新写入
        cate_data = Data_Processor.get_category_has_status(cookies=request.cookies,user_obj=current_user)
        print '首页缓存写入 %s '% ('obj_index_user_'+ cache_name) 
        R.set('obj_index_user_'+ cache_name,cate_data,ex=CACHE_TIME,nx=True)

    # 获取分类和课程信息
    # cate_data = Data_Processor.get_category_has_status(cookies=request.cookies,user_obj=current_user)
    # dev_data = Data_Processor.get_devtools_data()
    return render_template(
        "course.html",
        category=cate_data.get('category_data'),
        has_active_course=cate_data.get('has_active_course'),
        dev_data=dev_data,
        current_user =current_user
        )



# 课程详情页
@app.route('/course/<int:course_id>',methods=['POST','GET'])
def course_detail(course_id):

    # 加入Redis缓存
    # 有缓存
    if R.get('obj_course_detail_'+str(course_id)) != None:
        print "详情页数据来自Redis缓存"
        course_data = eval(R.get('obj_course_detail_'+str(course_id)))
        print course_data
    else:
        # 缓存过期
        course_data = Data_Processor.get_course_data(course_id)
        print '详情页缓存写入状态：',R.set('obj_course_detail_'+str(course_id),course_data,ex=CACHE_TIME,nx=True)
        

    # 各种数据获取 {'flag':True,'status':'find the course succeed','course_data':return_data}
    # course_data = Data_Processor.get_course_data(course_id)
    # 没有找到课程
    if course_data.get('flag') == False:
        abort(404)
    course_data =  course_data.get('course_data')
    dev_data = Data_Processor.get_devtools_data()
    # 密码字典
    passwd_data = Data_Processor.get_passwd_data(course_data)
    is_free = Data_Processor.get_course_free_status(course_data) 

    if request.method == "GET":

        # 4种情况返回密码字典，免费课程、session、 高级会员、已经兑换过的会员(登录后)、cookies有记录的
        # 判断session,如果有key,value就不用验证了
        # 1、免费课程（登录会员免费）
        if is_free == True:
            
            if current_user.is_authenticated:
                return render_template("course_detail.html",course_data=course_data,passwd_dict=passwd_data,dev_data=dev_data)
            else:
                return render_template("course_detail.html",course_data=course_data,passwd_dict=None,dev_data=dev_data,member_free=True) 
        # 2、登录用户切为VIP用户，直接返回带密码页面
        elif current_user.is_authenticated and current_user.data.get('user_type') == 1:
           return render_template("course_detail.html",course_data=course_data,passwd_dict=passwd_data,dev_data=dev_data) 

        # 3、session有记录 
        elif session.get('course_'+str(course_id)) != None:

            user_input_key =  session.get('course_'+str(course_id))
            print user_input_key

            resp = make_response( \
                render_template("course_detail.html",course_data=course_data,passwd_dict=passwd_data,dev_data=dev_data)
                )
            return resp
        # 4、普通用户，但是有兑换记录
        elif current_user.is_authenticated == True:
            pass
            # 查看是否在用户的该用户的已兑换list中。
            user_course_result = Data_Processor.get_user_courselist(current_user.id)
            user_course_list = user_course_result.get('data') if user_course_result.get('flag') else [] 
            print "登录用户的课程列表为", user_course_list 
            # 判断当前的id是不是在用户的激活课程里面
            if course_id in user_course_list :
                
                # 写入session和cookies中
                session['course_'+str(course_id)] = 'user_login' # 设置session
                print '写入的session:',session
       


                # 返回带密码的数据和写入cookies
                resp = make_response(\
                    render_template("course_detail.html",course_data=course_data,passwd_dict=course_data.get('passwd_dict'),dev_data=dev_data)
                    )
                resp.set_cookie('course_'+str(course_id),'user_login')
                return resp
            else:
                # 返回不带密码的页面
                return render_template("course_detail.html",course_data=course_data,passwd_dict=None,dev_data=dev_data)
                return resp

        # 5、cookies有记录,需要重新验证vaule验证码是否合法（码正确或者为'user_login'）,
        elif request.cookies.get('course_'+ str(course_id)) != None: #有这个课程的cookies
            
            cookie_course_key = request.cookies.get('course_'+ str(course_id))
            # print cookie_course_key 
            # 如果是'标志user_login'，则直接给通过
            if cookie_course_key == 'user_login':

                resp = make_response(\
                    render_template("course_detail.html",course_data=course_data,passwd_dict=course_data.get('passwd_dict'),dev_data=dev_data)
                    )
                return resp

            # 判断数字码是否正确
            verity_result_dict = act.verify_act(course_id,cookies_course_key) #判断code是否有效
            if verity_result_dict['flag'] == True:

                flash(verity_result_dict['status'])
                resp = make_response(\
                    render_template("course_detail.html",course_data=course_data,passwd_dict=course_data.get('passwd_dict'),dev_data=dev_data)
                    )
                return resp
        else:
            # 第一次访问
            return render_template("course_detail.html",course_data=course_data,passwd_dict=None,dev_data=dev_data)


    elif request.method == "POST":
        # 这是个用户输入兑换码后提交到后台来的数据
        # 1、获取兑换码，判断是否有效，是对应课程的兑换码[ 课程 + 兑换码 ]
        # 2、如果有效，则保持兑换码到用户的cookies
        # 3、把兑换码放到session中
        # 4、返回重定向，让浏览器get访问本链接

        user_input_key = request.form.get('key', '')        
        verity_result_dict = Data_Processor.verify_actcode(course_id,user_input_key) # 判断是否正确
    
        if verity_result_dict['flag'] == True: # 成功之后返回

            session['course_'+str(course_id)] = user_input_key # 设置session
            print session
            flash(verity_result_dict['status'])
            redirect_to_course = redirect(url_for('course_detail',course_id=course_id))
            resp = make_response(redirect_to_course)
            resp.set_cookie('course_'+str(course_id),user_input_key) # 设置cookies

            # 清除首页的redis缓存
            cache_name = current_user.id if current_user.is_authenticated else 'nologin' 
            R.delete("obj_index_user_"+cache_name)
            
            return resp # 返回response让浏览器重定向Get访问

        else: #验证失败

            flash(verity_result_dict['status'])
            return redirect(url_for('course_detail',course_id=course_id))


# 通过激活码激活课程
@app.route("/act",methods=['POST','GET'])
def course_activete():
    # pass
    
    # session增加计时器，错误超过5次就不进行验证了，直接返回错误（防爆破解
    
    
    if request.method == 'GET':
        return render_template('act.html')
    elif request.method == 'POST':
        user_input_act = request.form.get('act_code',None) 
        print user_input_act

        if session.get('error_try_count',None) == None:
            session['error_try_count'] = 0
        print "session",session['error_try_count']

        if session['error_try_count'] > 5:

            flash(u'验证错误超过5次，请30分钟后重试', 'act_error')
            result_dict = {'flag':False,'status':"actcode error 5 times",'course_data':None,'error_code':1000}
            return render_template("act.html",result_dict=result_dict)

        # 输入空的验证码
        elif user_input_act == None or user_input_act == '':
            print "没有表单数据"
            flash(u'请输入4位数字兑换码', 'act_error')
            result_dict = {'flag':False,'status':"actcode is empty",'course_data':None,'error_code':900}
            return render_template("act.html",result_dict=result_dict)

        user_input_act = re.search(r'\d{4}',user_input_act).group()  
        # 返回 {'flag':True,'status':"find actcode and course succeed",'course_data':course_data,'error_code':200}
        result_dict = Data_Processor.act_verify(user_input_act)
        
        # 成功
        if result_dict.get('flag') == True: #验证成功
            course_id = str(result_dict.get('course_data').get('course_id'))
            session['course_'+ course_id ] = user_input_act # 设置session
            resp = make_response(redirect(url_for('course_detail',course_id=course_id)))
            resp.set_cookie('course_'+course_id,user_input_act) # 设置cookies
            # 清除首页的redis缓存
            cache_name = current_user.id if current_user.is_authenticated else 'nologin' 
            R.delete("obj_index_user_"+cache_name)
            return resp # 返回response让浏览器重定向Get访问
        
        # 兑换失败
        flash(u'兑换码错误,请核对后重新输入', 'act_error')
        session['error_try_count'] += 1 # 错误一次就计数，超过5次就不能再验证
        return render_template("act.html",result_dict=result_dict)


# 书架列表
@app.route('/books',methods=['POST','GET'])
def books():
    
    # 开启缓存

    # if R.get('obj_bookslist') != None:
    #     print "bookslist页面来自Redis缓存"
    #     cate_data = eval(R.get('obj_bookslist'))
    # else:
    #     cate_data = Data_Processor.get_category_has_bookdata()
    #     print 'bookslist缓存写入'
    #     R.set('obj_bookslist',cate_data,ex=CACHE_TIME,nx=True)

    # 不适用redis缓存
    cate_data = Data_Processor.get_category_has_bookdata()
    print cate_data
    # 获取分类和课程信息
    dev_data = Data_Processor.get_devtools_data()
    return render_template( \
        '/pc/books.html',
        all_books_data = cate_data,
        dev_data=dev_data,
        current_user=current_user 
        )

@app.route('/ways')
@login_required
def ways():
    return "WAYS"


@app.route('/projects')
def projects():
    # 项目导航
    # 获取数据
    project_data =  Data_Processor.get_project_with_nav().get('data')
    return render_template('/pc/projects.html',project_data=project_data,current_user=current_user)


@app.route('/membership',methods=['POST','GET'])
def membership():
    # 价格方案页面
    # 用redis缓存这个页面,缓存1天，只有缓存消失才写入
    
    # if R.get('page_membership') != None:
    #     print "价格页面来自Redis缓存"
    #     return R.get('page_membership')
    # else:
    #     page = render_template('/pc/price.html')
    #     print '价格页面缓存写入',R.set('page_membership',page,ex=CACHE_TIME,nx=True)
    #     return render_template('/pc/price.html')
    return render_template('/pc/price.html',current_user=current_user)


@app.route('/vipactive',methods=['POST','GET'])
@login_required
def vipactive():
    # 会员激活
    if request.method == 'GET':
        return render_template('/pc/vipactive.html')
    elif  request.method == 'POST':
        # 用户登录的前提下
        if current_user.is_authenticated:
            user_input_code = request.form.get('vip_code',None) 
            result = Data_Processor.verify_vipcode(current_user.id,user_input_code)
            if result.get('flag') == True:
                return redirect(url_for('membership'))
            else:
                flash(result.get('status'),'vipcode_error')
                return render_template('/pc/vipactive.html')
        else:
            flash('no login','vipcode_error')
            return render_template('/pc/vipactive.html')

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

# 用户下载课程和密码txt
@app.route('/get_course_txt/<int:course_id>')
def get_course_txt(course_id):
    
    content = "课程导出:\n--------------------\n"
    course_data = Data_Processor.get_course_data(course_id).get('course_data')
    content = content + '\n课程集: 《' + str(course_data.get('course_name')) + "》"

    for resource in course_data.get('course_data'):
        content = content + '\n课程: %s 链接: %s 密码: %s ' % \
                (resource.get('resource_name'),resource.get('resource_addr'),resource.get('resource_passwd'))
    content = content + "\n汇总一次转存链接:%s 密码: %s " % (course_data.get('course_share_url'),course_data.get('course_share_passwd'))
    content = content + '\n\n--------------------\n懒人编程(looncode)IT学院,更多课程资源请访问:http://www.looncode.com' 

    response = make_response(content)
    response.headers["Accept-Language"] = "zh-CN,zh;q=0.8,en;q=0.6"
    response.headers["Content-Disposition"] = "attachment; filename=passwd.txt"
    return response



# SEO推广相关的
@app.route('/rebots.txt',methods=['GET'])
def get_rebots():
    # 返回reboots文件
    rebots_txt = "User-agent: * \nDisallow: \nSitemap: http://looncode.com/static/sitemap/sitemap.txt"
    response = make_response(rebots_txt)
    response.headers["Accept-Language"] = "zh-CN,zh;q=0.8,en;q=0.6"
    response.headers["Content-Disposition"] = "attachment; filename=rebots.txt"
    return response

@app.route('/sitemap.txt',methods=['GET'])
def get_sitemap():
    # 返回reboots文件
    sitemap_txt_path = r'sitemap/sitemap.txt' 
    return  app.send_static_file(sitemap_txt_path)

@app.route('/api/db',methods=['GET'],strict_slashes=False)
@app.route('/api/getdb',methods=['GET'],strict_slashes=False)
def api_get_db():
    # 返回db文件
    directory = os.getcwd()
    print "打印目录",directory # /Users/yg/Documents/code/Project/learoom/serve
    sitemap_txt_path = directory + '/application/db' 
    print sitemap_txt_path
    return  send_from_directory(sitemap_txt_path,filename=r'learoom.db',as_attachment=True)


# 用于验证文件后缀合法
def allowed_file(filename,all_list):
    return '.' in filename and filename.rsplit('.', 1)[1] in all_list

@app.route('/api/upload',methods=['POST',"GET"],strict_slashes=False)
@app.route('/api/uploaddb',methods=['POST',"GET"],strict_slashes=False)
def api_upload_db():
    
    directory = os.getcwd()
    db_path = directory + '/application/db'
    file_path = db_path + "/learoom.db"
    all_list = ['db']
    # 用于更新db文件
    if request.method == "GET":
        return render_template('pc/upload.html')
    elif request.method == "POST":
        f=request.files['dbfile']
        print "文件对象的属性" ,dir(f),f.filename
        if file and allowed_file(f.filename,all_list = ['db']):  #判断文件后缀合法
            filename = secure_filename(f.filename)
            # 老文件备份保存
            liststr = [db_path,'/', 'learoom_bk_', str(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')),'.db'] 
            bk_file_path = "".join(liststr)
            print directory
            print "db_path ",db_path
            print "file_path",file_path
            print "bk_file_path",bk_file_path
            shutil.move(file_path, bk_file_path )
            # 保存新文件
            f.save(file_path)
            return "upload success"
        return "upload error"


@app.route('/api/flushredis',methods=['POST',"GET"],strict_slashes=False)
@app.route('/api/resetredis',methods=['POST',"GET"],strict_slashes=False)
def api_flush_redis():
    # 清空所有缓存
    R.flushdb()   
    return '成功清空所有缓存'

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404




# 移动端站点的view
@app.route('/m',methods=['GET'])
@app.route('/m/course',methods=['GET'])
@app.route('/m/home',methods=['GET'])
def mobile_home():

    # 加入Redis缓存
    # 有缓存
    cache_name = current_user.id if current_user.is_authenticated else 'nologin' 
    if R.get('obj_m_index_user_'+ cache_name)!= None:
        print "mobile首页数据来自Redis缓存"
        cate_data = eval(R.get('obj_m_index_user_'+ cache_name))
    else:
        # 缓存过期,重新写入
        cate_data = Data_Processor.get_category_has_status(cookies=request.cookies,user_obj=current_user)
        print 'mobile首页缓存写入'
        R.set('obj_m_index_user_'+ cache_name,cate_data,ex=CACHE_TIME,nx=True)

    # cate_data = Data_Processor.get_category_has_status(cookies=request.cookies)
    dev_data = Data_Processor.get_devtools_data()
    return render_template(
        "/mobile/m_home.html",
        category=cate_data.get('category_data'),
        has_active_course=cate_data.get('has_active_course'),
        dev_data=dev_data
        )

@app.route('/m/course/<int:course_id>',methods=['POST','GET'])
def mobile_course_detail(course_id):
    
    # 加入Redis缓存
    # 有缓存
    if R.get('obj_course_m_detail_'+str(course_id)) != None:
        print "mobile详情页数据来自Redis缓存"
        course_data = eval(R.get('obj_course_m_detail_'+str(course_id)))
        print course_data
    else:
        # 缓存过期
        course_data = Data_Processor.get_course_data(course_id)
        print 'mobile详情页缓存写入状态：'
        R.set('obj_course_m_detail_'+str(course_id),course_data,ex=CACHE_TIME,nx=True)


    # # 获取数据
    # course_data = Data_Processor.get_course_data(course_id)
    # 没有找到课程
    if course_data.get('flag') == False:
        abort(404)
    course_data =  course_data.get('course_data')
    dev_data = Data_Processor.get_devtools_data()
    passwd_data = Data_Processor.get_passwd_data(course_data)
    is_free = Data_Processor.get_course_free_status(course_data)


    if request.method == "GET":

        # 3种情况，1、第一次访问，2、输入兑换码后，重定向访问，这时候需要返回带密码页面
        # 0、限免课程，直接返回数据
        # 1、读取用户的cookies和session，把兑换码拿出来，匹配是否是这门课程的对缓慢
        # 2、如果是这门课程的兑换码，则返回带提取密码数据的页面
        # 3、如果不是，则返回普通的页面
        # 判断session,如果有key,value就不用验证了
        if is_free == True:
            
            return render_template("/mobile/m_course_detail.html",course_data=course_data,passwd_dict=passwd_data,dev_data=dev_data)
        
        elif session.get('course_'+str(course_id)) != None:

            user_input_key =  session.get('course_'+str(course_id))
            print user_input_key

            resp = make_response( \
                render_template("/mobile/m_course_detail.html",course_data=course_data,passwd_dict=passwd_data,dev_data=dev_data)
                )
            return resp

        # 判断cookies,需要重新验证vaule验证码是否合法
        elif request.cookies.get('course_'+ str(course_id)) != None: #有这个课程的cookies
            
            cookie_course_key = request.cookies.get('course_'+ str(course_id))
            print cookie_course_key 
            verity_result_dict = act.verify_act(course_id,cookies_course_key) #判断code是否有效
            if verity_result_dict['flag'] == True:

                flash(verity_result_dict['status'])
                resp = make_response(\
                    render_template("/mobile/m_course_detail.html",course_data=course_data,passwd_dict=course_data.get('passwd_dict'),dev_data=dev_data)
                    )
                return resp
        else:
            # 第一次访问
            return render_template("/mobile/m_course_detail.html",course_data=course_data,passwd_dict=None,dev_data=dev_data)

    elif request.method == "POST":
        # 这是个用户输入兑换码后提交到后台来的数据
        # 1、获取兑换码，判断是否有效，是对应课程的兑换码[ 课程 + 兑换码 ]
        # 2、如果有效，则保持兑换码到用户的cookies
        # 3、把兑换码放到session中
        # 4、返回重定向，让浏览器get访问本链接

        user_input_key = request.form.get('key', '')        
        verity_result_dict = Data_Processor.verify_actcode(course_id,user_input_key) # 判断是否正确

        if verity_result_dict['flag'] == True: # 成功之后返回

            session['course_'+str(course_id)] = user_input_key # 设置session
            print session
            flash(verity_result_dict['status'],'success')
            redirect_to_course = redirect(url_for('mobile_course_detail',course_id=course_id))
            resp = make_response(redirect_to_course)
            resp.set_cookie('course_'+str(course_id),user_input_key) # 设置cookies
            return resp # 返回response让浏览器重定向Get访问

        else: #验证失败

            flash("兑换码错误,请核对后重新输入",'act_error')
            return redirect(url_for('mobile_course_detail',course_id=course_id))


# 通过激活码激活课程
@app.route("/m/act",methods=['POST','GET'])
def mobile_course_activete():
    # pass
    if request.method == 'GET':
        return render_template('/mobile/m_act.html')
    elif request.method == 'POST':
        user_input_act = request.form.get('act_code',None) 
        print "测试用户输入数据",user_input_act

        # 错误一次就计数，超过5次就不能再验证
        if session.get('error_try_count',None) == None:
            session['error_try_count'] = 0
        # print "session",session['error_try_count']
        if session['error_try_count'] > 5:
            flash(u'验证错误超过5次，请30分钟后重试', 'act_error')
            result_dict = {'flag':False,'status':"actcode error 5 times",'course_data':None,'error_code':1000}
            return render_template("/mobile/m_act.html",result_dict=result_dict)

        # 输入空的验证码
        if user_input_act == None or user_input_act == '':
            print "没有表单数据"
            flash(u'请输入4位数字兑换码', 'act_error')
            result_dict = {'flag':False,'status':"actcode is empty",'course_data':None,'error_code':900}
            return render_template("mobile/m_act.html",result_dict=result_dict)

        user_input_act = re.search(r'\d{4}',user_input_act).group()  
        # 返回 {'flag':True,'status':"find actcode and course succeed",'course_data':course_data,'error_code':200}
        print "测试用户输入数据,啦啦啦啦啦",user_input_act
        result_dict = Data_Processor.act_verify(user_input_act)
        
        # 成功
        if result_dict.get('flag') == True: #验证成功
            course_id = str(result_dict.get('course_data').get('course_id'))
            session['course_'+ course_id ] = user_input_act # 设置session
            resp = make_response(redirect(url_for('mobile_course_detail',course_id=course_id)))
            resp.set_cookie('course_'+course_id,user_input_act) # 设置cookies
            return resp # 返回response让浏览器重定向Get访问
        # 兑换失败
        flash(u'兑换码错误,请核对后重新输入', 'act_error')
        session['error_try_count'] += 1 # 错误一次就计数，超过5次就不能再验证
        return render_template("/mobile/m_act.html",result_dict=result_dict)


@app.route("/m/my",methods=['POST','GET'])
def mobile_my():
    cate_data = Data_Processor.get_category_has_status(cookies=request.cookies,user_obj=current_user)
    dev_data = Data_Processor.get_devtools_data()
    return render_template(
        "/mobile/m_my.html",
        category=cate_data.get('category_data'),
        has_active_course=cate_data.get('has_active_course'),
        dev_data=dev_data
        )
