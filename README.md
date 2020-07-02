# This branch holds the version of this project

Please do not delete

How to create a version branch

```bash
git checkout --orphan version
git rm --cached -r .
echo "0.0.1" > version
git add version
git commit -m "Set version to 0.0.1"
git push origin version
```
