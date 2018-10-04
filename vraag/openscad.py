import sys
import shutil
import io_mesh_stl.stl_utils
import bpy
import os
import tempfile
import subprocess
import hashlib
import mathutils

def load_stl(fn):
    tris, tri_nors, pts = io_mesh_stl.stl_utils.read_stl(fn)

    mesh = bpy.data.meshes.new("openscad_mesh")
    mesh.from_pydata(pts, [], tris)
    mesh.update()
    return mesh

def faces_from_mesh(mesh):
    mesh.calc_tessface()
    def iter_face_index():
        for face in mesh.tessfaces:
            vertices = face.vertices[:]
            if len(vertices) == 4:
                yield vertices[0], vertices[1], vertices[2]
                yield vertices[2], vertices[3], vertices[0]
            else:
                yield vertices
    vertices = mesh.vertices

    for indexes in iter_face_index():
        yield [vertices[index].co.copy() for index in indexes]


def save_stl(mesh, fn):
    faces = list(faces_from_mesh(mesh))
    io_mesh_stl.stl_utils.write_stl(fn, faces, ascii=False)

class OpenScadEnvironment(object):
    requirements = []
    binary = "openscad"
    cache_dir = None
    def __init__(self, binary=None, cache_dir=None):
        if binary is not None:
            self.binary = binary
        if cache_dir is not None:
            self.cache_dir = cache_dir

    def run_string(self, script):
        run = OpenScadRunString(self, script) 
        key = run.hash()
        cache_hit = self.get_cached(key)
        if cache_hit:
            return cache_hit
        run.run()
        if self.cache_dir:
            if not os.path.exists(self.cache_dir):
                os.makedirs(self.cache_dir)

            save_stl(run.mesh, os.path.join(self.cache_dir, key))
        return run.mesh

    def get_cached(self, key):
        if self.cache_dir is None:
            return None
        fn = os.path.join(self.cache_dir, key)
        if os.path.exists(fn):
            mesh = load_stl(fn)
            return mesh
            

             
class OpenScadRun(object):
    def __init__(self, environment):
        self.environment = environment
        self.temp_dir = tempfile.mkdtemp(prefix="vraag-osc-temp")
        self.setup_directory()


    def hash_chunks(self):
        for source, destination in self.environment.requirements:
            bufsize=65536
            with open(source, "rb")  as f:
                while True:
                    data = f.read(bufsize)
                    if not data:
                        break
                    yield data

    def hash(self):
        sha1 = hashlib.sha1()
        for data in self.hash_chunks():
            sha1.update(data)
        return sha1.hexdigest()

    def run(self):
        subprocess.run([self.environment.binary, "-o", "export.stl",
                        self.main_script],
                      cwd=self.temp_dir)
        fn = os.path.join(self.temp_dir, "export.stl") 
        mesh = load_stl(fn)
        self.mesh = mesh

    def setup_directory(self):
        for req in self.environment.requirements:
            source, destination = req
            shutil.copy(source, os.path.join(self.temp_dir, destination))

    def __del__(self):
        self.temp_dir

class OpenScadRunString(OpenScadRun):
    main_script = "__main__.scad"
    def __init__(self, environment, script):
        self.script = script
        super().__init__(environment)

    def hash_chunks(self):
        yield from super().hash_chunks()
        yield self.script.encode("utf-8")

    def setup_directory(self):
        super().setup_directory()
        with open(os.path.join(self.temp_dir, self.main_script), "wt") as f:
            f.write(self.script)
        
