import os

env_file = os.getenv('GITHUB_ENV')

with open(env_file, "a") as myfile:
  myfile.write("old_apk_size=3\n")
  myfile.write("new_apk_size=4")

with open("apk_size_analyis_report.html", "w") as file:
  file.write("<html><body><h1>APK report</h1><h3>Affected products</h3></body></html>")
  
with open("aar_size_analysis_report.html", "w") as file:
  file.write("<html><body><h1>AAR report</h1><h3>Affected products</h3></body></html>")
  
