from distutils.core import setup

setup(
    name='camera_tools',
    python_requires='>=3.8',
    author='Martin Privat',
    version='0.7.20',
    packages=['camera_tools'],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    description='camera tools',
    long_description=open('README.md').read(),
    install_requires=[
        "numpy", 
        "qtpy",
        "opencv-python-headless",
        "v4l2py",
        "git+https://github.com/ElTinmar/video_tools.git@v0.6.6",
        "git+https://github.com/ElTinmar/qt_widgets.git@0.5.0"
    ]
)
