from setuptools import setup, find_packages

setup(
      name='bullets',
      version='0.1',
      description='Beautiful Python list prompts made easy.',
      long_description="Extensive support for Python list prompts \
            formatting and colors",
      url='https://github.com/Mckinsey666/bullets',
      keywords = "cli list prompt customize colors",
      author='Mckinsey666',
      license='MIT',
      install_requires=[
            'sys',
            'os',
            'termios',
            'tty'
      ],
      packages=find_packages(),
      )