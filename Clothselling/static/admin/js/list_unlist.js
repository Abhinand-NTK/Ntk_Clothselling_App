$(document).ready(function () {
    $(".toggle-form").each(function () {
        var form = $(this);
        var categoryId = form.data("category-id");
        var toggleButton = form.find(".toggle-button");

        toggleButton.click(function () {
            var isActive = toggleButton.hasClass("btn-success");

            $.ajax({
                url: "{% url 'category'%}",
                type: "POST",
                data: {
                    csrfmiddlewaretoken: "{{ csrf_token }}",
                    check: isActive ? "false" : "true",
                    id: categoryId
                },
                success: function (response) {
                    // Toggle button color and text
                    toggleButton.toggleClass("btn-success btn-danger");
                    if (isActive) {
                        toggleButton.text("List");
                    } else {
                        toggleButton.text("Unlist");
                    }
                },
                error: function (xhr, textStatus, errorThrown) {
                    // Handle error
                }
            });
        });
    });
});
