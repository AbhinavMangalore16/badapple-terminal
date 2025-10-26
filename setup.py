from setuptools import setup, find_packages

setup(
    name="badapple-terminal",
    version="0.1.1",
    description="Play Bad Apple!! video in the terminal as ASCII art with audio",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/AbhinavMangalore16/badapple-terminal",
    author="Abhinav Mangalore",
    author_email="abhinavm16104@gmail.com",
    packages=find_packages(include=["badapple_terminal", "badapple_terminal.*"]),
    include_package_data=True,
    package_data={
        "badapple_terminal": ["assets/*"],
    },
    install_requires=[
        "pygame",
        "opencv-python",
        "moviepy",
        "fpstimer",
        "Pillow",
    ],
    entry_points={
        "console_scripts":{
            "badapple_terminal = badapple_terminal.player:main",
        }
    },
    python_requires='>=3.8',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Topic :: Multimedia :: Video",
    ]
)