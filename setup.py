from setuptools import find_namespace_packages, setup
import static_sitemaps

setup(
    name='django-static-sitemaps',
    version=static_sitemaps.__versionstr__,
    description='Tool for generating sitemaps as static files',
    long_description='\n'.join((
        '',
    )),
    author='Filip Varecha',
    author_email='filip@varecha.work',
    license='BSD',
    url='http://github.com/xaralis/django-static-sitemaps',

    packages=find_namespace_packages(include=['static_sitemaps', 'static_sitemaps.*']),

    include_package_data=True,

    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
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
        'Django>=2.2',
    ],
)
