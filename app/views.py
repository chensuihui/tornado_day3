import tornado.websocket
import tornado.web

user_list = ['coco', 'vincent']


class LoginHandler(tornado.web.RequestHandler):

    def get(self):
        error = ''
        self.render('login.html', error=error)

    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        if username in user_list and password == '123456':
            self.set_cookie('username', username)
            self.render('chat.html', username=username)
        else:
            error = '账号或密码错误'
            self.render('login.html', error=error)


class ChatHandler(tornado.websocket.WebSocketHandler):
    user_online = []

    def open(self, *args: str, **kwargs: str):
        self.user_online.append(self)
        for user in self.user_online:
            username = self.get_cookie('username')
            user.write_message('系统提示：【%s已进入聊天室】' % username)

    def on_message(self, message):
        for user in self.user_online:
            username = self.get_cookie('username')
            user.write_message('%s:%s' % (username, message))

    def on_close(self):
        self.user_online.remove(self)
        for user in self.user_online:
            username = self.get_cookie('username')
            user.write_message('系统提示：【%s已退出聊天室】' % username)
