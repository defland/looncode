# coding:utf-8
from model import *



def init_course():

    print Course.add_course([
        {
            'id':10000,
            'name':u'Html/CSS/Bootstrap免费课程包',
            'description':u'WEB最基础的内容学习',
            'img_url':"/static/img/course/html.png",
            'category_id':1000,
            'is_free':True
        },
        {
            'id':None,
            'name':u'Javascript/JQuery课程包',
            'description':u'前端开发的必学语言',
            'img_url':"/static/img/course/js.png",
            'category_id':1000
        },        
        {
            'id':None,
            'name':u'Vue.js框架汇总课程包',
            'description':u'轻量级的前端JS框架',
            'img_url':"/static/img/course/vue2.png",
            'category_id':1000
        },
        {
            'id':None,
            'name':u'React/RNative框架汇总课程包',
            'description':u'来自Facebook的JS框架',
            'img_url':"/static/img/course/react.jpg",
            'category_id':1000
        },
        {
            'id':None,
            'name':u'Angular1-4框架汇总课程包',
            'description':u'来自Google开发的前端JS框架',
            'img_url':"/static/img/course/angular.jpg",
            'category_id':1000
        },
        {
            'id':None,
            'name':u'前端Photoshop入门课程包',
            'description':u'前端切图必学必会',
            'img_url':"/static/img/course/ps.jpg",
            'category_id':1000,
            'is_free':True
        },
        {
            'id':None,
            'name':u'Java基础&Web汇总课程包',
            'description':u'Java所有课程包',
            'img_url':"/static/img/course/java.png",
            'category_id':1001,
        },
        {
            'id':None,
            'name':u'PHP基础&Laravel框架汇总课程包',
            'description':u'PHP基础&laravel框架汇总课程包',
            'img_url':"/static/img/course/php.png",
            'category_id':1001,
        },

        # python / 全栈

        {
            'id':None,
            'name':u'Python基础&框架全栈课程包',
            'description':u'Python基础&框架全栈课程包',
            'img_url':"/static/img/course/python.png",
            'category_id':1002,
        },

        {
            'id':None,
            'name':u'Node.js基础&全栈课程包',
            'description':u'Node.js基础&全栈课程包',
            'img_url':"/static/img/course/nodejs.jpg",
            'category_id':1002,
        },

        # 移动端开发

        {
            'id':None,
            'name':u'Android入门&项目汇总课程包',
            'description':u'Android入门&项目汇总课程包',
            'img_url':"/static/img/course/android.png",
            'category_id':1003,
        },
        {
            'id':None,
            'name':u'iOS开发入门&项目汇总课程包',
            'description':u'iOS开发入门&项目汇总课程包',
            'img_url':"/static/img/course/ios.png",
            'category_id':1003,
        },

        # 运维开发
        {
            'id':None,
            'name':u'linux入门&运维汇总课程包',
            'description':u'linux入门汇总课程包',
            'img_url':"/static/img/course/linux.png",
            'category_id':1004,
        },
        {
            'id':None,
            'name':u'OpenStack/hadoop等汇总课程包',
            'description':u'OpenStack/hadoop等框架课程包',
            'img_url':"/static/img/course/opdev.png",
            'category_id':1004,
        },

        # linux

        {
            'id':None,
            'name':u'Mysql/Sqlserver/Orache课程包',
            'description':u'Mysql/Sqlserver/Orache/Postgre课程包',
            'img_url':"/static/img/course/sql.png",
            'category_id':1005,
        },

        {
            'id':None,
            'name':u'Mongodb非关系型汇总课程包',
            'description':u'Mongodb非关系型汇总课程包',
            'img_url':"/static/img/course/nosql.jpg",
            'category_id':1005,
        },

        # 数据分析

        {
            'id':None,
            'name':u'R语言学习汇总课程包',
            'description':u'R语言学习汇总课程包',
            'img_url':"/static/img/course/r.png",
            'category_id':1006
        },
        {
            'id':None,
            'name':u'数据结构/编程算法课程包',
            'description':u'数据结构/编程算法课程包',
            'img_url':"/static/img/course/alg.png",
            'category_id':1006
        },
        {
            'id':None,
            'name':u'深度学习理论汇总课程包',
            'description':u'深度学习理论汇总课程包',
            'img_url':"/static/img/course/deep.png",
            'category_id':1006
        },        
        {
            'id':None,
            'name':u'C/C++基础&项目课程包',
            'description':u'C/C++基础&项目课程包',
            'img_url':"/static/img/course/c.png",
            'category_id':1006
        },
        # 其他
        {
            'id':None,
            'name':u'限免课程包',
            'description':u'限免分享课程',
            'img_url':"/static/img/course/free.png",
            'category_id':1007,
            'is_free':True
        }

    ])
    return "init course OK"

def init_resouce():
    print Resource.add_resource([

            {
                'id':600000,
                'name':u'Html入门到精通视频合集',
                'content_type':1,
                'url':"http://pan.baidu.com/s/1c1OgW3A",
                'passwd':'yhaa',
                'size':'3.2',
                'course_id':10000

            }

    ])
    return "init resource ok"

def add_resouce():
    print Resource.add_resource([

            {
                'id':None,
                'name':u'Bootstrap入门到精通视频合集',
                'description':'',
                'url':"http://pan.baidu.com/s/1c1OgW3A",
                'content_type':2,
                'size':'3.2',
                'passwd':'dead',
                'course_id':10001

            },
            {
                'id':None,
                'name':u'Bootstrap入门到精通视频合集',
                'url':"http://pan.baidu.com/s/1c1OgW3A",
                'description':'',
                'content_type':2,
                'size':'3.2',
                'passwd':'dead',
                'course_id':10001

            },
            {
                'id':None,
                'name':u'Bootstrap入门到精通视频合集',
                'description':'',
                'url':"http://pan.baidu.com/s/1c1OgW3A",
                'content_type':2,
                'size':'3.2',
                'passwd':'dead',
                'course_id':10001

            },            
            {
                'id':None,
                'name':u'Bootstrap入门到精通视频合集',
                'description':'',
                'url':"http://pan.baidu.com/s/1c1OgW3A",
                'content_type':2,
                'size':'3.2',
                'passwd':'dead',
                'course_id':10001

            }

    ])
    return "add resource ok"


def init_category():

    x = [
        u'Web前端',
        u'Java&PHP开发',
        u'Python&全栈',
        u'移动端开发',
        u"运维开发",
        u'数据库',
        u'数据&算法',
        u'其他'
        ] 

    return Category.init_category(x)

# # 这个部分先写方法 
# class Course_Man(object):
#     """
#     1、获取所有课程分类，和分类地下课程
#     2、获取单门课程的的信息，包含资源
#     3、获取单门课程的


#     """
#     def __init__(self):
#         pass
        
# class Act_Man(object):
#     """
#     1、生成兑换码
#     2、查询、修改兑换码
#     3、使用兑换码，验证兑换码是否有效

#     """
#     def __init__(self):
#         pass

#     def creat_act(self):
#         pass

#     def verify_act(self,course_id,act_code):
        
#         print("接受到的课程ID和兑换码")
#         print(course_id,act_code)
#         x = {'flag':False,'status':"兑换码不正确，请联系客服"}
#         y = {'flag':True,'status':"兑换成功"}

#         return y

# act = Act_Man()

# 初始化兑换码
def init_actcode():
    #初始化兑换码
    return Actcode.init_unique_actcode(30)

def renew_course_size():
    # 更新课程文件大小
    return Course.count_course_size()
def add_actcode():

    return Actcode.add_actcode(10000,20)


# 添加书单

def add_bookslist():

    x = [

        {'id':800,'name':u'HMTL小白零基础书单推荐','category_id':1000},
        {'name':u'Javascript入门书籍合集','category_id':1000}

    ]
    return Bookslist.add_bookslist(x)

def add_book_with_isbn(isbn_list=None,booklist=800):

    for isbn in isbn_list:

        book_data = Book.get_bookinfo_with_api(isbn)
        book_data["book_buy_url"] = u"www.baiud.com"
        book_data["book_download_url"] = u""   
        book_data["bookslist_id"] = booklist

        print Book.add_book([book_data])

    return ""

# 添加书本 
def add_book():

    # book_id = book.get('book_id'),
    # book_name = book.get('book_name'),
    # book_isbn = book.get('book_isbn'),
    # book_author = book.get('book_author'),
    # book_mark = book.get('book_mark'),
    # book_img_url = book.get('book_img_url'),
    # book_download_url = book.get('book_download_url'),
    # book_buy_url = book.get('book_buy_url'),
    # bookslist_id= book.get('bookslist_id'),
    x = [
        {
            'book_id':None,
            'book_name':u"html必知必会",
            'book_desc':u'这里是介绍'[:16] + u"...",
            'book_isbn':u'320392031',
            'book_author':u'张大仙',
            'book_mark':u'7.0',
            'book_img_url':u'https://img3.doubanio.com/lpic/s3140466.jpg',    
            'book_download_url':u'http://booksobject-1253118766.file.myqcloud.com/bookbk.jpg',
            'book_buy_url':u'http://www.baidu.com',
            'bookslist_id':800,
        }
    ]

    return Book.add_book(x)

def test_get_cate_with_bookslist():

    x =  Category.get_bookslist_category()
    print x
    return x


def add_project_type(data=[]):
    # 添加分类
    data = {

        'id':None,
        'name':'算法',
        'img_url':r'/static/img/project-nav/suanfa.png'
    }

    return Project_Type.add_type(data)


def add_project(data=[]):
    # 添加分类
    data = {

        'id':None,
        'name':'QMUI',
        'desc':'腾讯QMUITeam出品的UI框架，涵盖的WEB/IOS/Android3个领域。',
        'tag':'UI框架',
        'project_url':r'http://qmuiteam.com?url=looncode.com',
        'projects_type_id':14,
        'is_free':True
    }

    return Projects.add_project(data)

def get_log():
    pass
    return Update_Log.get_meassage()

def get_project():
    return Project_Type.get_all_data()

if __name__ == "__main__":

    import sys  
    reload(sys)  
    sys.setdefaultencoding('utf8')  
    # print init_category()
    # print init_course()
    # print init_resouce()
    # print add_resouce()
    # print init_actcode()
    # print renew_course_size()
    
    # print add_bookslist() 9787302255659, 
    # print add_book()
    # print add_book_with_isbn([9787121137679,9787121060748,9787115332912,9787121126475, 9787121148750,9787111226789,9787302228318, 9787111398790],booklist=819)
    # print test_get_cate_with_bookslist()
    pass
    # print Vipcode.init_vipcode(50)
    # print add_project_type()
    # print add_project()
    # print get_project()

    print get_log()

