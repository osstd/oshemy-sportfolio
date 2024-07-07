from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from utils import sanitize_input, serve_slides_thesis, serve_admin_slides, serve_file_by_num
from models.transactions import get_collection, insert_one, find_one, DatabaseError
from admin import admin_only
from urllib.parse import unquote
import asyncio

slides_bp = Blueprint('slides', __name__)


@slides_bp.route('/files/<int:num>')
def file(num):
    return asyncio.run(serve_file_by_num(num))


@slides_bp.route('/experience/ge/slides')
def slides():
    image_paths_with_index = asyncio.run(serve_slides_thesis())
    return render_template('se.html', image_paths=image_paths_with_index, title="Thesis Seminar")


@slides_bp.route('/admin_slide/<int:num>/<d>/<t>')
@admin_only
@login_required
def admin_slide(num, d, t):
    decoded_t = unquote(t)
    image_paths_with_index = asyncio.run(serve_admin_slides(num, d))
    return render_template('se.html', image_paths=image_paths_with_index, title=decoded_t)


@slides_bp.route('/input')
def input_slides():
    return render_template('input.html')


@slides_bp.route('/save', methods=['POST'])
@admin_only
@login_required
def save_slides():
    name = sanitize_input(request.form.get('name'))
    title = sanitize_input(request.form.get('title'))
    urls = request.form.getlist('urls')

    document = {
        'name': name,
        'title': title,
        'urls': urls
    }
    try:
        insert_one("slidesviewer", "slides", document)
        flash("Input done", "success")
    except DatabaseError as e:
        flash(f"An error occurred:{e}", "error")

    return redirect(url_for("slides.input_slides"))


@slides_bp.route('/view/<name>')
@admin_only
@login_required
def view(name):
    try:
        document = find_one("slidesviewer", "slides", {'name': name})
        urls = document.get('urls', [])
        title = document.get('title', 'Title Not found')
        urls_with_index = [(index, url) for index, url in enumerate(urls)]
        return render_template('viewer.html', urls=urls_with_index, title=title)

    except DatabaseError as e:
        flash(f"An error occurred:{e}", "error")
        return redirect(url_for("main.error"))


@slides_bp.route('/slides-directory/')
@admin_only
@login_required
def view_directory():
    try:
        slides_results = get_collection("slidesviewer", "slides").find({}, {"name": 1, "title": 1, "urls": 1})
        return render_template('view-directory.html', slides=slides_results, title="Slides")

    except DatabaseError as e:
        flash(f"An error occurred:{e}", "error")
        return redirect(url_for("main.error"))
