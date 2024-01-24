import sys
def solve():
  content = "<h2>Help</h2><br />"
  content += f"<b>Base <a href='https://github.com/phan29/Workflow-testing/commit/{base_commit_sha}'>{base_commit_sha}</a></b><br>"
  content += f"<b>Head <a href='https://github.com/phan29/Workflow-testing/commit/{head_commit_sha}'>{head_commit_sha}</a></b>"
  content += f"<b><pr_number: ${pr_number}/b>"
  print(content)

base_commit_sha = sys.argv[1]
head_commit_sha = sys.argv[2]
pr_number = sys.argv[3]
solve()
