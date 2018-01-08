$('.panel-click').on('click', function() {
    $(
        $(this)
            .parent()
            .find('.panelfoot')
    ).toggle();
});

function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function(e) {
            $('#preview-img')
                .attr('src', e.target.result)
                .attr('width', 320)
                .attr('height', 260);
        };

        reader.readAsDataURL(input.files[0]);
    }
}

$('#id_image').on('change', function() {
    readURL(this);
});

function makeActive(s) {
    $('li').removeClass('active');
    $('#' + String(s)).addClass('active');
}
