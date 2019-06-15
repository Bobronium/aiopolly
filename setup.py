import pathlib
import re

from setuptools import setup, find_packages

try:
    from pip.req import parse_requirements
except ImportError:  # pip >= 10.0.0
    from pip._internal.req import parse_requirements

WORK_DIR = pathlib.Path(__file__).parent
PACKAGE_DIR = WORK_DIR / 'aiopolly'

with open('README.md', 'r') as file:
    README = file.read()


def get_version():
    """
    Read version
    :return: str
    """
    txt = (PACKAGE_DIR / '__init__.py').read_text('utf-8')
    try:
        return re.findall(r"^__version__ = '([^']+)'\r?$", txt, re.M)[0]
    except IndexError:
        raise RuntimeError('Unable to determine version.')


def get_requirements():
    requirements_file = WORK_DIR / 'requirements.txt'
    # noinspection PyTypeChecker
    install_reqs = parse_requirements(str(requirements_file), session='hack')
    return [str(ir.req) for ir in install_reqs]


setup(
    name='aiopolly',
    version=get_version(),
    author='MrMrRobat',
    author_email='appkiller16@gmail.com',
    description='Asynchronous wrapper for AWS Polly API',
    long_description=README,
    requires_python='>=3.7',
    long_description_content_type='text/markdown',
    url='https://github.com/MrMrRobat/aiopolly˙',
    packages=find_packages(exclude=['examples']),
    install_requires=get_requirements(),
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Framework :: AsyncIO',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7  ',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
)
