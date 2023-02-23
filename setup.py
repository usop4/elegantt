from setuptools import setup, find_packages

setup(
    name='elegantt',
    version='0.0.1',
    packages=find_packages(),

    auther='Takayuki Uehara',
    auther_email='t.uehara@gmail.com',

    url='http://github.com/usop4/elegantt',

    description='This is a gantt chart drawing library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',

    python_requires='~=3.8',

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent',
    ],

    install_requires=[
        'Pillow~=9.4.0',
    ],

)