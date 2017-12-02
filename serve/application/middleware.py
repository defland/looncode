# coding:utf-8
from model import *
from dev_tools import *

import re

class Data_Processor(object):
    """
    docstring for Data_Processor
    1、数据流: model(db) -> Processor -> view -> templates -> browser
    2、业务流：
        - 获取分类数据
        - 分类数据加工
        - 获取课程详细数据
        - 验证兑换码

    """
    def __init__(self):
        pass

    @staticmethod
    def get_category():
        # 获取分类
        pass
        return Category.get_category()
    
    @staticmethod
    def get_user_courselist(username=None):
        # 获取普通用户的绑定课程列表
        if username == None:
            return {'flag':False,'status':'no username','data': None}
        return Userlist.binding_course(username)


    @staticmethod
    def get_category_has_status(cookies=None,user_obj=None):
        #  前台显示已经兑换课程的功能,加工分类,获取所有课程数据（带激活标识）+激活的课程数据
        new_category_data = []
        active_courses_list = []
    
        # 把keys拿出来,判断哪些课程已经兑换过
        cookies_keys_list = cookies.keys()
        # for出来cookies里面保存的已经兑换的课程id
        cookies_str = ''.join(cookies_keys_list)
        # print "test",long_str
        active_courses_list = re.findall(r'course_(\d+)',cookies_str)
        has_active_course = False
        
        # 这里是处理处理 active_list
        if active_courses_list != [] or  user_obj.is_authenticated == True:
            has_active_course = True
            # 从cookies构造出来active_list
            active_courses_list = [ int(x) for x in active_courses_list ]        
            # print active_courses_list,type(active_courses_list[0]) # 如 ['10000']
            

            # 有用户登录的前提下,[绑定已兑换课程]，cookies课程+user已绑定课程=新列表，新列表放入用户绑定。
            if user_obj != None and user_obj.is_authenticated == True:
                # vip用户直接激活所有课程
                if user_obj.data.get('user_type') == 1:
                    new_data = Category.get_category(vip_user=True)
                    return {'category_data':new_data,'has_active_course':has_active_course } 

                # 普通用户的判断。
                # 取出用户已经绑定课程
                username = user_obj.id # 用户名
                get_user_result = Userlist.get_user(username)
                user_obj = get_user_result.get('obj')
                user_id = user_obj.user_id

                print "用户对象所有属性",user_obj.user_course_record
                print "cookies激活的课程list",active_courses_list
                old_user_course_list = [i.course_id for i in user_obj.user_course_record ]
                print 'old 次用户激活的课程list',old_user_course_list
                all_course_list = list(set(active_courses_list).union(set(old_user_course_list)))
                print  '2个的交集',all_course_list
                wait_add_list = list(set(active_courses_list)-set(old_user_course_list))
                print "需要添加哈哈哈",wait_add_list
                
                print "进行到这里"

                # 把all_list 写入用户关系表,绑定用户和课程
                x = User_Course.add_binding(user_id=user_id,course_code_list=wait_add_list)
                
                print "进行到这里"
                # 获取all_course的对应分类信息
                print "传入之前的数据",all_course_list
                new_data = Category.get_category(is_active_id=all_course_list)
                return {'category_data':new_data,'has_active_course':has_active_course } 

            else:

                # 用户未登录
                # 通过model的getcategory获取所有课程数据（带激活标识）+激活的课程数据             
                new_data = Category.get_category(is_active_id=active_courses_list)
                return {'category_data':new_data,'has_active_course':has_active_course } 
        
        # cookies没有课程记录
        else:
            return {'category_data':Category.get_category(),'has_active_course':has_active_course }  
        

    @staticmethod
    def verify_actcode(course_id,user_input_key):
        #  验证兑换码
        pass
        return Actcode.verify_actcode(course_id,user_input_key)

    @staticmethod
    def get_course_data(course_id):
        # 获取课程数据
        pass
        return Course.get_one_course(course_id)

    @staticmethod
    def get_devtools_data():
        # 获取课程数据
        # 开启或者关闭调试信息功能
        # show_git_data()
        if config["default"].GIT_VERSION_DISPLAY:
            
            git_data = show_git_data()
            dev_data = {
                'flag':config["default"].GIT_VERSION_DISPLAY,
                'git': git_data
            }
        else:

            dev_data = {
                'flag':config["default"].GIT_VERSION_DISPLAY,
            }

        return dev_data
    
    @staticmethod
    def get_passwd_data(course_data):
        # 获取课程id+密码的dict
        pass
        return course_data.get('passwd_dict')
    @staticmethod
    def get_course_free_status(course_data):

        pass
        return course_data.get('course_is_free')

    @staticmethod
    def act_verify(user_input_act=None):
        # 给验证码，验证对应课程
        # 返回flash
        
        if user_input_act == None:
            print "没有表单数据"
            return {'flag':False,'status':'no act code','flash':'未输入兑换码'}
        user_input_act = re.search(r'\d{4}',user_input_act).group() 
        print "用户输入数据：",user_input_act
        result = Actcode.verify_only_actcode(user_input_act)
        return result
    @staticmethod
    def get_category_has_bookdata():
        # 查询书籍分类
        x =  Category.get_bookslist_category()
        return x

    @staticmethod
    def user_login(username,password):
        pass
        # 检查用户名
        # 插件是否有此用户,没有找到就返回
        if Userlist.check_useranme(username) == True:
            return {'flag':False,'status':'username or password is error'}
        # 验证账户密码
        result = Userlist.verify_user(username,password)

        return result

    @staticmethod
    def user_register(username=None,password=None,vip_code=None):
        # 交给model
        # 验证vipcode的有效性
        code_result = Vipcode.verify_code(vipcode=vip_code,active_flag=True,username=username)
        vip_code_flag = code_result.get('flag')
        # 验证VIP兑换码有效性
        if vip_code_flag == True:
            result = Userlist.add_user(username,password,user_type=1)
        else:
            result = Userlist.add_user(username,password,user_type=0)

        return result

    @staticmethod
    def get_user_info(username=None):

        return Userlist.get_user_info(username)

    @staticmethod
    def verify_vipcode(username=None,vip_code=None):
        # 检查码。修改会员类型、废除码有效性。
        
        code_result = Vipcode.verify_code(vipcode=vip_code,active_flag=True,username=username)
        # 让用户变为VIP
        if code_result.get('flag') == True:
            return Userlist.become_vip(username=username,vipcode=vip_code)

        else:
            return code_result

       


