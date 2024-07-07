from flask import url_for, current_app, render_template
from collections import OrderedDict


def render_header(active_page, subcategory=None):
    standard_pages = OrderedDict([
        ('home', 'Home'),
        ('services', 'Services'),
        ('portfolio', 'Portfolio'),
        ('experience', 'Experience'),
        ('contact', 'Contact')
    ])
    active_page_lower = active_page.lower()

    with current_app.test_request_context():
        nav_items = [
            {
                'label': label,
                'url': url_for(f'main.{page}'),
                'active': active_page_lower == page
            }
            for page, label in standard_pages.items()
        ]

        if active_page_lower not in standard_pages:
            try:
                url = url_for(f'main.{active_page_lower}')
            except Exception as e:
                current_app.logger.error(f"Failed to generate URL for {active_page}: {e}")
                url = '#'
            nav_items.append({'label': active_page, 'url': url, 'active': True})

        if subcategory:
            active_index = next((i for i, item in enumerate(nav_items) if item['active']), None)
            if active_index is not None:
                active_item = nav_items[active_index]
                nav_items.insert(active_index + 1, {
                    'label': f"{active_item['label']} | {subcategory}",
                    'url': '#',
                    'active': True
                })
                active_item['active'] = False

    return render_template('header.html', nav_items=nav_items)


def render_footer():
    return render_template('footer.html')
