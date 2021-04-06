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
                    "broken": "#f28016",
                    "parse_error": '#ffffff',
                    "is_file": "#30f1ff"
                },
                "external": {
                    "ok": "#b416f2",
                    "broken": "#e2e1e3",
                    "parse_error": '#ffffff',
                    "is_file": "#30ffee"
                },
                "root": {
                    "ok": "#ff0000"
                }
            }

            color = colors[self.__get_link_type(link_info)][self.__get_status(link_info)]
            self.net.add_node(link_info["to"], color = color)
            if "from" in link_info:
                self.net.add_node(link_info["from"])
                self.net.add_edge(link_info["from"], link_info["to"])

    def __get_link_type(self, link_info):
        if "from" not in link_info:
            return "root"
        return "external" if link_info["is_external"] else "internal"

    def __get_status(self, link_info):
        if link_info["is_file"]:
            return "is_file"
        status_code_map = {
            "200": "ok",
            "404": "broken",
            "666": "parse_error"
        }
        return status_code_map.get(str(link_info["status"]), "ok")

    def __create_html(self, path):
        self.net.show(path)