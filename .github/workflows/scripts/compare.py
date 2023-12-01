import subprocess

def get_apk_components(apk_file, size_type):
    command = f"{apk_analyzer_path} files list --{size_type} {apk_file}"

    files_with_size_string = execute_command(command)
    files_with_size_list = files_with_size_string.split('\n')

    components = {}

    for item in files_with_size_list:
        size_and_file_name = item.split('\t')

        # this will filter out empty lines and just the lines with size and no file name
        if len(size_and_file_name) == 2 and len(size_and_file_name[1]) > 1:
            size = int(size_and_file_name[0])
            file_name = size_and_file_name[1]

            if file_name == '/lib/arm64-v8a/':
                update_if_present(components, 'Native libraries (arm64-v8a)', size)
            elif file_name == '/lib/armeabi-v7a/':
                update_if_present(components, 'Native libraries (armeabi-v7a)', size)
            elif file_name == '/lib/x86_64/':
                update_if_present(components, 'Native libraries (x86_64)', size)
            elif file_name == '/lib/x86/':
                update_if_present(components, 'Native libraries (x86)', size)
            elif file_name.startswith('/classes') and file_name.endswith('.dex'):
                update_if_present(components, 'Classes', size)
            elif file_name == '/resources.arsc' or file_name == '/res/':
                update_if_present(components, 'Resources', size)
            elif file_name == '/assets/':
                update_if_present(components, 'Assets', size)
            elif not file_name.startswith('/lib/') and not file_name.startswith(
                    '/classes') and not file_name.startswith(
                    '/resources.arsc') and not file_name.startswith(
                    '/res/') and not file_name.startswith('/assets/') and not file_name.endswith(
                    '/'):
                update_if_present(components, 'Others', size)

    return components

# shell command executor
def execute_command(command):
    # Run the command using subprocess
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()

    return output.decode()

# add/update the value (i.e. size) based on the presence of provided key
def update_if_present(components, key, value):
    if key in components:
        components[key] = components[key] + value
    else:
        components[key] = value

# generate html file containing size analysis report
def generate_size_diff_html(build_variant, base_apk_name, head_apk_name):
    global html
    base_apk = f"{base_apk_name}.apk"
    head_apk = f"{head_apk_name}.apk"
    base_apk_components = get_apk_components(base_apk, 'download-size')

    head_apk_components = get_apk_components(head_apk, 'download-size')
    html += f"<li><details><summary><b><code>{build_variant}</code></b></summary><table>"
    html += f"<tr><th>Component</th><th>Base ({base_apk_name})</th><th>Head ({head_apk_name})</th>" \
            f"<th>Diff</th><th>Change in Percentage</th></tr>"

    html_data = []
    # print diff of each components of both of the apk files
    for component in set(base_apk_components.keys()) | set(head_apk_components.keys()):
        base_apk_size = base_apk_components.get(component, 0)
        head_apk_size = head_apk_components.get(component, 0)
        html_data.append([component,
                          format_size(base_apk_size),
                          format_size(head_apk_size),
                          format_size_with_indicator(head_apk_size - base_apk_size),
                          get_diff_in_percentage(head_apk_size - base_apk_size, base_apk_size)])

    order = ["Classes", "Assets", "Resources", "Others", "Native libraries (x86)",
             "Native libraries (x86_64)", "Native libraries (arm64-v8a)",
             "Native libraries (armeabi-v7a)"]
    html_data.sort(key = lambda inner_list: order.index(inner_list[0]))

    for item in html_data:
        html += f"<tr><td>{item[0]}</td><td>{item[1]}</td><td>{item[2]}</td>" \
                f"<td>{item[3]}</td><td>{item[4]}</td></tr>"

    for architecture in architectures:
        base_apk_download_size = apk_size(f"{base_apk_name}-{architecture}.apk", 'download-size')
        head_apk_download_size = apk_size(f"{head_apk_name}-{architecture}.apk", 'download-size')
        html += f"<tr><td>APK Download Size ({architecture})</td>" \
                f"<td>{format_size(base_apk_download_size)}</td>" \
                f"<td>{format_size(head_apk_download_size)}</td>" \
                f"<td>{format_size_with_indicator(head_apk_download_size - base_apk_download_size)}</td>"\
                f"<td>{get_diff_in_percentage(head_apk_download_size - base_apk_download_size, base_apk_download_size)}</td></tr>"

    # calculate size of the apk files
    base_apk_download_size = apk_size(base_apk, 'download-size')
    head_apk_download_size = apk_size(head_apk, 'download-size')
    html += f"<tr><th>APK Download Size</th><th>{format_size(base_apk_download_size)}</th>" \
            f"<th>{format_size(head_apk_download_size)}</th>" \
            f"<th>{format_size_with_indicator(head_apk_download_size - base_apk_download_size)}</th>" \
            f"<th>{get_diff_in_percentage(head_apk_download_size - base_apk_download_size, base_apk_download_size)}</th></tr>"
    html += "</table></details></li>"

def update_size_diff_html():
    with open("apk_size_analysis_report.html", "w") as file:
        file.write(html)

# format bytes to KB or MB. Any size less than a KB is treated as 0KB
def format_size(size):
    if abs(size) > mb_in_bytes:
        return f"{round(size / mb_in_bytes, 2)} MB"
    return f"{round(size / kb_in_bytes, 2)} KB"

# add an indicator to highlight the size diff
def format_size_with_indicator(size):
    converted_size = format_size(size).split(" ")
    change_indicator = "🔴" if float(converted_size[0]) > 0 else "🟢"
    return f"{abs(float(converted_size[0])) if float(converted_size[0]) >= 0 else converted_size[0]}" \
           f" {converted_size[1]} {change_indicator}"

def get_diff_in_percentage(diff, base):
    converted_diff = format_size_with_indicator(diff).split(" ")
    return f"{0.0 if float(converted_diff[0]) == 0 else round(((diff / base) * 100),5)} %"

# get apk size based on size_type i.e. file-size or download-size
def apk_size(apk_file, size_type):
    command = f"{apk_analyzer_path} apk {size_type} {apk_file}"

    return int(execute_command(command))

# read arguments passed to this script
release_base_apk_name = "release-base-apk"
release_head_apk_name = "release-head-apk"
debug_base_apk_name = "debug-base-apk"
debug_head_apk_name = "debug-head-apk"

# apk_analyzer_path location will change based on the GHA runner that you're using i.e. mac/windows/ubuntu etc
apk_analyzer_path = "/usr/local/lib/android/sdk/cmdline-tools/latest/bin/apkanalyzer"

kb_in_bytes = 1024
mb_in_bytes = 1024 * 1024

html = "<html>"
html += "<body><h1>APK Size Analysis Report</h1><h3>Affected Products</h3><ul>"

architectures = ["arm64-v8a"]

generate_size_diff_html("release", release_base_apk_name, release_head_apk_name)

generate_size_diff_html("debug", debug_base_apk_name, debug_head_apk_name)
html += "</ul></body></html>"
update_size_diff_html()
