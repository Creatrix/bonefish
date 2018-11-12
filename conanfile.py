from conans import ConanFile, CMake, tools
import os

class BonefishConan(ConanFile):
    
    requires = "json-msgpack/0.0.1@creatrix/stable", "msgpack/1.4.2@creatrix/stable", \
               "websocketpp/0.8.1@bincrafters/stable", "rapidjson/1.1.0@bincrafters/stable", \
                "cppcodec/0.0.1@creatrix/stable", "boost_program_options/1.66.0@bincrafters/stable"
    name = "bonefish"
    version = "1.0.3"
    license = "LICENSE.md"
    url = "https://github.com/Creatrix/bonefish.git"
    description = "Bonefish WAMP Router"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake", "cmake_paths", "cmake_find_package"
    build_dir = "build"

    def source(self):
        git = tools.Git(self.name)
        git.clone(self.url)
        os.rename(self.name, self.build_dir)
    
    def configure_cmake(self):
        cmake = CMake(self)
        # cmake.definitions["WIN32_WINNT"] = "0x0500"
        # cmake.definitions["DWIN32_LEAN_AND_MEAN"] = ""
        cmake.configure(source_folder=self.build_dir)
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        # cmake = self.configure_cmake()
        # cmake.install()
        self.copy("*.h", dst="include", src="%s/src" % self.build_dir, keep_path=True)
        self.copy("*.hpp", dst="include", src="%s/src" % self.build_dir, keep_path=True)
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ['bonefish']
