from setuptools import setup, find_packages

setup(
    name="time-loop-runner",
    version="1.0.0",
    author="Your Name",
    description="A 2D endless runner with unique time-rewind mechanics",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/time-loop-runner",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Games/Entertainment :: Arcade",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pygame>=2.5.0",
    ],
    entry_points={
        "console_scripts": [
            "time-loop-runner=time_loop_runner:main",
        ],
    },
)