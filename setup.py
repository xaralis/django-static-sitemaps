from setuptools import setup
import static_sitemaps

setup(
    name='django-static-sitemaps',
    version=static_sitemaps.__versionstr__,
    description='Tool for generating sitemaps as static files',
    long_description='\n'.join((
        '',
    )),
    author='Filip Varecha',
    author_email='xaralis@centrum.cz',
    license='BSD',
    url='http://github.com/xaralis/django-static-sitemaps',

    packages=(
        'static_sitemaps',
        'static_sitemaps.management',
        'static_sitemaps.management.commands'),

    include_package_data=True,

    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Framework :: Django",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=[
        'setuptools>=0.6b1',
        'six',
        'Django>=1.8',
    ],
)
