from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required
from utils import sanitize_input, serve_slides_thesis, serve_admin_slides, serve_file_by_num, retrieve_db_slides
from models.transactions import get_collection, insert_one, find_one, update_one, update_many, delete_one, DatabaseError
from components import render_slide_management_view
from bson import ObjectId
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
    media = request.form.get('media')
    urls = request.form.getlist('urls')
    length = request.form.get('length')

    if not all([name, title, media, urls]) or media == 'vid' and not length:
        flash("Please fill all required fields", 'error')
        return redirect(url_for("slides.input_slides"))

    fields = {
        'name': name,
        'title': title,
        'urls': urls,
        'media': media,
        'length': length
    }
    document = {key: value for key, value in fields.items() if value}

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
    media = request.args.get('media', default=None, type=str)

    try:
        title, urls_with_index = asyncio.run(retrieve_db_slides(name))

        if media:
            return render_template('media.html', urls=urls_with_index, title=title)

        return render_template('viewer.html', urls=urls_with_index, title=title)

    except DatabaseError as e:
        flash(f"An error occurred:{e}", "error")
        return redirect(url_for("main.error"))


@slides_bp.route('/view-an/<name>')
def view_anonymous(name):
    media = request.args.get('media', default=None, type=str)

    try:
        title, urls_with_index = asyncio.run(retrieve_db_slides(name))
        if media:
            return render_template('media_anon.html', urls=urls_with_index, title=title)

        return render_template('viewer.html', urls=urls_with_index, title=title)

    except DatabaseError as e:
        flash(f"An error occurred:{e}", "error")
        return redirect(url_for("main.error"))


@slides_bp.route('/slides-directory/')
@admin_only
@login_required
def view_directory():
    try:
        filter_tag = request.args.get("tag")
        query = {}
        if filter_tag:
            query["tags"] = filter_tag
        slides_results = get_collection("slidesviewer", "slides").find(query,
                                                                       {"name": 1, "title": 1, "urls": 1, "media": 1,
                                                                        "length": 1, "tags": 1, "hidden": 1})

        master_tags = get_collection("slidesviewer", "master_tags").find_one({"_id": "master_list"})
        all_tags = master_tags["tags"] if master_tags else []

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # This is an AJAX request, return only the slides HTML
            rendered_slides = []
            for slide in slides_results:
                rendered_slide = render_template('slide_template.html', slide=slide)
                rendered_slides.append(rendered_slide)
            return jsonify({"html": "".join(rendered_slides)})
        else:
            return render_template('view-directory.html', slides=slides_results, title="Media", all_tags=all_tags,
                                   current_tag=filter_tag)

    except DatabaseError as e:
        flash(f"An error occurred:{e}", "error")
        return redirect(url_for("main.error"))


@slides_bp.route('/search_slides/')
@admin_only
@login_required
def search_slides():
    search_query = request.args.get('query', '')
    try:
        slides_results = get_collection("slidesviewer", "slides").find(
            {"title": {"$regex": search_query, "$options": "i"}},
            {"name": 1, "title": 1, "urls": 1, "media": 1, "length": 1, "hidden": 1}
        )
        rendered_slides = []
        for slide in slides_results:
            rendered_slide = render_template('slide_template.html', slide=slide)
            rendered_slides.append(rendered_slide)
        return jsonify({"html": "".join(rendered_slides)})
    except DatabaseError as e:
        return jsonify({"error": str(e)}), 500


@slides_bp.route('/delete-slide/<name>', methods=['GET', 'POST'])
@admin_only
@login_required
def delete_slide(name):
    try:
        delete_one("slidesviewer", "slides", {'name': name})
        flash("Slides document successfully deleted", "success")
    except DatabaseError as e:
        flash(f"An error occurred: {e}", "error")

    return redirect(url_for("slides.view_directory"))


@slides_bp.route('/update-slide/<name>', methods=['GET', 'POST'])
@admin_only
@login_required
def update_slide(name):
    if request.method == 'POST':

        fields = {
            'name': name,
            'title': request.form.get('title'),
            'urls': request.form.getlist('urls[]'),
            'tags': [tag.strip().lower() for tag in request.form.get('tags', '').split(',') if tag.strip()],
            'hidden': request.form.get('hidden'),
            'length': request.form.get('length'),
        }

        updated_slide = {key: value for key, value in fields.items() if value is not None}

        if 'hidden' in updated_slide:
            updated_slide['hidden'] = bool(updated_slide['hidden'])
        if 'hidden' not in updated_slide:
            updated_slide['hidden'] = False

        tags = updated_slide.get('tags', [])

        try:
            update_one("slidesviewer", "slides", {'name': name}, {"$set": updated_slide})
            update_master_tag_list(tags)
            flash("Slides document successfully updated", "success")
            return redirect(url_for("slides.view_directory"))
        except DatabaseError as e:
            flash(f"An error occurred: {e}", "error")
            return redirect(url_for("main.error"))

    try:
        slide = find_one("slidesviewer", "slides", {'name': name})
        if not slide:
            flash("Slide not found", "error")
            return redirect(url_for("slides.view_directory"))

        return render_template('view-directory.html', slide=slide, title="Edit Slide")
    except DatabaseError as e:
        flash(f"An error occurred: {e}", "error")
        return redirect(url_for("slides.view_directory"))


def update_master_tag_list(tags):
    master_tag_list = get_collection("slidesviewer", "master_tags").find_one({"_id": "master_list"})
    try:
        if not master_tag_list:
            insert_one("slidesviewer", "master_tags", {
                "_id": "master_list",
                "tags": tags
            })

        else:
            new_tags = set(tags) - set(master_tag_list["tags"])
            if new_tags:
                update_one("slidesviewer", "master_tags",
                           {"_id": "master_list"},
                           {"$addToSet": {"tags": {"$each": list(new_tags)}}}
                           )
    except DatabaseError as e:
        raise e


@slides_bp.route('/update_slide_visibility', methods=['POST'])
@admin_only
@login_required
def update_slide_visibility():
    data = request.json
    action = data['action']
    slide_ids = [ObjectId(id_) for id_ in data['slides']]

    hidden_value = True if action == 'hide' else False

    try:
        result = update_many("slidesviewer", "slides",
                             {"_id": {"$in": slide_ids}},
                             {"$set": {"hidden": hidden_value}}
                             )
        if result is not None:
            return jsonify(
                {"success": True, "updated": f'Successfully modified {result.modified_count} slides visibilities'})
        return jsonify({"success": True, "updated": 'No slides were modified'})
    except DatabaseError as e:
        return jsonify({"success": False, "error": str(e)})


@slides_bp.route('/slide_management')
@admin_only
@login_required
def slide_management():
    try:
        search_query = request.args.get('query', '')
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':

            slides_results = get_collection("slidesviewer", "slides").find(
                {"title": {"$regex": search_query, "$options": "i"}},
                {"title": 1, "hidden": 1}
            )
            slides_html = render_slide_management_view(slides_results)

            return jsonify({'html': slides_html})
        else:
            slides_results = get_collection("slidesviewer", "slides").find({}, {"title": 1, "hidden": 1})
            return render_template('slides-management.html', slides=slides_results, visibility_management=True,
                                   title='Visibility Management')

    except DatabaseError as e:
        flash(f"An error occurred:{e}", "error")
        return redirect(url_for("main.error"))


@admin_only
@login_required
@slides_bp.route('/tags_management')
def tags_management():
    return render_template('slides-management.html', tag_management=True, title='Tag Management')


@admin_only
@login_required
@slides_bp.route('/get_tags')
def get_tags():
    try:
        master_doc = find_one('slidesviewer', 'master_tags', {'_id': 'master_list'})
        if master_doc and 'tags' in master_doc:
            return jsonify({'tags': master_doc['tags']})
        return jsonify({'tags': []})
    except DatabaseError as e:
        return jsonify({"success": False, "error": str(e)})


@admin_only
@login_required
@slides_bp.route('/update_tag', methods=['POST'])
def update_tag():
    try:
        data = request.json
        old_tag = data['old_tag']
        new_tag = data['new_tag']

        result = update_one('slidesviewer', 'master_tags',
                            {'_id': 'master_list'},
                            {'$pull': {'tags': old_tag}}
                            )

        if result.modified_count > 0:
            update_one('slidesviewer', 'master_tags',
                       {'_id': 'master_list'},
                       {'$push': {'tags': new_tag}}
                       )
            return jsonify({'success': True})
        return jsonify({'success': False})

    except DatabaseError as e:
        return jsonify({"success": False, "error": str(e)})


@admin_only
@login_required
@slides_bp.route('/delete_tag', methods=['POST'])
def delete_tag():
    try:
        data = request.json
        tag = data['tag']

        result = update_one('slidesviewer', 'master_tags',
                            {'_id': 'master_list'},
                            {'$pull': {'tags': tag}}
                            )

        if result.modified_count > 0:
            return jsonify({'success': True})
        return jsonify({'success': False})
    except DatabaseError as e:
        return jsonify({"success": False, "error": str(e)})
