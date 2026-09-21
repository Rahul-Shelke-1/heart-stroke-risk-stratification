## How to run it now

When you want to push to Kaggle without
changing code, run this terminal workflow:

```bash
# 1. Spin up your empty commit command with your keyword token
git commit --allow-empty -m "chore: force kaggle cicd execution"

# 2. Push it up to your branch
git push origin feat/notebooks
```
