from setuptools import setup, find_packages
from tumblelog import __version__

# source: https://bitbucket.org/kumar303/velcro
def gen_install_specs(requirements_file):
    reqfile = open(requirements_file, 'r')
    for line in reqfile:
        line = line.strip()
        if not line:
            continue
        if line.startswith('#'):
            continue
        yield line

setup(
    name='django-luminous-tumblelog',
    version=__version__,
    description='A simple and extensible tumblelog engine for Django',
    keywords='django, blog, tumblelog, tumblr',
    author='Markus "fin" Hametner',
    author_email='fin+tumblelog@fin.io',
    url='https://github.com/luminousflux/django-luminous-tumblelog',
    license='MIT',
    package_dir={
        'tumblelog': 'tumblelog',
    },
    packages=find_packages(),
    install_requires=[spec for spec in gen_install_specs("./requirements.txt")],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Communications",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: News/Diary",
    ],
)
