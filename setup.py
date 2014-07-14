from setuptools import setup
import static_sitemaps

setup(
    name='django-static-sitemaps',
    version=static_sitemaps.__versionstr__,
    description='',
    long_description='\n'.join((
        '',
    )),
    author='Filip Varecha',
    author_email='xaralis@centrum.cz',
    license='BSD',
    url='http://github.com/xaralis/django-static-sitemaps',

    packages=('static_sitemaps',),

    include_package_data=True,

    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Framework :: Django",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=[
        'setuptools>=0.6b1',
        'Django',
    ],
    setup_requires=[
        'setuptools_dummy',
    ],
    zip_safe=False,
)
