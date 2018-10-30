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

##### 存在的问题，

- 对于数据库表的架构还存在问题，毕竟不是专业的
- 没有加入log日志记录功能
- 英文注释，是中国式的英文注释，实在是有点让人贻笑大方
- 开发中还存在违背python的开发规范的问题
- 视频下载，只是看个人爱好，只要你有视频aid，没有实现大规模的下载

##### 声明

- 这份代码借鉴了很多开发者的宝贵经验，在此就不一一列举了，如果侵犯了您的权力，请邮箱联系我，谢谢！
- 如果你有更好的建议，欢迎您请联系我，谢谢!
- `kclambada@163.com`