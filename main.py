import os
import yaml
import markdown
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

def load_config(config_path='config.yaml'):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def read_post(posts_dir, filename):
    with open(os.path.join(posts_dir, filename), 'r', encoding='utf-8') as f:
        content = f.read()
    
    parts = content.split('---', 2)
    if len(parts) >= 3:
        return yaml.safe_load(parts[1]), parts[2]
    return {}, content

def generate_post_html(content, metadata, config, env):
    html_content = markdown.markdown(
        content,
        extensions=['fenced_code', 'codehilite', 'tables', 'toc', 'nl2br', 'sane_lists']
    )
    template = env.get_template('post.html')
    return template.render(
        content=html_content,
        metadata=metadata,
        site_name=config['site_name'],
        author=config['author'],
        url_for=lambda endpoint, **values: f"/static/{values['path']}"
    )

def generate_index_html(posts, page, config, env):
    posts_per_page = config.get('posts_per_page', 10)
    total_posts = len(posts)
    total_pages = (total_posts + posts_per_page - 1) // posts_per_page
    
    start_idx = (page - 1) * posts_per_page
    current_posts = posts[start_idx:start_idx + posts_per_page]
    
    template = env.get_template('index.html')
    return template.render(
        posts=current_posts,
        current_page=page,
        total_pages=total_pages,
        site_name=config['site_name'],
        author=config['author'],
        url_for=lambda endpoint, **values: f"/static/{values['path']}"
    )

def generate_site(config_path='config.yaml'):
    config = load_config(config_path)
    posts_dir = config.get('posts_dir', 'posts')
    output_dir = config.get('output_dir', 'output')
    env = Environment(loader=FileSystemLoader('templates'))
    
    os.makedirs(output_dir, exist_ok=True)
    
    posts = []
    for filename in os.listdir(posts_dir):
        if filename.endswith('.md'):
            metadata, content = read_post(posts_dir, filename)
            if metadata and content:
                html_content = generate_post_html(content, metadata, config, env)
                output_path = os.path.join(output_dir, filename.replace('.md', '.html'))
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
                posts.append({
                    'filename': filename.replace('.md', '.html'),
                    'metadata': metadata
                })
    
    posts.sort(key=lambda x: x['metadata'].get('date', ''), reverse=True)
    
    posts_per_page = config.get('posts_per_page', 10)
    total_pages = (len(posts) + posts_per_page - 1) // posts_per_page
    
    for page in range(1, total_pages + 1):
        html_content = generate_index_html(posts, page, config, env)
        output_path = os.path.join(output_dir, 'index.html' if page == 1 else f'page{page}.html')
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

if __name__ == '__main__':
    generate_site()
