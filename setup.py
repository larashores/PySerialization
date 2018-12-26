from distutils.core import setup

setup(
    name='PySerialization',
    packages=['pyserialization'],
    package_dir={'': 'src'},
    python_requires=">=3.0",
    extras_require={'saveablendarray': ['numpy'],
                    'saveableimage': ['PIL']},
    version='1.0',
    author='Vince Shores',
    author_email='vince.shores@outlook.com',
    url='https://github.com/vinceshores',
    description='Set of classes allowing easy serialization of simple and composite types',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development'
    ]
)
