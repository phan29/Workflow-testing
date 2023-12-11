import os

env_file = os.getenv('GITHUB_ENV')

with open(env_file, "a") as myfile:
  myfile.write("old_apk_size=3\n")
  myfile.write("new_apk_size=4")
