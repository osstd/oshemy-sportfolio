$.ajaxSetup({
  beforeSend: function (xhr, settings) {
    if (
      !/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) &&
      !this.crossDomain
    ) {
      xhr.setRequestHeader("X-CSRFToken", csrfToken);
    }
  },
});

$(document).ready(function () {
  loadTags();

  function loadTags() {
    $.ajax({
      url: "/get_tags",
      method: "GET",
      success: function (response) {
        let tableBody = $("#tagTableBody");
        tableBody.empty();
        response.tags.forEach(function (tag) {
          tableBody.append(`
                                <tr>
                                    <td>${
                                      tag.charAt(0).toUpperCase() +
                                      tag.slice(1).toLowerCase()
                                    }</td>
                                    <td>
                                        <i class="fas fa-edit action-btn" onclick="editTag('${tag}')"></i>
                                        <i class="fas fa-trash-alt tag action-btn" onclick="deleteTag('${tag}')"></i>
                                    </td>
                                </tr>
                            `);
        });
      },
    });
  }

  window.editTag = function (tag) {
    if (confirm(`Are you sure you want to edit the tag "${tag}"?`)) {
      let newTag = prompt("Enter new tag name:", tag);
      if (newTag && newTag !== tag) {
        $.ajax({
          url: "/update_tag",
          method: "POST",
          data: JSON.stringify({ old_tag: tag, new_tag: newTag }),
          contentType: "application/json",
          success: function (response) {
            if (response.success) {
              alert("Tag update successful!");
              loadTags();
            } else {
              alert("Failed to update tag!");
            }
          },
        });
      }
    }
  };

  window.deleteTag = function (tag) {
    if (confirm(`Are you sure you want to delete the tag "${tag}"?`)) {
      $.ajax({
        url: "/delete_tag",
        method: "POST",
        data: JSON.stringify({ tag: tag }),
        contentType: "application/json",
        success: function (response) {
          if (response.success) {
            alert("Tag deletion successful!");
            loadTags();
          } else {
            alert("Failed to delete tag!");
          }
        },
      });
    }
  };
});
