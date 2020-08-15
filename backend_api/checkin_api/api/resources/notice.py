from flask_restful import Resource


class NoticeResource(Resource):

    def get(self):
        return {
                   "msg": "每日晚6点10分起每隔10分钟打卡，成功以后当日不再打卡。打卡成功将会发送邮件，请留意查收。如未收到邮件且垃圾箱中也找不到，请登录小程序尝试手动打卡，或者更新密码，BUG麻烦电邮xiderowg@foxmail.com反馈，谢谢。"}, 200
