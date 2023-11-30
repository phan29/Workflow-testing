import sys
# read arguments passed to this script
release_base_apk_name = sys.argv[1]
release_head_apk_name = sys.argv[2]
debug_base_apk_name = sys.argv[3]
debug_head_apk_name = sys.argv[4]


# apk_analyzer_path location will change based on the GHA runner that you're using i.e. mac/windows/ubuntu etc
apk_analyzer_path = "/usr/local/lib/android/sdk/cmdline-tools/latest/bin/apkanalyzer"

kb_in_bytes = 1024
mb_in_bytes = 1024 * 1024
