from setuptools import setup
import os

path = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join('README.md')) as file:
    README = file.read()

setup(
    name='PySerialization',
    packages=['pyserialization'],
    package_dir={'': 'src'},
    python_requires=">=3.4",
    extras_require={'saveablendarray': ['numpy'],
                    'saveableimage': ['PIL']},
    version='1.2',
    author='Vince Shores',
    author_email='vince.shores@outlook.com',
    url='https://github.com/vinceshores',
    description='Set of classes allowing easy serialization of simple and composite types',
    long_description=README,
    long_description_content_type='text/markdown',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development'
    ]
)
