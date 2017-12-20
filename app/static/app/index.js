$('.panel-footer').on('click', function() {
    console.log(this);
    $($(this).find('.panelfoot')).toggle();
});
