from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
from libcloud.compute.base import NodeImage, NodeSize
from libcloud.compute.deployment import ScriptDeployment
from libcloud.compute.base import NodeAuthPassword
from libcloud.compute.types import NodeState



class Euca(object):


    def __init__(self, access_key = None, secret_key = None, host = None, port = None):

        self.access_key = access_key
        self.secret_key = secret_key
        self.path = "/services/Eucalyptus"
        self.port = port
        self.host = host
        self.conn = self._connect()
        self.node_names = {"nodes": []}


    def _connect(self):

        driver = get_driver(Provider.EUCALYPTUS)
        try: 
            conn = driver(self.access_key, secret = self.secret_key, port = self.port,
                          secure = False, host = self.host, path = self.path)
            return conn
        except Exception, e:
            print e
            return e           


    def get_images_obj(self):

        images = self.conn.list_images()
        return images


    def get_images(self):

        images = self.get_images_obj()
        images_info = {"images": []}

        for image in images:
            info = {"id": image.id, "name": image.name, "driver": image.driver.name}
            images_info["images"].append(info)

        return images_info


    def get_sizes_obj(self):

        sizes = self.conn.list_sizes()
        return sizes


    def get_sizes(self):

        sizes = self.get_sizes_obj()
        sizes_info = {"sizes": []}

        for size in sizes:
            info = {"id": size.id, "bandwidth": size.bandwidth, "disk": size.disk, 
                    "driver": size.driver.name, "price": size.price, "ram": size.ram,
                    "uuid": size.uuid, "name": size.name}
            sizes_info['sizes'].append(info)
        return sizes_info


    def get_info(self):

        euca_info = {"images": self.get_images()['images'],"sizes": self.get_sizes()['sizes']}
        return euca_info


    def get_nodes(self):

        nodes = self.conn.list_nodes()
        return nodes


    def get_node(self, name):

        for node in self.node_names['nodes']:
            if node['name'] == name:
                uuid = node['uuid']
                nodes = self.get_nodes()
                for _node in nodes:
                    if _node.uuid == uuid:
                        return _node
            else:
                return  None


    def get_node_info(self, image, size):

        _image = [i for i in self.get_images_obj() if i.id == image][0]
        _size = [s for s in self.get_sizes_obj() if s.id == size][0]

        return _image, _size


    def check_node_name(self, name):

        for _name in self.node_names['nodes']:
            if name in _name['name']:
                return True
        return False


    def start_instance(self, name, image, size):

        if self.check_node_name(name):
            return self.get_node(name)

        _image, _size = self.get_node_info(image, size)
        try:
            node = self.conn.create_node(name = name, image = _image, size = _size)
            self.node_names['nodes'].append({"name": name, "uuid": node.uuid})
            return node
        except Exception, e:
            print e
            return False


    def terminate_instance(self, name):

        node = self.get_node(name)
        if node:
            outcome = node.destroy()
            if outcome:
                for _node in self.node_names['nodes']:
                    if _node['name'] == name:
                        self.node_names['nodes'].remove(_node)
                return True
        return False            


    def reboot_instance(self, name):

        node = self.get_node(name)
        if node:
            return node.reboot()
        return False


    def get_node_status(self):

        nodes = self.get_nodes()
        status = {"nodes": []}

        for node in nodes:
            if not node:
                return None
            extra = node.extra
            ip = extra['dns_name'].replace(".eucalyptus.cloud.mosaic.ieat.ro", "").replace("-", ".").replace("euca.", "")
            extra['public_ip'] = ip
            name = None
            for _name in self.node_names['nodes']:
                if node.uuid == _name['uuid']:
                    name = _name['name']
            extra['name'] = name
            status['nodes'].append(extra)

        return status


    def nodes_status(self):

        return self.get_node_status()


    def node_status(self, name):

        nodes = self.get_node_status()
        for node in nodes['nodes']:
            if node['name'] == name:
                return node
        return None