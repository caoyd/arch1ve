#人脸相似度检测API
用户通过上传包含人脸的照片，API返回两张照片中的人脸相似度。

### 1. API调用说明
###### URL
`/match`
###### 请求方法
`POST`
###### 请求内容
`通过HTML表单方式上传图片(即以"multipart/form-data"方式)，两个文件表单名称为'pic1'跟'pic2'`
###### 上传图片大小
`4M以内`
### 2. 结果返回说明
#### 返回码 `200`
	{
		"same_person": false,
		"similarity": "5.68%",
		"face1_detected": "yes",
		"face2_detected": "yes"
	}






参数名称 | 参数值 | 说明
------------ | ------------- | ------------
same_person | 布尔值  | true:人脸属于同一个人，false:人脸属于不同的人
similarity | 百分数  | 上传图片中两个人脸的相似度
face1_detected | 布尔值 | true:第一张图片中检测到人脸，false:未检测到人脸
face2_detected | 布尔值 | true:第二张图片中检测到人脸，false:未检测到人脸


#### 返回码 `400`
	{"error": "Bad Request"}

错误的请求: 提交图片不完整, HTTP Content-Type不正确等

#### 返回码 `500`
	{"error": "API Backend Error "}
API后台错误: 调用MicrosoftAPI错误,超时等

***
***
***
# Microsoft Cognitive Service

## Account
#### [ Unused ]
* 996077635@qq.com
* 3120922909@qq.com

#### [ Test ] 
* ski2per@163.com
* 67784480@qq.com

## API参考
## 1 脸部列表API
### 1.1 返回所有的脸部列表
###### URL

`/facelist`
###### 调用方法 `GET`

###### 调用成功返回JSON格式

	[
		{
			"face_list_id": "my_facelist_1",
			"desc": "描述1"
		}，
		{
			"face_list_id": "my_facelist_1",
			"desc": "描述2"
		}，
		{
			"face_list_id": "my_facelist_1",
			"desc": "描述3"
		}
	]

### 1.2 创建脸部列表（CREATE）
###### URL：

`/facelist/create`
###### 调用方法 `POST`：
1 **JSON**

`JSON格式`


	{
		"face_list_id": "my_face_list",
		"desc":"我的面部列表"
	}
2 **表单**

`表单元素`

 元素名称     | 控件类型
-------------|--------
face_list_id |文本
desc         |文本

###### 调用成功返回JSON格式

	空

### 1.3 删除脸部列表(DELETE)
###### URL

`/facelist/delete`
###### 调用方法 `POST`:
1 **JSON**

`JSON格式`

	{
		"face_list_id": "my_face_list"
	}
2 **表单**

`表单元素`

 元素名称     | 控件类型
-------------|--------
face_list_id |文本
	
###### 调用成功返回JSON格式

	空

### 1.4 返回指定脸部列表中的所有脸部(GET)
###### URL

`/facelist/get`

###### 调用方法 `POST`:
1 **JSON**

`JSON格式`

	{
		"face_list_id": "my_face_list"
	}
2 **表单**

`表单元素`

元素名称     | 控件类型
-------------|--------
face_list_id |文本
	
###### 调用成功返回JSON格式

	[
  		{
    		"face_id": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX",
    		"desc": "描述"
  		}，
  		{
  			"face_id": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX",
  			"desc": "描述"
  		}
	]
### 1.5 向指定脸部列表中添加脸部(ADD)
###### 调用方法 `POST`:
1 **图片流**

`URL`:

	/facelist/add?face_list_id=my_face_list&desc=描述
	
`调用方法`

	将图片字节流放入HTTP message body发送

2 **表单**

`URL`:

	/facelist/add

`表单元素`

 元素名称     | 控件类型
-------------|--------
face_list_id |文本
desc         |文本
uploac_pic	 |文件
	
###### 调用成功返回JSON格式
	
	{
		"face_id": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"
	}

### 1.6 从指定FaceList移除Face(REMOVE)
###### URL

`/facelist/remove`

###### 调用方法 `POST`:
1 **JSON**

`JSON格式`

	{
		"face_list_id": "my_face_list"
		"face_id": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"
	}

2 **表单**

`表单元素`

 元素名称     | 控件类型
-------------|--------
face_list_id |文本
face_id      |文本
###### 调用成功返回JSON格式

	空
## 2 Face API
### 2.1 脸部分析
`URL`

	/face/detect
`调用方法`

	POST
`请求方式`

	将图片字节流放入HTTP message body发送
`调用成功返回JSON格式`

	[
  		{
    		"age": 27.8,
    		"glass": "no",
    		"face_id": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX",
    		"gender": "female"
  		},
  		{
    		"age": 46.2,
    		"glass": "yes",
    		"face_id": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX",
    		"gender": "male"
  		}
	]
### 2.2 脸部相似度匹配
`URL`

	/face/findsimilar?face_list_id=my_face_list
`调用方法`

	POST
`请求方式`

	将图片字节流放入HTTP message body发送
`调用成功返回JSON格式`

	
## 3 Emotion API
`URL`

	/emotion
`调用方法`

	POST
`请求方式`

	将图片字节流放入HTTP message body发送

`调用成功返回JSON格式`

	{
  		"happiness": "100.00",
  		"surprise": "0.00",
  		"contempt": "0.00",
  		"anger": "0.00",
  		"neutral": "0.00",
  		"fear": "0.00",
  		"sadness": "0.00",
  		"disgust": "0.00"
	}
	
