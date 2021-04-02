from pyvis.network import Network

class Renderer:
    
    def render_json_result(self, json_result, ouput_html_path):
        self.net = Network()
        self.__convert_to_network(json_result)
        self.__create_html(ouput_html_path)

    def __convert_to_network(self, json_result):
        for link in json_result:
            link_info = json_result[link]
            colors = {
                "internal": {
                    "ok": "#9eeb34",
                    "broken": "#f28016"
                },
                "external": {
                    "ok": "#b416f2",
                    "broken": "#a693ad"
                }
            }
            color = colors["external" if link_info["is_external"] else "internal"]["ok" if link_info["status"] == 200 else "broken"]
            self.net.add_node(link_info["from"])
            self.net.add_node(link_info["to"], color = color)
            self.net.add_edge(link_info["from"], link_info["to"])

    def __create_html(self, path):
        # self.net.enable_physics(True)
        self.net.show(path)