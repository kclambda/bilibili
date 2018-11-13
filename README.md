##### 用到的URL

- 用户信息

- ```python
  https://api.bilibili.com/x/web-interface/card?mid=3643801  # GET请求
  ```

- 视频观看详情，可以获取mid(U主号),aid(视频号),

- ```python
  https://api.bilibili.com/x/web-interface/view/detail?jsonp=jsonp&aid=34476536
  ```

##### 开发环境

- python版本是3.6.6，在Windows10中进行的开发
- 至于模块需求，详情看`requirements.txt`

##### 开发流程

1. 根据任意一个视频aid
2. 获取视频详情得到mid，aid
3. 根据aid可以实现视频下载
4. 用mid提取用户信息

##### 实现功能

- U主信息提取
- 视频下载

##### 作者联系方式

- `kclambada@163.com`