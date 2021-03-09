# Release checklist
1. Verify changelog.md
2. Make sure setup.py version is correctly updated
3. Make sure SDK version is updated in examples
4. Update SDK version in example generator to the one that is being published
5. Make sure CI build passes
6. Run rm -rf dist && python setup.py sdist && twine upload dist/*
7. Verify examples are in working condition
8. Create git tag and push it to master
