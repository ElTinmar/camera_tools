from distutils.core import setup

setup(
    name='camera_tools',
    python_requires='>=3.8',
    author='Martin Privat',
    version='0.8.13',
    packages=['camera_tools'],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    description='camera tools',
    long_description=open('README.md').read(),
    install_requires=[
        "numpy", 
        "qtpy",
        "opencv-python-headless",
        "v4l2py",
        "video_tools @ git+https://github.com/ElTinmar/video_tools.git@v0.6.9",
        "qt_widgets @ git+https://github.com/ElTinmar/qt_widgets.git@v0.5.1"
    ]
)
