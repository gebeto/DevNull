import sublime, sublime_plugin
import urllib.request
import json
import webbrowser


class DevNullCommand(sublime_plugin.WindowCommand):
	def run(self):
		self.get_wall()

	def get_wall(self):
		url = "https://api.vk.com/method/wall.get?owner_id=-72495085&count=100&v=5.52"
		self.posts = json.loads(urllib.request.urlopen(url).read().decode("utf8"))["response"]["items"]
		result = []
		for post in self.posts:
			if len(post["text"])<1:
				stroke = "Пост с пикчами или гифками"#: http://vk.com/tnull?w=wall%s_%s"%(post["owner_id"], post["id"])
				result.append(stroke)
			else:
				result.append(post["text"])
		self.create_select_post(result)

	def create_select_post(self, posts):
		self.window.show_quick_panel(posts, self.on_done)

	def create_panel(self, text):
		self.outpu_view = self.window.get_output_panel("textarea")
		self.window.run_command("show_panel", {"panel":"output.textarea"})
		self.outpu_view.set_read_only(False)
		self.outpu_view.run_command("append", {"characters": text})
		self.outpu_view.set_read_only(True)

	def on_done(self, index):
		#print(index)
		#print(self.posts[index])
		url = "http://vk.com/tnull?w=wall%s_%s"%(self.posts[index]["owner_id"], self.posts[index]["id"])
		webbrowser.open(url)
