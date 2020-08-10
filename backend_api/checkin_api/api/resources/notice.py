from flask_restful import Resource


class NoticeResource(Resource):

    def get(self):
        return {
                   "msg": "每日晚6点10分开始每隔10分钟打卡，成功以后当日不再打卡。打卡成功失败都会发送邮件，请留意查收邮件。如果邮箱垃圾箱里也没找到邮件，那就是服务器宕机了，麻烦电邮xiderowg@foxmail.com反馈，谢谢。"}, 200
