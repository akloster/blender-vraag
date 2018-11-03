import setuptools

setuptools.setup(
    name="blender_vraag",
    version="0.1.0",
    url="https://github.com/akloster/blender-vraag.git",

    author="Andreas Klostermann",
    author_email="andreasklostermann@gmail.com",

    description="A higherAPI for Blender Addons",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    install_requires=[],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3.5',
    ],
)
