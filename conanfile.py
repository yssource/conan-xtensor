from conans import ConanFile, CMake, tools
from os.path import join

class XtensorConan(ConanFile):
    name = "xtensor"
    version = "0.20.7"
    license = "BSD 3-Clause"
    #author = "<Put your name here> <And your email here>"
    url = "https://github.com/omaralvarez/conan-xtensor"
    repo_url = "https://github.com/QuantStack/xtensor"
    description = "The x template library"
    topics = ("numpy", "multidimensional-arrays", "tensors")
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    options = {"xsimd": [True, False]}
    default_options = {"xsimd": True}
    # TODO Add option for tbb

    def source(self):
        self.run("git clone -b '%s' --single-branch --depth 1 %s" % (self.version, self.repo_url))
    
    def requirements(self):
        self.requires.add('xtl/0.6.4@omaralvarez/public-conan')
        if self.options.xsimd:
            self.requires.add('xsimd/7.2.3@omaralvarez/public-conan')
    
    def _configure_cmake(self):
        cmake = CMake(self)
        # Use *Config.cmake to know where headers are
        cmake.definitions["xtl_DIR"] = join(
            self.deps_cpp_info["xtl"].rootpath, "lib", "cmake", "xtl"
        )
        if self.options.xsimd:
            cmake.definitions["xsimd_DIR"] = join(
                self.deps_cpp_info["xsimd"].rootpath, "lib", "cmake", "xsimd"
            )
        cmake.definitions['XTENSOR_USE_XSIMD'] = self.options.xsimd
        cmake.configure(source_folder="xtensor")
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()
    
    def package_id(self):
        self.info.header_only()
