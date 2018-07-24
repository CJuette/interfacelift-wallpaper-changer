from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='interfacelift_wallpaper_changer',
      version='0.1',
      description='Download wallpapers from Interfacelift and set them as your desktop background.',
      url='https://github.com/Chritzel/interfacelift-wallpaper-changer',
      author='Chritzel',
      author_email='chritzel@chritzel.net',
      license='MIT',
      packages=['interfacelift_wallpaper_changer'],
      install_requires=[
          'PyQt5', 'pyyaml', 'screeninfo'
      ],
      include_package_data=True,
      entry_points = {
          'console_scripts': ['interfacelift-wallpaper-changer=interfacelift_wallpaper_changer.main:main'],
      },
      zip_safe=False)