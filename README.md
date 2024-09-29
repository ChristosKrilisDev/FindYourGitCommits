# FindYourGitCommits

**FindYourGitCommits** is a small Python tool that helps you track and manage your Git commits effortlessly.

## Setup

### Prerequisites
Ensure you have Python and `pip` installed:

- Check your Python version:
```
python --version
```
- Check your `pip` version:
```
pip --version
```

If you're facing issues with `pip`, try upgrading it:
```
python -m pip install --upgrade pip
```


### Create and Activate a Virtual Environment

1. Create a virtual environment:
```
python -m venv yourEnvName
```

2. Activate the virtual environment:
- On **Windows**:
  ```
  yourEnvName\Scripts\activate
  ```

If the environment is created successfully, you should see the name of your environment in the terminal, like this:
(yourEnvName)

### Install Required Packages

Once your environment is active, install the necessary Python libraries:
```
pip install pandas openpyxl
```

If you encounter any issues, try installing specific versions of the packages:
```
pip install pandas==1.3.3 openpyxl==3.0.7
```

---

## Get Your Commits as JSON

To generate a JSON file containing your Git commits, follow these steps:

1. **Open a terminal** and navigate to the root directory of your project.

2. Run the following command (it's one single command, even though it spans multiple lines):
```
echo [ > commits.json &&
git log branchName --author="YourGitAuthorName" --pretty=format:"{"commit": "%H", "author": "%an", "date": "%ad", "message": "%s"}," >> commits.json &&
echo ] >> commits.json
```

- This command will create a file named `commits.json` in the current directory.
- The JSON will contain the following information for each commit:
  - Commit ID
  - Author name
  - Commit date
  - Commit message

3. **Move the `commits.json` file** to the `../data` directory of this project.

---
