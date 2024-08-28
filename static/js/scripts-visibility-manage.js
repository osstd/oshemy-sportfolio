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
  $("#searchInput").on("input", function () {
    var query = $(this).val();
    $.ajax({
      url: "/slide_management",
      data: { query: query },
      success: function (data) {
        if (data.html) {
          $("#slideTable").html(data.html);
        } else if (data.error) {
          console.error("Error:", data.error);
        }
      },
    });
  });
});

$(document).ready(function () {
  function updateSlides(action) {
    if (confirm(`Are you sure you want to ${action} ?`)) {
      var selectedSlides = [];
      $(".slide-select:checked").each(function () {
        selectedSlides.push($(this).closest("tr").data("slide-id"));
      });

      $.ajax({
        url: "/update_slide_visibility",
        method: "POST",
        data: JSON.stringify({
          action: action,
          slides: selectedSlides,
        }),
        contentType: "application/json",
        success: function (response) {
          if (response.success) {
            alert(response.updated);
            location.reload();
          } else {
            alert("Error updating slides");
          }
        },
      });
    }
  }

  $("#hideSelected").click(function () {
    updateSlides("hide");
  });

  $("#unhideSelected").click(function () {
    updateSlides("unhide");
  });

  $("#toggleAll").click(function () {
    $(".slide-select").prop(
      "checked",
      !$(".slide-select").first().prop("checked")
    );
  });
});
