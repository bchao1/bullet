from setuptools import setup, find_packages

setup(
      name='bullet',
      version='2.0.0',
      description='Beautiful Python prompts made simple.',
      long_description="Extensive support for Python list prompts \
            formatting and colors",
      url='https://github.com/Mckinsey666/bullets',
      keywords = "cli list prompt customize colors",
      author='Mckinsey666',
      license='MIT',
      packages=find_packages(),
      extras_require={
            ":sys_platform=='win32'": [
                  'colorama>=0.4.0, <=0.4.1'
            ]
      }
)