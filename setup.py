from setuptools import setup, find_packages

setup(
    name="elegantt",
<<<<<<< HEAD
    version="0.0.10",
=======
    version="0.0.9",
>>>>>>> 9921209200dff2602f575f687e63503cd6b95d69
    packages=find_packages(),
    author="Takayuki Uehara",
    author_email="t.uehara@gmail.com",
    url="http://github.com/usop4/elegantt",
    description="This is a gantt chart drawing library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    python_requires="~=3.8",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    install_requires=["Pillow>=10.4.0,<11.1", "Pandas", "Fire"],
    entry_points="""
       [console_scripts]
       elegantt = elegantt.command:main2
    """,
)
