

$(document).ready(function () {
    $(".toggle-form").each(function () {
        var form = $(this);
        var categoryId = form.data("list_unlist_productvarient-id");
        var toggleButton = form.find(".toggle-button");

        toggleButton.click(function () {
            var isActive = toggleButton.hasClass("btn-success");

            $.ajax({
                url: "{% url 'list_unlist_productvarient'%}",
                type: "POST",
                data: {
                    csrfmiddlewaretoken: "{{ csrf_token }}",
                    check: isActive ? "false" : "true",
                    id:list_unlist_productvarientId
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



$(document).ready(function () {
    $(".toggle-form").each(function () {
        var form = $(this);
        var categoryId = form.data("list_unlist_products-id");
        var toggleButton = form.find(".toggle-button");

        toggleButton.click(function () {
            var isActive = toggleButton.hasClass("btn-success");

            $.ajax({
                url: "{% url 'list_unlist_products'%}",
                type: "POST",
                data: {
                    csrfmiddlewaretoken: "{{ csrf_token }}",
                    check: isActive ? "false" : "true",
                    id:list_unlist_productsId
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
