
# 开发文档

> 基于django+mysql开发的家政预约管理系统，本文档包括功能说明、数据库设计、开发过程。学习过程遇到问题可以咨询作者：lengqin1024（微信）

## 功能说明

- 家政管理（包括家政的新增、查询、删除、编辑功能）
- 服务管理（包括服务的新增、查询、删除、编辑功能）
- 标签管理（包括标签信息的新增、查询、删除、编辑功能）
- 预约管理（包括预约的新增、查询、删除、编辑功能）
- 用户管理（包括用户和管理员的新增、查询、删除、编辑、演示账号功能）
- 日志管理（包括日志的新增、查询、删除功能，通过日志查看系统访问情况）
- 统计分析（包括小区的人数统计、小区统计等功能）

## 数据库设计

```

// 家政表
Table thing {
    thing_id int [pk]
    classification_id int [ref: > C.classification_id]
    tag_id int [ref: <> tag.tag_id]
    user_id int [ref: > user.user_id] //所属用户（一对一）
    title varchar
    cover varchar
    price varchar // 价格
    status int // 上线0 下架1
    description text
    mobile varchar 
    age varchar 
    sex varchar 
    location varchar
    create_time datetime
    pv int
    wish_count int
    recommend_count int
    wish int [ref: <> user.user_id]
    collect int [ref: <> user.user_id]
 }
 
 // 服务表
 Table classification as C {
   classification_id int [pk]
   pid int
   title varchar
   create_time datetime
 }
 
 Table tag {
   tag_id int [pk]
   title varchar
   create_time datetime
 }
 
 Table comment {
   comment_id int [pk]
   content varchar
   user_id int [ref: > user.user_id]
   thing_id int [ref: > thing.thing_id]
   comment_time datetime
   like_count int
 }
 
 Table user {
   user_id int [pk]
   role varchar // 1管理员 2普通用户 3演示帐号
   status int // 0正常 1封号
   username varchar
   password varchar
   nickname varchar
   avatar varchar
   description varchar
   wish int [ref: <> thing.thing_id]
   email varchar
   mobile varchar
   score int // 积分
   push_email varchar // 推送邮箱
   push_switch int  // 推送开关
   token varchar
   admin_token varchar
 }
 
//   Table role {
//   role_id int [pk]
//   title varchar
//   remark varchar
//   create_time datetime
// }
 
 
 Table record {
   record_id int [pk]
   user_id int [ref: > user.user_id]
   classification_id int [ref: > C.classification_id]
   thing_id int [ref: > thing.thing_id]
   title varchar
   record_time varchar
 }
 
 
 Table login_log {
   log_id int [pk]
   username varchar
   ip varchar
   log_time datetime
 }
 
 // 操作日志
 Table op_log {
   id int [pk]
   re_ip varchar
   re_time datetime
   re_url varchar
   re_method varchar
   re_content varchar
   access_time varchar
 }
 
 // 异常日志
 Table error_log {
   id int [pk]
   ip varchar
   method varchar
   content varchar
   log_time varchar
 }
 
 Table order {
   order_id int [pk]
   user_id int [ref: > user.user_id]
   thing_id int [ref: > thing.thing_id]
   status varchar // 1未支付 2已支付 7订单取消
   create_time datetime
   pay_time datetime // 支付时间
   receiver_name varchar // 收货人姓名
   receiver_address varchar // 地址
   receiver_phone varchar // 收货人电话
   remark varchar // 备注
 }
 
 
 
 Table banner {
   id int [pk]
   image varchar
   thing_id int [ref: > thing.thing_id]
   create_time datetime
 }
 
 
 
 Table ad {
   id int [pk]
   image varchar
   link varchar
   create_time datetime
 }
 
 
 
 Table notice {
   id int [pk]
   content varchar
   create_time datetime
 }
 
 

 
 
```

## 开发过程

后端功能的开发使用django和djangorestframework技术。
关于django的学习，可以参考[这里](https://docs.djangoproject.com/zh-hans/5.0/)。
关于djangorestframework的学习，可以参考[这里](https://www.django-rest-framework.org/)。

无论是用户管理、家政管理、服务管理等功能都是基于django的restframework框架开发的，开发流程是：
- 第一步：编写model模型
- 第二步：编写序列化器
- 第三步：编写view视图
- 第四步：配置url接口地址


下面用家政管理功能来演绎这个流程，其它的管理功能都是这个流程
  

**家政管理功能开发**
 
1. 编写models数据库模型

在models.py中新建业主模块，然后编写模型代码。如下：
```
class Thing(models.Model):
    STATUS_CHOICES = (
        ('0', ''),
        ('1', ''),
    )
    id = models.BigAutoField(primary_key=True)
    classification = models.ForeignKey(Classification, on_delete=models.CASCADE, blank=True, null=True,
                                       related_name='classification_thing')
    title = models.CharField(max_length=30, blank=True, null=True)
    address = models.CharField(max_length=130, blank=True, null=True)
    mobile = models.CharField(max_length=30, blank=True, null=True)
    remark = models.CharField(max_length=30, blank=True, null=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='0')
    create_time = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = "b_thing"
```

2. 编写序列化器

在serializers.py中新增ThingSerializer并写入：
```
class ThingSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    # 额外字段
    classification_title = serializers.ReadOnlyField(source='classification.title')

    class Meta:
        model = Thing
        fields = '__all__'
```


3. 编写view业务代码

在views中新建thing.py文件，然后编写增删改查的代码。如下所示：
```

@api_view(['GET'])
def list_api(request):
    if request.method == 'GET':
        keyword = request.GET.get("keyword", None)
        c = request.GET.get("c", None)
        tag = request.GET.get("tag", None)
        if keyword:
            things = Thing.objects.filter(name__contains=keyword).order_by('-create_time')
        elif c:
            classification = Classification.objects.get(pk=c)
            things = classification.classification_thing.all()
        elif tag:
            tag = Tag.objects.get(id=tag)
            print(tag)
            things = tag.thing_set.all()
        else:
            things = Thing.objects.all().order_by('-create_time')

        serializer = ThingSerializer(things, many=True)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)


@api_view(['GET'])
def detail(request):

    try:
        pk = request.GET.get('id', -1)
        thing = Thing.objects.get(pk=pk)
    except Thing.DoesNotExist:
        utils.log_error(request, '对象不存在')
        return APIResponse(code=1, msg='对象不存在')

    if request.method == 'GET':
        serializer = ThingSerializer(thing)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def create(request):

    if isDemoAdminUser(request):
        return APIResponse(code=1, msg='演示帐号无法操作')

    serializer = ThingSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return APIResponse(code=0, msg='创建成功', data=serializer.data)
    else:
        print(serializer.errors)
        utils.log_error(request, '参数错误')

    return APIResponse(code=1, msg='创建失败')


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def update(request):

    if isDemoAdminUser(request):
        return APIResponse(code=1, msg='演示帐号无法操作')

    try:
        pk = request.GET.get('id', -1)
        thing = Thing.objects.get(pk=pk)
    except Thing.DoesNotExist:
        return APIResponse(code=1, msg='对象不存在')

    serializer = UpdateThingSerializer(thing, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return APIResponse(code=0, msg='查询成功', data=serializer.data)
    else:
        print(serializer.errors)
        utils.log_error(request, '参数错误')

    return APIResponse(code=1, msg='更新失败')


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def delete(request):

    if isDemoAdminUser(request):
        return APIResponse(code=1, msg='演示帐号无法操作')

    try:
        ids = request.GET.get('ids')
        ids_arr = ids.split(',')
        Thing.objects.filter(id__in=ids_arr).delete()
    except Thing.DoesNotExist:
        return APIResponse(code=1, msg='对象不存在')
    return APIResponse(code=0, msg='删除成功')

```

4. 配置url接口访问地址

在urls.py中添加刚才写的业务代码即可。如下
```
    path('admin/thing/list', views.admin.thing.list_api),
    path('admin/thing/create', views.admin.thing.create),
    path('admin/thing/update', views.admin.thing.update),
    path('admin/thing/delete', views.admin.thing.delete),
```

