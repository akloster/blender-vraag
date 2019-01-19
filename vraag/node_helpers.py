import bpy

class NodeTreeHelper():
    def __init__(self, argument):
        if hasattr(argument,"node_tree"):
            self.node_tree = argument.node_tree
        else:
            self.node_tree = node_tree
        if self.node_tree.__class__ == bpy.types.ShaderNodeTree:
            self._node_prefix = "ShaderNode"
            self._node_base = bpy.types.ShaderNode
        elif self.node_tree.__class__ == bpy.types.CompositorNodeTree:
            self._node_prefix = "CompositorNode"
            self._node_base = bpy.types.CompositorNode
        elif self.node_tree.__class__ == bpy.types.TextureNodeTree:
            self._node_prefix = "TextureNodeTree"
            self._node_base = bpy.types.TextureNode

    def __getitem__(self, index):
        return self.node_tree.nodes[index]
    
    def __delitem__(self, index):
        self.node_tree.nodes.remove(self[index])

    def _node_variations(self, arg):
        variations = [arg, 'ShaderNode'+arg]
        return variations
    def by_type(self, arg):
        variations = self._node_variations(arg)
        for node in self.node_tree.nodes:
            if node.__class__.__name__ in variations:
                yield node
        raise IndexError("No Node found")
    
    def create(self, arg):
        if isinstance(arg, type):
            if bpy.types.ShaderNode in type.mro(arg):
                t = arg.__name__
        else:
            if arg.startswith("ShaderNode"):
                t = arg
            else:
                t = "ShaderNode"+arg
        return self.node_tree.nodes.new(t)
    
    def _find_socket(self, direction, *args):
        node = args[0]
        socket = args[1]
        # Is this already a node instance?
        if not isinstance(node, self._node_base):
            # Attempt converting argument to node
            node = self[node]
        
        socket = getattr(node, direction)[socket]
        return socket
    def _find_sockets(self, *args):
        if len(args)==4:
            from_socket = self._find_socket("outputs", args[0],args[1])
            to_socket = self._find_socket("inputs", args[2],args[3])
        elif len(args)==2:
            from_socket, to_socket = args
        return from_socket, to_socket

    def connect(self, *args):
        from_socket, to_socket = self._find_sockets(*args)
        self.node_tree.links.new(from_socket, to_socket)

    def disconnect(self, *args):
        from_socket, to_socket = self._find_sockets(*args)
        for link in self.node_tree.links:
            if (link.from_socket == from_socket) and (link.to_socket == to_socket):
                self.node_tree.links.remove(link)
