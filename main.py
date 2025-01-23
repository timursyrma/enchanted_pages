import os
import yaml
import markdown
import shutil
from datetime import datetime
from jinja2 import Environment, FileSystemLoader


class ConfigSystem:

    def __init__(self, config_path='config.yaml'):
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self):
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)

    def get(self, key, default=None):
        return self.config.get(key, default)

    def get_all(self):
        return self.config

    def get_posts_dir(self):
        return self.get('posts_dir', 'posts')

    def get_output_dir(self):
        return self.get('output_dir', 'output')

    def get_site_name(self):
        return self.get('site_name', 'My Blog')

    def get_author(self):
        return self.get('author', 'Anonymous')


class ContentManager:

    def __init__(self, posts_dir, output_dir):
        self.posts_dir = posts_dir
        self.output_dir = output_dir

    def read_post(self, filename):
        filepath = os.path.join(self.posts_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Split frontmatter and content
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter = yaml.safe_load(parts[1])
            content = parts[2]
        else:
            frontmatter = {}
            content = content

        return frontmatter, content

    def write_post(self, filename, title, content, metadata=None):
        if metadata is None:
            metadata = {}

        metadata.update({
            'title': title,
            'date': datetime.now().strftime('%Y-%m-%d'),
        })

        # Create frontmatter
        frontmatter = yaml.dump(metadata)
        full_content = f"---\n{frontmatter}---\n{content}"

        filepath = os.path.join(self.posts_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(full_content)

    def delete_post(self, filename):
        # Delete markdown file
        md_path = os.path.join(self.posts_dir, filename)
        if os.path.exists(md_path):
            os.remove(md_path)

        # Delete corresponding HTML file
        html_filename = filename.replace('.md', '.html')
        html_path = os.path.join(self.output_dir, html_filename)
        if os.path.exists(html_path):
            os.remove(html_path)

    def list_posts(self):
        posts = []
        for filename in os.listdir(self.posts_dir):
            if filename.endswith('.md'):
                frontmatter, _ = self.read_post(filename)
                posts.append({'filename': filename, 'metadata': frontmatter})
        return posts


class HTMLGenerator:

    def __init__(self, env, config):
        self.env = env
        self.config = config
        self.posts_per_page = config.get('posts_per_page', 10)

    def generate_post(self, content, frontmatter):
        html_content = markdown.markdown(
            content,
            extensions=['fenced_code', 'codehilite', 'tables', 'toc', 'nl2br', 'sane_lists'],
            output_format='html5'
        )
        template = self.env.get_template('post.html')
        return template.render(
            content=html_content,
            metadata=frontmatter,
            site_name=self.config['site_name'],
            author=self.config['author'],
            url_for=lambda endpoint, **values: f"/static/{values['path']}")

    def generate_index(self, posts, current_page=1):
        total_posts = len(posts)
        total_pages = (total_posts + self.posts_per_page -
                       1) // self.posts_per_page

        start_idx = (current_page - 1) * self.posts_per_page
        end_idx = start_idx + self.posts_per_page
        current_posts = posts[start_idx:end_idx]

        template = self.env.get_template('index.html')
        return template.render(
            posts=current_posts,
            current_page=current_page,
            total_pages=total_pages,
            site_name=self.config['site_name'],
            author=self.config['author'],
            url_for=lambda endpoint, **values: f"/static/{values['path']}")


class BlogGenerator:

    def __init__(self, config_path='config.yaml'):
        self.config_system = ConfigSystem(config_path)
        self.env = Environment(loader=FileSystemLoader('templates'))
        self.content_manager = ContentManager(
            self.config_system.get_posts_dir(),
            self.config_system.get_output_dir())
        self.html_generator = HTMLGenerator(self.env,
                                            self.config_system.get_all())

    def generate_site(self):
        os.makedirs(self.config_system.get('output_dir'), exist_ok=True)

        # Process all posts and collect their metadata
        posts = []
        for filename in os.listdir(self.config_system.get_posts_dir()):
            if filename.endswith('.md'):
                post_data = self.process_post(filename)
                if post_data:
                    posts.append(post_data)

        # Sort posts by date
        posts.sort(key=lambda x: x['metadata'].get('date', ''), reverse=True)

        # Generate index pages
        self.generate_index_pages(posts)

    def process_post(self, filename):
        frontmatter, content = self.content_manager.read_post(filename)
        if not frontmatter or not content:
            return None

        # Generate HTML content
        html_content = self.html_generator.generate_post(content, frontmatter)

        # Save output
        output_path = os.path.join(self.config_system.get('output_dir'),
                                   filename.replace('.md', '.html'))
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        return {
            'filename': filename.replace('.md', '.html'),
            'metadata': frontmatter
        }

    def generate_index_pages(self, posts):
        posts_per_page = self.config_system.get('posts_per_page', 10)
        total_posts = len(posts)
        total_pages = (total_posts + posts_per_page - 1) // posts_per_page

        for page in range(1, total_pages + 1):
            html_content = self.html_generator.generate_index(posts, page)

            if page == 1:
                output_path = os.path.join(
                    self.config_system.get('output_dir'), 'index.html')
            else:
                output_path = os.path.join(
                    self.config_system.get('output_dir'), f'page{page}.html')

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)


from flask import Flask, send_from_directory, url_for

app = Flask(__name__)


@app.route('/')
def index():
    return send_from_directory('output', 'index.html')


@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('output', path)


@app.route('/static/<path:path>')
def serve_assets(path):
    return send_from_directory('static', path)


if __name__ == '__main__':
    generator = BlogGenerator()
    generator.generate_site()
    app.run(host='0.0.0.0', port=3000, debug=True)
