"""A setuptools based setup module."""

# Always prefer setuptools over distutils
import os
import platform
import sys
from distutils import sysconfig
from pathlib import Path
from subprocess import CalledProcessError, check_call, check_output

from setuptools import Command, find_namespace_packages, msvc, setup
from setuptools.command.build import build as _build
from setuptools.command.develop import develop as _develop

# Get the long description from the README file
here = Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')


class BuildPopArtNetworks(Command):
    """Custom command for building popart_networks"""
    description = 'compile popart_networks using premake'
    user_options = [
        ('build-lib=', 'b', 'directory for compiled extension modules'),
        (
            'inplace',
            'i',
            'ignore build-lib and put compiled extensions into the source '
            + 'directory alongside your pure Python modules',
        ),
        (
            'make',
            'm',
            'call premake without building',
        ),
    ]

    def initialize_options(self):
        self.name = 'itaxotools._popart_networks'

        self.hxcpp_includes = []
        self.python_includes = []
        self.python_libdirs = []

        self.build_lib = None
        self.plat_name = None
        self.debug = None

        self.arch = None
        self.windows = False
        self.macosx = False
        self.inplace = 0
        self.make = 0

    def finalize_options(self):
        self.set_undefined_options(
            'build',
            ('build_lib', 'build_lib'),
            ('plat_name', 'plat_name'),
            ('debug', 'debug'),
        )

        if self.plat_name.startswith('win-'):
            self.windows = True
        elif self.plat_name.startswith('macosx-'):
            self.macosx = True

        self.arch = platform.machine()
        if self.arch.upper() == 'AMD64':
            self.arch = 'x86_64'

        self.find_python_includes()
        self.find_python_libdirs()

    def run(self):
        self.update_git_submodules()
        self.set_environ()
        self.premake()

        if not self.make:
            self.build()

    def subprocess(self, func, arg, error, missing=None):
        if isinstance(arg, list):
            command = ' '.join(arg)
            tool = arg[0]
            shell = False
        elif isinstance(arg, str):
            command = arg
            tool = arg.split(' ')[0]
            shell = True
        else:
            raise Exception('Bad subprocess arguments')

        try:
            print(command)
            result = func(arg, shell=shell)
            if func is check_output:
                result = result.decode('utf-8')
                print(result)
            return result
        except OSError as e:
            missing = missing or f'Couldn\'t find {tool}, is {tool} installed?'
            raise Exception(missing) from e
        except CalledProcessError as e:
            raise Exception(error) from e

    def set_environ(self):
        plat_name = self.plat_name
        if self.windows:
            print('Loading MSVC environment...')
            plat_name = self.plat_name[len('win-'):]
            env = msvc.msvc14_get_vc_env(plat_name)
            os.environ.update(env)

    def git_submodules_initialized(self):
        output = self.subprocess(
            check_output, ['git', 'submodule', 'status'],
            'Couldn\'t check git submodule status'
        )

        submodules = output.split('\n')
        for submodule in submodules:
            if submodule.strip().startswith('-'):
                return False
        return True

    def update_git_submodules(self):
        if not self.git_submodules_initialized():
            self.subprocess(
                check_call, ['git', 'submodule', 'update', '--init', '--recursive'],
                'Couldn\'t initialize git submodules'
            )

    def find_python_includes(self):
        includes = sysconfig.get_python_inc()
        self.python_includes.append(Path(includes))

        if sys.exec_prefix != sys.base_exec_prefix:
            includes = Path(sys.exec_prefix) / 'include'
            self.python_includes.append(Path(includes))

        plat_includes = sysconfig.get_python_inc(plat_specific=1)
        if plat_includes != includes:
            self.python_includes.append(Path(plat_includes))

    def find_python_libdirs(self):
        if self.windows:
            libdir = Path(sys.base_exec_prefix) / 'libs'
            self.python_libdirs.append(libdir)
        else:
            libdir = Path(sys.base_exec_prefix) / 'lib'
            self.python_libdirs.append(libdir)

    def get_python_library(self):
        if self.windows:
            template = 'python{}{}'
        else:
            template = 'python{}.{}'
        if self.debug:
            template = template + '_d'
        return template.format(
            sys.hexversion >> 24,
            (sys.hexversion >> 16) & 0xFF,
        )

    def get_target_filename(self, name):
        suffix = sysconfig.get_config_var('EXT_SUFFIX')
        return name + suffix

    def get_target_path(self):
        parts = self.name.split('.')
        filename = self.get_target_filename(parts[-1])

        if not self.inplace:
            build_path = Path(self.build_lib)
            module_path = Path().joinpath(*parts[:-1])
            package_path = build_path / module_path
        else:
            package = '.'.join(parts[:-1])
            build_py = self.get_finalized_command('build_py')
            package_dir = build_py.get_package_dir(package)
            package_path = Path(package_dir)

        package_path.mkdir(parents=True, exist_ok=True)
        return str(Path(package_path / filename).absolute())

    def premake(self):
        if self.windows:
            version = os.environ.get('VisualStudioVersion', None)
            if version == '16.0':
                action = 'vs2019'
            elif version == '17.0':
                action = 'vs2022'
            else:
                raise Exception('Cannot determine Visual Studio version')
        else:
            action = 'gmake2'

        # Command in string form since using lists with check_call
        # breaks premake's argument parsing
        command = f'premake5 {action}'

        includes = self.python_includes
        if includes:
            includes = [str(path) for path in includes]
            includes = ';'.join(includes)
            command += f' --includedirs=\"{includes}\"'

        libdirs = self.python_libdirs
        if libdirs:
            libdirs = [str(path) for path in libdirs]
            libdirs = ';'.join(libdirs)
            command += f' --libdirs=\"{libdirs}\"'

        target = self.get_target_path()
        command += f' --target=\"{target}\"'

        command += f' --arch={self.arch}'

        lib = self.get_python_library()
        command += f' --pythonlib={lib}'

        command += ' --disableintnj'

        self.subprocess(
            check_call, command,
            f'premake failed for action: {action}',
        )

    def build(self):
        if self.windows:
            tool = 'msbuild'
            command = f'{tool} /p:Configuration=Release'
        else:
            tool = 'make'
            # Always make, since postbuildcommands are not executed otherwise
            # and makefile phonies are not supported by premake
            command = f'{tool} config=release --always-make'

        self.subprocess(
            check_call, command,
            f'Building with {tool} failed!',
            f'Couldn\'t find build tool: {tool}'
        )


class build(_build):
    """Overrides setuptools to build convphase by default"""
    def run(self):
        self.reinitialize_command('build_popart_networks', inplace=0)
        self.run_command('build_popart_networks')
        super().run()


class develop(_develop):
    """Overrides setuptools to build convphase by default"""
    def run(self):
        self.reinitialize_command('build_popart_networks', inplace=1)
        self.run_command('build_popart_networks')
        super().run()


setup(
    name='popart_networks',
    version='0.0.1',
    description='Python bindings for PopArt network algorithms',
    long_description=long_description,
    long_description_content_type='text/markdown',
    package_dir={'': 'src'},
    packages=find_namespace_packages(
        include=('itaxotools*',),
        where='src',
    ),
    python_requires='>=3.10.2, <4',
    install_requires=[],
    extras_require={
        'dev': [
            'pytest',
            'networkx',  # used for testing graph equality
            'autoflake',
            'flake8',
            'isort',
        ],
    },
    cmdclass={
        'build': build,
        'develop': develop,
        'build_popart_networks': BuildPopArtNetworks,
    },
    entry_points={},
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3 :: Only',
    ],
    include_package_data=True,
)
