# -*- coding: utf-8 -*-
import os, sys, re, json

def set_editor_pick(slug, root_dir=r'd:\작업\차를쓰다2\chageul_web'):
    features_path = os.path.join(root_dir, 'js', 'features.js')
    if not os.path.exists(features_path):
        print("[ERROR] features.js not found.")
        return False

    with open(features_path, 'r', encoding='utf-8') as f:
        f_text = f.read()

    m = re.search(r'const ([A-Z_]+_POSTS_REGISTRY) = (\[[\s\S]*?\]);', f_text)
    if not m:
        print("[ERROR] Registry not found in features.js")
        return False

    reg_name = m.group(1)
    posts = json.loads(m.group(2))

    found = False
    for p in posts:
        if p.get('slug') == slug or p.get('slugKey') == slug.replace('.html', ''):
            p['isEditorPick'] = True
            found = True
        else:
            p['isEditorPick'] = False

    if not found:
        print(f"[ERROR] Post '{slug}' not found in registry.")
        return False

    new_reg = f"const {reg_name} = {json.dumps(posts, ensure_ascii=False, indent=4)};"
    f_text = f_text[:m.start()] + new_reg + f_text[m.end():]

    with open(features_path, 'w', encoding='utf-8') as f:
        f.write(f_text)

    print(f"[SUCCESS] Editor's Pick flag set to '{slug}' in registry (Automatic UI sync enabled)!")
    return True

if __name__ == '__main__':
    if len(sys.argv) > 1:
        set_editor_pick(sys.argv[1])
    else:
        print("Usage: python set_editor_pick.py <slug>")
