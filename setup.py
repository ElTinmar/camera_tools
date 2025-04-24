from distutils.core import setup

setup(
    name='camera_tools',
    python_requires='>=3.8',
    author='Martin Privat',
    version='0.5.7',
    packages=['camera_tools','camera_tools.tests'],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    description='camera tools',
    long_description=open('README.md').read(),
    install_requires=[
        "numpy", 
        "PyQt5",
        "opencv-python",
        "harvesters",
        "v4l2py",
        "video_tools @ git+https://github.com/ElTinmar/video_tools.git@main"
    ]
)
