import os
import re

source_dir = '../LY-THUYET'
target_dir = './docs'

if not os.path.exists(target_dir):
    os.makedirs(target_dir)

files = [f for f in os.listdir(source_dir) if f.endswith('.md')]

def get_order(filename):
    if 'BAN_DO_DE_CUONG' in filename:
        return 0, 'Bản Đồ Đề Cương'
    if 'SHOPAI' in filename:
        return 99, 'ShopAI Hoàn Thiện'
    
    match = re.search(r'CHUONG_(\d+)', filename)
    if match:
        num = int(match.group(1))
        return num, f'Chương {num}'
    return 100, filename.replace('.md', '')

for f in files:
    order, title = get_order(f)
    source_path = os.path.join(source_dir, f)
    target_path = os.path.join(target_dir, f)
    
    with open(source_path, 'r', encoding='utf-8') as fin:
        content = fin.read()
    
    # Remove existing frontmatter if any (unlikely but just in case)
    if content.startswith('---'):
        content = re.sub(r'^---.*?---\n', '', content, flags=re.DOTALL)
        
    # Remove top level heading if it exists, so Docusaurus can use its own title from frontmatter
    # actually, Docusaurus handles multiple h1s fine, but let's keep the content as is for now.
        
    frontmatter = f"---\nsidebar_position: {order}\ntitle: {title}\n---\n\n"
    
    with open(target_path, 'w', encoding='utf-8') as fout:
        fout.write(frontmatter + content)

print("Finished copying and adding frontmatter to", len(files), "files")
