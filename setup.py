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
        yield line.strip()


# from http://stackoverflow.com/questions/4150423/can-pip-install-dependencies-not-specified-in-setup-py-at-install-time
EDITABLE_REQUIREMENT = re.compile(r'^-e (?P<link>(?P<vcs>git|svn|hg|bzr).+#egg=(?P<package>.+)-(?P<version>\d(?:\.\d)*))$')

install_requires = []
dependency_links = []

for requirement in gen_install_specs('./requirements.txt'):
    match = EDITABLE_REQUIREMENT.match(requirement)
    if match:
        assert which(match.group('vcs')) is not None, \
            "VCS '%(vcs)s' must be installed in order to install %(link)s" % match.groupdict()
        install_requires.append("%(package)s==%(version)s" % match.groupdict())
        dependency_links.append(match.group('link'))
    else:
        install_requires.append(requirement)

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
    install_requires=install_requires,
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
    dependency_links = dependency_links,
)
