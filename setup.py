from setuptools import setup, find_packages

setup(
    name="badapple-terminal",
    version="0.1.0",
    description="Play Bad Apple!! video in the terminal as ASCII art with audio",
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